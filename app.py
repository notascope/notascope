# builtins
import re
import sys
import json
from collections import Counter
from glob import glob

# perf
from numba import njit
from functools import cache

# plotly
from dash import Dash, html, dcc, Input, Output, State, callback_context
import dash_cytoscape as cyto
from dash_extensions import EventListener
from notascope_components import DashDiff
import plotly.express as px
import plotly.graph_objects as go

# data science
import pandas as pd
import numpy as np
import igraph
from sklearn.manifold import MDS, TSNE
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import coo_matrix
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

default_study = "tiny"
vis_types = ["network", "tsne", "dendro"]
cost_types = ["difflib", "compression"]

print("start", np.random.randint(1000))  # unseeded so every launch is different
np.random.seed(1)  # now set seed for deterministic embedding algos

difflib_df = pd.read_csv(f"results/difflib_costs.csv", names=["study", "system", "from_slug", "to_slug", "difflib"])
ncd_df = pd.read_csv(f"results/ncd_costs.csv", names=["study", "system", "from_slug", "to_slug", "compression"])
costs_df = pd.merge(difflib_df, ncd_df, how="outer")
tokens_df = pd.read_csv("results/tokens.tsv", names=["study", "system", "slug", "token"], delimiter="\t")


def ext_of_longest(study, system, obj):
    return sorted(glob(f"results/{study}/{system}/{obj}/*"), key=len)[-1].split(".")[-1]


filter_prefix = "study==@study and system==@system"


def load_results():
    results = dict()
    for (study, system), df in tokens_df.groupby(["study", "system"]):
        if study not in results:
            results[study] = dict()
        results[study][system] = dict(
            imgext=ext_of_longest(study, system, "img"),
            srcext=ext_of_longest(study, system, "source"),
            slugs=df["slug"].unique(),
            tokens=df["token"].nunique(),
        )
    return results


results = load_results()
print("ready")

app = Dash(__name__, title="NotaScope", suppress_callback_exceptions=True)


app.layout = html.Div(
    [
        html.Div(id="content"),
        dcc.Location(id="location"),
        dcc.Tooltip(
            id="tooltip",
            children=[
                html.Div(
                    [
                        html.P(id="tt_name", style=dict(textAlign="center")),
                        html.Img(id="tt_img", style={"max-width": "300px", "max-height": "200px"}),
                    ],
                    style={"width": "300px", "height": "230px", "overflow": "hidden"},
                )
            ],
        ),
        EventListener(
            id="event_listener",
            events=[
                {"event": "keydown", "props": ["shiftKey"]},
                {"event": "keyup", "props": ["shiftKey"]},
            ],
        ),
    ]
)


@cache
def square_and_order(study, system, cost):
    df = costs_df.query(filter_prefix)
    square = df.pivot_table(index="from_slug", columns="to_slug", values=cost).fillna(0)
    order = list(square.index)
    square = square.values
    return square, order


def get_tsne(study, system, cost, from_slug, to_slug):
    fig_json, fig_df = build_tsne(study, system, cost)
    fig = go.Figure(json.loads(fig_json))

    if from_slug:
        from_row = fig_df.loc[from_slug]
        to_row = fig_df.loc[to_slug]
        fig.add_scatter(x=[from_row.x, to_row.x], y=[from_row.y, to_row.y], hoverinfo="skip", showlegend=False)

    return fig


@cache
def build_tsne(study, system, cost):
    square, order = square_and_order(study, system, cost)
    tsne = TSNE(n_components=2, metric="precomputed", square_distances=True, learning_rate="auto", init="random")
    embedding = tsne.fit_transform((square + square.T) / 2)
    emb_df = pd.DataFrame(embedding, index=order, columns=["x", "y"])
    fig = px.scatter(emb_df, x="x", y="y", hover_name=order)
    fig.update_layout(height=700, width=700, dragmode="pan", plot_bgcolor="white")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), uirevision="yes")
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig.to_json(), emb_df


def get_dendro(study, system, cost, from_slug, to_slug):
    fig = go.Figure(json.loads(build_dendro(study, system, cost)))
    return fig


