import json
import plotly.graph_objects as go
from functools import cache


import numpy as np
from .distances import dmat_and_order
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform


def get_dendro(study, notation, distance, from_slug, to_slug, vis):
    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    fig_json, y_by_slug, leaves = build_dendro(study, notation, distance)
    fig = go.Figure(json.loads(fig_json))
    if from_slug:
        from_y = y_by_slug[from_slug]
        to_y = y_by_slug[to_slug]
        distance = dmat_sym[order.index(from_slug), order.index(to_slug)]
        fig.add_scatter(
            x=[0, -distance, -distance, 0],
            y=[from_y, from_y, to_y, to_y],
            marker_opacity=[1, 0, 0, 1],
            hoverinfo="skip",
            showlegend=False,
            marker_color="red",
            mode="lines+markers",
        )
        if from_slug == to_slug:
            fig.data[1].marker = dict(
                color=dmat_sym[order.index(from_slug)][leaves],
                cmax=np.median(dmat_sym),
                colorscale="Viridis",
            )
        else:
            fig.data[1].marker.opacity = 0
    else:
        fig.data[1].marker = dict(color=np.median(dmat_sym, axis=0)[leaves])
    return fig


def append_members(nodes, node):
    if len(nodes[node]) == 2:
        return nodes[node][1]
    nodes[node].append([])
    for child in nodes[node][0]:
        if type(child) is int:
            nodes[node][1].append(child)
        else:
            nodes[node][1] += append_members(nodes, child)
    return nodes[node][1]


def make_nodes(P, order):
    nodes = dict()
    root = (0, 0)
    for xs, ys in zip(P["dcoord"], P["icoord"]):
        x_mid = (xs[1] + xs[2]) / 2
        y_mid = (ys[1] + ys[2]) / 2
        root = max(root, (x_mid, y_mid))
        for k, key in enumerate([(xs[1], ys[1]), (x_mid, y_mid), (xs[2], ys[2])]):
            nodes[key] = [[]]
            for i in [0, 3]:
                if (i == 0 and k != 2) or (i == 3 and k != 0):
                    nodes[key][0].append((xs[i], ys[i]))
                if xs[i] == 0:
                    leaf_id = order.index(P["ivl"][int((ys[i] - 5) / 10)])
                    nodes[(xs[i], ys[i])] = [[leaf_id], [leaf_id]]
    for n in nodes:
        append_members(nodes, n)
    return nodes, root


def medioid(samples, dmat_sym):
    subset = dmat_sym[samples][:, samples]
    sum_dist = np.sum(subset, axis=0)
    return samples[np.argsort(sum_dist)[0]]


@cache
def build_dendro(study, notation, distance):
    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    Z = hierarchy.linkage(squareform(dmat_sym), "average", optimal_ordering=True)
    P = hierarchy.dendrogram(Z, labels=order, no_plot=True)
    nodes, root = make_nodes(P, order)
    x = []
    y = []
    hovertext = []
    label_x = []
    label_y = []
    label_text = []
    y_by_slug = dict()

    def append_point(x_val, y_val):
        y.append(y_val)
        x.append(-x_val)
        cluster_members = nodes[(x_val, y_val)][1]
        node_slug = None
        if len(cluster_members):
            cluster_medioid = medioid(cluster_members, dmat_sym)
            node_slug = order[cluster_medioid]
        hovertext.append([node_slug])

    for i, (icoord, dcoord) in enumerate(zip(P["icoord"], P["dcoord"])):
        for j, (y_val, x_val) in enumerate(zip(icoord, dcoord)):
            append_point(x_val, y_val)
            if x_val == 0:
                slug = P["ivl"][int((y_val - 5) / 10)]
                if slug not in y_by_slug:
                    y_by_slug[slug] = y_val
                    label_x.append(-x_val)
                    label_y.append(y_val)
                    label_text.append(slug)
        y.append(None)
        x.append(None)
        hovertext.append(None)
    append_point(root[0], root[1])
    fig = go.Figure()
    fig.add_scatter(
        x=x,
        y=y,
        line_width=1,
        customdata=hovertext,
        hoverinfo="none",
        mode="lines+markers",
        marker_size=1,
    )
    fig.add_scatter(
        x=np.array(label_x)[np.argsort(label_y)],
        y=np.array(label_y)[np.argsort(label_y)],
        text=np.array(label_text)[np.argsort(label_y)],
        mode="markers+text",
        textposition="middle right",
        hoverinfo="skip",
        marker=dict(cmin=0, symbol="square"),
    )
    fig.update_layout(
        height=800, showlegend=False, dragmode="pan", plot_bgcolor="white"
    )
    fig.update_layout(uirevision="yes")
    fig.update_yaxes(visible=False)
    return fig.to_json(), y_by_slug, P["leaves"]
