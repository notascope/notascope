import json
import plotly.graph_objects as go
from functools import cache


import numpy as np
from .distances import dmat_and_order, get_distance


def get_dendro(gallery, notation, distance, from_spec, to_spec, vis):
    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    fig_json, y_by_spec, leaves = build_dendro(gallery, notation, distance)
    fig = go.Figure(json.loads(fig_json))
    if from_spec:
        from_y = y_by_spec[from_spec]
        to_y = y_by_spec[to_spec]
        distance = dmat_sym[order.index(from_spec), order.index(to_spec)]
        fig.add_scatter(
            x=[0, -distance, -distance, 0],
            y=[from_y, from_y, to_y, to_y],
            marker_opacity=[1, 0, 0, 1],
            hoverinfo="skip",
            showlegend=False,
            marker_color="red",
            mode="lines+markers",
        )
        if from_spec == to_spec:
            fig.data[1].marker = dict(
                color=dmat_sym[order.index(from_spec)][leaves],
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
def build_dendro(gallery, notation, distance):
    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    from scipy.cluster import hierarchy
    from scipy.spatial.distance import squareform

    Z = hierarchy.linkage(squareform(dmat_sym), "average", optimal_ordering=True)
    P = hierarchy.dendrogram(Z, labels=order, no_plot=True)
    nodes, root = make_nodes(P, order)
    x = []
    y = []
    hovertext = []
    label_x = []
    label_y = []
    label_text = []
    y_by_spec = dict()

    def append_point(x_val, y_val):
        y.append(y_val)
        x.append(-x_val)
        cluster_members = nodes[(x_val, y_val)][1]
        node_spec = None
        if len(cluster_members):
            cluster_medioid = medioid(cluster_members, dmat_sym)
            node_spec = order[cluster_medioid]
        hovertext.append([node_spec])

    for i, (icoord, dcoord) in enumerate(zip(P["icoord"], P["dcoord"])):
        for j, (y_val, x_val) in enumerate(zip(icoord, dcoord)):
            append_point(x_val, y_val)
            if x_val == 0:
                spec = P["ivl"][int((y_val - 5) / 10)]
                if spec not in y_by_spec:
                    y_by_spec[spec] = y_val
                    label_x.append(-x_val)
                    label_y.append(y_val)
                    label_text.append(spec)
        y.append(None)
        x.append(None)
        hovertext.append(None)
    append_point(root[0], root[1])

    y, label_y, y_by_spec = respace(gallery, notation, distance, y, label_y, y_by_spec)

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
        cliponaxis=False,
    )
    fig.update_layout(
        height=800, showlegend=False, dragmode="pan", plot_bgcolor="white"
    )
    fig.update_layout(uirevision="yes", margin=dict(l=10, r=100))
    fig.update_yaxes(visible=False)
    return fig.to_json(), y_by_spec, P["leaves"]


def respace(gallery, notation, distance, y, label_y, y_by_spec):
    spec_by_y = {v: k for k, v in y_by_spec.items()}
    prev_y = None
    remap = []
    for curr_y in sorted(spec_by_y.keys()):
        if prev_y:
            remap.append(
                (
                    prev_y,
                    curr_y,
                    get_distance(
                        gallery,
                        notation,
                        distance,
                        spec_by_y[prev_y],
                        spec_by_y[curr_y],
                    ),
                )
            )
        else:
            remap.append((0, curr_y, 0))
        prev_y = curr_y

    def scale_y(y_in, remap):
        if y_in is None:
            return None
        y_out = 0
        for start, end, accum in remap:
            if y_in > start:
                if y_in > end:
                    y_out += accum
                else:
                    y_out += accum * (y_in - start) / (end - start)
        return y_out

    y = [scale_y(yy, remap) for yy in y]
    label_y = [scale_y(yy, remap) for yy in label_y]
    y_by_spec = {k: scale_y(v, remap) for k, v in y_by_spec.items()}
    return y, label_y, y_by_spec