@cache
def build_dendro(study, system, cost):
    square, order = square_and_order(study, system, cost)
    Z = hierarchy.linkage(squareform((square + square.T) / 2.0), "complete", optimal_ordering=True)
    P = hierarchy.dendrogram(Z, labels=order, no_plot=True)

    x = []
    y = []
    label_x = []
    label_y = []
    label_text = []
    for icoord, dcoord in zip(P["icoord"], P["dcoord"]):
        for i, d in zip(icoord, dcoord):
            y.append(i)
            x.append(-d)
            if d == 0:
                label_x.append(-d)
                label_y.append(i)
                label_text.append(P["ivl"][int((i - 5) / 10)])
        y.append(None)
        x.append(None)
    fig = go.Figure()
    fig.add_scatter(x=x, y=y, line_width=1, hoverinfo="skip", mode="lines")
    fig.add_scatter(x=label_x, y=label_y, text=label_text, hovertext=label_text, mode="text", textposition="middle right", hoverinfo="none")
    fig.update_layout(height=800, showlegend=False)
    return fig.to_json()


def get_network(study, system, cost, from_slug, to_slug):
    net = json.loads(build_network(study, system, cost))

    if from_slug != to_slug:
        for_cost = get_cost(study, system, cost, from_slug, to_slug)
        rev_cost = get_cost(study, system, cost, to_slug, from_slug)
        both_dirs = [[from_slug, to_slug], [to_slug, from_slug]]
        to_drop = ["__".join(x) for x in both_dirs]
        dropped = [elem for elem in net if elem["data"]["id"] in to_drop]
        net = [elem for elem in net if elem["data"]["id"] not in to_drop]
        for source, dest in both_dirs:
            id = source + "__" + dest
            new_elem = {
                "data": {
                    "source": source,
                    "target": dest,
                    "id": id,
                    "length": for_cost if source == from_slug else rev_cost,
                },
                "classes": "",
            }
            if len(dropped) == 0 or (id not in [x["data"]["id"] for x in dropped] and "bidir" not in dropped[0]["classes"]):
                new_elem["classes"] += " inserted"
            if source == from_slug:
                new_elem["classes"] += " selected"
            net.append(new_elem)
    for elem in net:
        if elem["data"]["id"] in [from_slug, to_slug]:
            elem["classes"] += " selected"
    return net


@njit
def find_edges(square):
    n = len(square)
    result = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            has_k = False
            direct = square[i, j]
            if direct != 0:
                for k in range(n):
                    if k == i or k == j:
                        continue
                    via_k = square[i, k] + square[k, j]
                    if (via_k - direct) / direct <= 0:
                        has_k = True
                        break
                if not has_k:
                    result[i, j] = direct
    return result


@cache
def build_network(study, system, cost):
    square, order = square_and_order(study, system, cost)
    network_elements = []
    n = len(square)
    if n < 20:
        mds = MDS(n_components=2, dissimilarity="precomputed")
        embedding = mds.fit_transform((square + square.T) / 2)

        edges = find_edges(square)
        for i in range(n):
            for j in range(n):
                if edges[i, j] == 0:  # no zero or self-edges
                    continue
                longest = edges[i, j] > edges[j, i]
                eq = edges[i, j] == edges[j, i]
                this_eq = eq and i > j  # only first of the two bidir edges
                if longest or this_eq:
                    network_elements.append(
                        {
                            "data": {
                                "source": order[i],
                                "target": order[j],
                                "id": order[i] + "__" + order[j],
                                "length": edges[i, j],
                            },
                            "classes": (" bidir" if eq else ""),
                        }
                    )
    else:
        spanning = coo_matrix(minimum_spanning_tree(square))
        g = igraph.Graph.Weighted_Adjacency(spanning.toarray().tolist())
        layout = g.layout_kamada_kawai(maxiter=10000)
        embedding = np.array(layout.coords)

        for i, j, d in zip(spanning.row, spanning.col, spanning.data):
            network_elements.append(
                {
                    "data": {
                        "source": order[i],
                        "target": order[j],
                        "id": order[i] + "__" + order[j],
                        "length": d,
                    },
                    "classes": "",
                }
            )

    emb_df = pd.DataFrame(embedding, index=order, columns=["x", "y"])
    emb_span = embedding.max() - embedding.min()

    scale = 1000 if n < 20 else 10000
    imgext = results[study][system]["imgext"]
    for i, row in emb_df.iterrows():
        network_elements.append(
            {
                "data": {
                    "id": i,
                    "label": i,
                    "url": f"/assets/results/{study}/{system}/img/{i}.{imgext}",
                },
                "position": {c: row[c] * scale / emb_span for c in ["x", "y"]},
                "classes": "",
            }
        )
    return json.dumps(network_elements)


