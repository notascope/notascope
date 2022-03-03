import re
from dash import Dash, html, dcc, Input, Output, callback_context
import random
import json
import pandas as pd
import numpy as np
from sklearn.manifold import MDS
import os
import dash_cytoscape as cyto

print("start", np.random.randint(100))
np.random.seed(1)


def precompute():
    results = dict()
    for study in [
        d for d in os.listdir(f"./results") if os.path.isdir(f"./results/{d}")
    ]:
        if study not in results:
            results[study] = dict()
        for system in [
            d
            for d in os.listdir(f"./results/{study}")
            if os.path.isdir(f"./results/{study}/{d}")
        ]:
            df = pd.read_csv(
                f"results/{study}/{system}/costs.csv",
                names=["study", "system", "from", "to", "cost"],
            )
            square = df.pivot_table(index="from", columns="to", values="cost").fillna(0)
            order = list(square.index)
            mds = MDS(n_components=2, dissimilarity="precomputed")
            embedding = mds.fit_transform((square.values + square.values.T) / 2)
            emb_min = embedding.min()
            emb_max = embedding.max()
            emb_span = emb_max - emb_min
            emb_max += emb_span / 2
            emb_min -= emb_span / 2
            emb_df = pd.DataFrame(embedding, index=order, columns=["x", "y"])

            network_elements = []
            for i, row in emb_df.iterrows():
                network_elements.append(
                    {
                        "data": {
                            "id": i,
                            "label": i,
                            "url": f"/assets/results/{study}/{system}/png/{i}.png",
                        },
                        "position": {c: row[c] * 1000 / emb_span for c in ["x", "y"]},
                        "classes": "regular",
                    }
                )

            square = square.values
            n = len(square)
            result = np.zeros((n, n))
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    has_k = False
                    direct = square[i, j]
                    for k in range(n):
                        if k == i or k == j:
                            continue
                        via_k = square[i, k] + square[k, j]
                        if (via_k - direct) / direct < 0.05:
                            has_k = True
                            break
                    if not has_k:
                        result[i, j] = direct
            for i in range(n):
                for j in range(n):
                    if i == j:  # no self edges
                        continue
                    if result[i, j] == 0:  # no zero edges
                        continue
                    if result[j, i] == 0:  # no edge without other direction
                        continue
                    if result[i, j] > result[j, i] or (
                        result[i, j] == result[j, i] and i > j  # only one bidir edge
                    ):
                        network_elements.append(
                            {
                                "data": {
                                    "source": order[i],
                                    "target": order[j],
                                    "id": order[i] + "__" + order[j],
                                    "length": result[i, j],
                                },
                                "classes": "regular"
                                + (" bidir" if result[i, j] == result[j, i] else ""),
                            }
                        )
            results[study][system] = dict(df=df, network_elements=network_elements)
    return results


results = precompute()
default_study = list(results.keys())[0]
default_system = list(results[default_study].keys())[0]


app = Dash(__name__, title="NotaScope", suppress_callback_exceptions=True)