def parse_hashpath(hashpath):
    m = re.match("#" + "/(.*)" * 9, hashpath)
    if m:
        return sanitize_state(*m.groups())
    else:
        return sanitize_state()


def sanitize_state(study="", system="", cost="", vis="", system2="", cost2="", vis2="", from_slug="", to_slug=""):
    if vis not in vis_types:
        vis = vis_types[0]

    if vis2 not in vis_types:
        vis2 = vis_types[0]

    if cost not in cost_types:
        cost = cost_types[0]

    if cost2 not in cost_types:
        cost2 = cost_types[0]

    if study not in results:
        study = default_study

    study_res = results[study]
    slugs = set()
    if system in study_res:
        for s in study_res[system]["slugs"]:
            slugs.add(s)
    else:
        system = list(results[study].keys())[0]

    if system2 in study_res:
        for s in study_res[system2]["slugs"]:
            slugs.add(s)
    else:
        system2 = ""

    if system2 == "":
        vis2 = ""
        cost2 = ""

    if from_slug not in slugs:
        from_slug = to_slug = ""
    elif to_slug not in slugs:
        to_slug = from_slug

    return study, system, cost, vis, system2, cost2, vis2, from_slug, to_slug


@app.callback(
    Output("location", "hash"),
    Output("network", "tapNodeData"),
    Output("network", "tapEdgeData"),
    Output("network2", "tapNodeData"),
    Output("network2", "tapEdgeData"),
    Input("selection", "data"),
    Input("study", "value"),
    Input("system", "value"),
    Input("system2", "value"),
    Input("cost", "value"),
    Input("cost2", "value"),
    Input("vis", "value"),
    Input("vis2", "value"),
    Input("network", "tapNodeData"),
    Input("network", "tapEdgeData"),
    Input("figure", "clickData"),
    Input("network2", "tapNodeData"),
    Input("network2", "tapEdgeData"),
    Input("figure2", "clickData"),
    State("event_listener", "event"),
)
def update_hashpath(
    selection, study, system, system2, cost, cost2, vis, vis2, node_data, edge_data, fig_data, node_data2, edge_data2, fig_data2, event
):
    shift_down = bool((dict(shiftKey=False) if not event else event)["shiftKey"])
    ctx = callback_context
    from_slug, to_slug = selection
    if ctx.triggered:
        click_system = ctx.triggered[0]["prop_id"].split(".")[0]
        click_type = ctx.triggered[0]["prop_id"].split(".")[1]

        if click_type == "tapNodeData":
            if click_system == "network":
                to_slug = node_data["id"]
                if not shift_down:
                    from_slug = to_slug
            if click_system == "network2":
                to_slug = node_data2["id"]
                if not shift_down:
                    from_slug = to_slug
            edge_data = None
            edge_data2 = None
        if click_type == "tapEdgeData":
            if click_system == "network":
                from_slug = edge_data["source"]
                to_slug = edge_data["target"]
            if click_system == "network2":
                from_slug = edge_data2["source"]
                to_slug = edge_data2["target"]
            node_data = None
            node_data2 = None
        if click_type == "clickData":
            if click_system == "figure":
                to_slug = fig_data["points"][0]["hovertext"]
                if not shift_down:
                    from_slug = to_slug
            if click_system == "figure2":
                to_slug = fig_data2["points"][0]["hovertext"]
                if not shift_down:
                    from_slug = to_slug
    hashpath = "#/" + "/".join(sanitize_state(study, system, cost, vis, system2, cost2, vis2, from_slug, to_slug))
    return hashpath, node_data, edge_data, node_data2, edge_data2


@app.callback(
    Output("content", "children"),
    Input("location", "hash"),
)
def update_content(hashpath):
    study, system, cost, vis, system2, cost2, vis2, from_slug, to_slug = parse_hashpath(hashpath)
    cmp, net, fig = details_view(study, system, cost, vis, from_slug, to_slug)
    if system2:
        style = dict()
        style2 = dict(gridColumnStart=2, display="block")
        cmp2, net2, fig2 = details_view(study, system2, cost2, vis2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(display="none", gridRowStart=3)
        cmp2, net2, fig2 = None, [], {}

    vis2_style = dict(width="100px")
    if system == system2 and cost == cost2:
        cmp2 = None
    if not system2:
        vis2_style["display"] = "none"

    systems = [dict(label=f"{s} ({results[study][s]['tokens']})", value=s) for s in results[study]]

    return html.Div(
        className="wrapper",
        children=[
            html.Div(
                [dcc.Dropdown(id="study", value=study, options=[s for s in results], clearable=False, style=dict(width="100px"))],
                style=dict(position="absolute", left=10, top=10),
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(id="system", value=system, options=systems, clearable=False, className="dropdown"),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="vis", value=vis, options=vis_types, clearable=False, style=dict(width="100px")),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="cost", value=cost, options=cost_types, clearable=False, style=dict(width="100px")),
                        style=dict(display="inline-block"),
                    ),
                ],
                style=dict(margin="0 auto"),
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(id="system2", value=system2, options=systems, clearable=True, className="dropdown"),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="vis2", value=vis2, options=vis_types, clearable=False, style=vis2_style),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="cost2", value=cost2, options=cost_types, clearable=False, style=vis2_style),
                        style=dict(display="inline-block"),
                    ),
                ],
                style=dict(margin="0 auto"),
            ),
            html.Div(network_or_figure(net, fig, ""), style=style),
            html.Div(network_or_figure(net2, fig2, "2"), style=style2),
            html.Div(cmp, className="comparison"),
            html.Div(cmp2, className="comparison"),
            dcc.Store(id="selection", data=[from_slug, to_slug]),
        ],
    )


def network_or_figure(net, fig, suffix):
    if net:
        net_style, fig_style = dict(), dict(display="none")
    else:
        net_style, fig_style = dict(display="none"), dict()

    return [
        html.Div(cytoscape("network" + suffix, net), style=net_style),
        html.Div(dcc.Graph(id="figure" + suffix, figure=fig, config=dict(scrollZoom=True), clear_on_unhover=True), style=fig_style),
    ]


def cytoscape(id, elements):
    return cyto.Cytoscape(
        id=id,
        className="network",
        layout={"name": "preset"},
        minZoom=0.05,
        maxZoom=1,
        autoRefreshLayout=False,
        elements=elements,
        stylesheet=[
            {
                "selector": "node",
                "style": {
                    "width": 100,
                    "height": 100,
                    "shape": "rectangle",
                    "background-fit": "cover",
                    "background-image": "data(url)",
                    "label": "data(label)",
                    "border-color": "grey",
                    "border-width": 1,
                    "text-outline-color": "white",
                    "text-outline-width": "2",
                    "text-margin-y": "20",
                },
            },
            {
                "selector": "edge",
                "style": {
                    "line-color": "grey",
                    "curve-style": "bezier",
                    "target-arrow-color": "grey",
                    "control-point-weight": 0.6,
                    "target-arrow-shape": "triangle-backcurve",
                    "arrow-scale": 2,
                    "label": "data(length)",
                    "font-size": "24px",
                    "text-outline-color": "white",
                    "text-outline-width": "3",
                },
            },
            {
                "selector": ".bidir",
                "style": {
                    "source-arrow-color": "grey",
                    "source-arrow-shape": "triangle-backcurve",
                },
            },
            {
                "selector": ".selected",
                "style": {
                    "source-arrow-color": "red",
                    "target-arrow-color": "red",
                    "line-color": "red",
                    "border-color": "red",
                    "border-width": 5,
                },
            },
            {
                "selector": ".inserted",
                "style": {"line-style": "dashed"},
            },
        ],
    )


def header_and_image(study, system, slug, tokens_n, tokens_nunique):
    imgext = results[study][system]["imgext"]
    return [
        html.H3(slug),
        html.P(f"{tokens_n} tokens, {tokens_nunique} uniques"),
        html.Img(
            src=f"/assets/results/{study}/{system}/img/{slug}.{imgext}",
            style=dict(verticalAlign="middle", maxHeight="200px", maxWidth="20vw"),
        ),
    ]