def cytoscape(id, elements):
    return cyto.Cytoscape(
        id=id,
        className="network",
        layout={"name": "preset"},
        minZoom=0.3,
        maxZoom=2,
        elements=elements,
        stylesheet=[
            {
                "selector": "node",
                "style": {
                    "width": 50,
                    "height": 50,
                    "shape": "rectangle",
                    "background-fit": "cover",
                    "background-image": "data(url)",
                    "label": "data(label)",
                    "border-color": "grey",
                    "border-width": 1,
                },
            },
            {
                "selector": "edge",
                "style": {
                    "line-color": "grey",
                    "target-arrow-color": "grey",
                    "target-arrow-shape": "triangle",
                    "curve-style": "straight",
                    "label": "data(length)",
                },
            },
            {
                "selector": ".bidir",
                "style": {
                    "source-arrow-color": "grey",
                    "source-arrow-shape": "triangle",
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
        ],
    )


def parse_hashpath(hashpath):
    m = re.match(r"#/(.*)/(.*)/(.*)/(.*)/(.*)", hashpath)
    if m:
        return m.group(1), m.group(2), m.group(3) or None, m.group(4), m.group(5)
    return default_study, default_system, None, "", ""


app.layout = html.Div([html.Div(id="content"), dcc.Location(id="location")])


@app.callback(
    Output("content", "children"),
    Input("location", "hash"),
)
def make_content(hashpath):
    study, system, system2, from_slug, to_slug = parse_hashpath(hashpath)
    cmp, net = make_comparison(study, system, from_slug, to_slug)
    if system2:
        style = dict()
        style2 = dict(gridColumnStart=2, visibility="visible")
        cmp2, net2 = make_comparison(study, system2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(visibility="hidden", gridRowStart=3)
        cmp2, net2 = None, []

    return html.Div(
        className="wrapper",
        children=[
            html.Div(
                [
                    dcc.Dropdown(
                        id="study",
                        value=study,
                        options=[s for s in results],
                        clearable=False,
                        className="dropdown",
                    ),
                ],
                style=dict(position="absolute", left=10, top=10),
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="system",
                        value=system,
                        options=[s for s in results[study]],
                        clearable=False,
                        className="dropdown",
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="system2",
                        value=system2,
                        options=[s for s in results[study]],
                        clearable=True,
                        className="dropdown",
                    ),
                ]
            ),
            html.Div([cytoscape("network", net)], style=style),
            html.Div([cytoscape("network2", net2)], style=style2),
            html.Div(cmp, className="comparison"),
            html.Div(cmp2, className="comparison"),
            dcc.Store(id="selection", data=[from_slug, to_slug]),
        ],
    )


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
    Input("network", "tapNodeData"),
    Input("network", "tapEdgeData"),
    Input("network2", "tapNodeData"),
    Input("network2", "tapEdgeData"),
)
def update_hashpath(
    selection, study, system, system2, node_data, edge_data, node_data2, edge_data2
):
    ctx = callback_context
    from_slug, to_slug = selection
    if ctx.triggered:
        click_system = ctx.triggered[0]["prop_id"].split(".")[0]
        click_type = ctx.triggered[0]["prop_id"].split(".")[1]

        if click_type == "tapNodeData":
            if click_system == "network":
                from_slug = to_slug = node_data["id"]
            if click_system == "network2":
                from_slug = to_slug = node_data2["id"]
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
    hashpath = f"#/{study}/{system}/{system2 or ''}/{from_slug}/{to_slug}"
    return hashpath, node_data, edge_data, node_data2, edge_data2


def iframe(study, system, url):
    return html.Iframe(
        src=f"/assets/results/{study}/{system}/{url}?{random.random()}",
        style=dict(width="100%", height="300px"),
    )


def img(study, system, slug):
    return html.Img(
        src=f"/assets/results/{study}/{system}/png/{slug}.png",
        style=dict(verticalAlign="middle", maxHeight="250px", maxWidth="20vw"),
    )


def make_comparison(study, system, from_slug, to_slug):
    cmp = None
    system_results = results[study][system]
    net = json.loads(json.dumps(system_results["network_elements"]))
    try:
        # add to default outputs
        if from_slug != to_slug:
            for elem in net:
                if (
                    elem["data"]["id"] == from_slug + "__" + to_slug
                    or elem["data"]["id"] == to_slug + "__" + from_slug
                ):
                    elem["classes"] = elem["classes"].replace("regular", "selected")
                else:
                    elem["classes"] = elem["classes"].replace("selected", "regular")
            df = system_results["df"]
            row = df[(df["from"] == from_slug) & (df["to"] == to_slug)]
            cost = row["cost"].values[0]
            row = df[(df["from"] == to_slug) & (df["to"] == from_slug)]
            rev_cost = row["cost"].values[0]
            cmp = [
                html.H3(
                    (f"{from_slug} ➞ {to_slug} = {cost}")
                    + (f" ({rev_cost})" if rev_cost != cost else "")
                ),
                html.Div(
                    [
                        img(study, system, from_slug),
                        html.Span("➞", style=dict(margin="20px")),
                        img(study, system, to_slug),
                    ],
                    style=dict(height="250px"),
                ),
                iframe(study, system, f"html/{from_slug}__{to_slug}.html"),
                iframe(study, system, f"cost/{from_slug}__{to_slug}.txt"),
            ]
        elif from_slug != "":
            for elem in net:
                if elem["data"]["id"] == from_slug:
                    elem["classes"] = elem["classes"].replace("regular", "selected")
                else:
                    elem["classes"] = elem["classes"].replace("selected", "regular")
            cmp = [
                html.H3(from_slug),
                html.Div([img(study, system, from_slug)], style=dict(height="250px")),
                iframe(study, system, f"source/{from_slug}.txt"),
            ]

    except Exception as e:
        print(repr(e))

    return (cmp, net)


if __name__ == "__main__":
    app.run_server(debug=True)