def diff_view(study, system, from_slug, to_slug):
    srcext = results[study][system]["srcext"]
    with open(f"results/{study}/{system}/source/{from_slug}.{srcext}", "r") as f:
        from_code = f.read()
    if from_slug == to_slug:
        to_code = from_code
    else:
        with open(f"results/{study}/{system}/source/{to_slug}.{srcext}", "r") as f:
            to_code = f.read()
    return html.Div(
        [html.Div([DashDiff(oldCode=from_code, newCode=to_code)], style=dict(border="none"))],
        style=dict(marginTop="20px", textAlign="left", height="300px", maxWidth="48vw", overflow="scroll", border="1px solid grey"),
    )


def get_token_info(study, system, slug):
    df = tokens_df.query(filter_prefix + " and slug==@slug")["token"]
    return df.values, len(df), df.nunique()


@cache
def get_cost(study, system, cost, from_slug, to_slug):
    return costs_df.query(filter_prefix + " and from_slug==@from_slug and to_slug==@to_slug")[cost].values[0]


def details_view(study, system, cost, vis, from_slug, to_slug):
    cmp = None
    net = []
    fig = {}
    if vis == "network":
        net = get_network(study, system, cost, from_slug, to_slug)
    elif vis == "tsne":
        fig = get_tsne(study, system, cost, from_slug, to_slug)
    elif vis == "dendro":
        fig = get_dendro(study, system, cost, from_slug, to_slug)
    else:
        raise Exception("invalid vis")

    try:
        from_tokens, from_tokens_n, from_tokens_nunique = get_token_info(study, system, from_slug)
        if from_slug != to_slug:

            to_tokens, to_tokens_n, to_tokens_nunique = get_token_info(study, system, to_slug)
            for_cost = get_cost(study, system, cost, from_slug, to_slug)
            rev_cost = get_cost(study, system, cost, to_slug, from_slug)

            shared_tokens = list((Counter(from_tokens) & Counter(to_tokens)).elements())
            shared_uniques = set(from_tokens) & set(to_tokens)
            td1 = html.Td(
                header_and_image(study, system, from_slug, from_tokens_n, from_tokens_nunique),
                style=dict(verticalAlign="top"),
            )
            td2 = html.Td(
                ["tokens", html.Br()]
                + [f"{from_tokens_n - len(shared_tokens)} ⬌ {to_tokens_n - len(shared_tokens)}"]
                + [html.Br(), html.Br(), "uniques", html.Br()]
                + [f"{from_tokens_nunique - len(shared_uniques)} ⬌ {to_tokens_nunique - len(shared_uniques)}"]
                + [html.Br(), html.Br(), "tree edit", html.Br(), f"{rev_cost} ⬌ {for_cost}"]
            )
            td3 = html.Td(
                header_and_image(study, system, to_slug, to_tokens_n, to_tokens_nunique),
                style=dict(verticalAlign="top"),
            )
            cmp = [html.Table([html.Tr([td1, td2, td3])], style=dict(width="100%", height="300px"))]
        elif from_slug != "":
            _, from_tokens_n, from_tokens_nunique = get_token_info(study, system, from_slug)
            cmp = header_and_image(study, system, from_slug, from_tokens_n, from_tokens_nunique)

        if from_slug != "":
            cmp += [diff_view(study, system, from_slug, to_slug)]

    except Exception as e:
        print(repr(e))

    return (cmp, net, fig)


# if/when there is a PNG system, just inline the imgext dict in the string
app.clientside_callback(
    """
    function(hoverData, hoverData2) {
        pieces = window.location.hash.split("/");
        study=pieces[1];
        if(!hoverData){
            if(!hoverData2){
                return [false, null, null, null];
            }
            hoverData = hoverData2;
            system=pieces[4];
        }
        else {
            system=pieces[2];
        }
        pt = hoverData["points"][0];
        bbox = pt["bbox"]
        slug = pt["hovertext"]
        return [true, bbox, "/assets/results/"+study+"/"+system+"/img/"+slug+".svg", slug]
    }
    """,
    Output("tooltip", "show"),
    Output("tooltip", "bbox"),
    Output("tt_img", "src"),
    Output("tt_name", "children"),
    Input("figure", "hoverData"),
    Input("figure2", "hoverData"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
