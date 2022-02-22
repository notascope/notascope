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
    for s in [d for d in os.listdir("./results") if os.path.isdir("./results/" + d)]:
        df = pd.read_csv(
            f"results/{s}/costs.csv", names=["system", "from", "to", "cost"]
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
                        "url": f"/assets/results/{s}/png/{i}.png",
                    },
                    "position": {c: row[c] * 1000 / emb_span for c in ["x", "y"]},
                }
            )

        square = np.maximum(square.values, square.values.T)
        for i in range(len(square)):
            for j in range(len(square)):
                if i >= j:
                    continue
                has_k = False
                direct = square[i, j]
                for k in range(len(square)):
                    if k == i or k == j:
                        continue
                    via_k = square[i, k] + square[k, j]
                    if (via_k - direct) / direct < 0.05:
                        has_k = True
                        break
                if not has_k:
                    network_elements.append(
                        {
                            "data": {
                                "source": order[i],
                                "target": order[j],
                                "id": order[i] + "__" + order[j],
                            }
                        }
                    )

        results[s] = dict(df=df, network_elements=network_elements)
    return results


results = precompute()
default_system = list(results.keys())[0]


app = Dash(__name__, title="NotaScope")


def cytoscape(id):
    return cyto.Cytoscape(
        id=id,
        className="network",
        layout={"name": "preset"},
        minZoom=0.3,
        maxZoom=2,
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
            {"selector": "edge", "style": {"line-color": "grey"}},
            {
                "selector": ".selected",
                "style": {
                    "line-color": "red",
                    "border-color": "red",
                    "border-width": 5,
                },
            },
        ],
    )


app.layout = html.Div(
    className="wrapper",
    children=[
        html.Div(
            [
                dcc.Dropdown(
                    id="system",
                    value=default_system,
                    options=[{"label": s, "value": s} for s in results],
                    clearable=False,
                    className="dropdown",
                ),
            ]
        ),
        html.Div(
            [
                dcc.Dropdown(
                    id="system2",
                    options=[{"label": s, "value": s} for s in results],
                    clearable=True,
                    className="dropdown",
                ),
            ]
        ),
        html.Div([cytoscape("network")], id="network_container"),
        html.Div([cytoscape("network2")], id="network2_container"),
        html.Div(id="comparison", className="comparison"),
        html.Div(id="comparison2", className="comparison"),
        dcc.Store(id="selection", data=["", ""]),
    ],
)


@app.callback(
    Output("selection", "data"),
    Output("network", "tapNodeData"),
    Output("network", "tapEdgeData"),
    Output("network2", "tapNodeData"),
    Output("network2", "tapEdgeData"),
    Input("network", "tapNodeData"),
    Input("network", "tapEdgeData"),
    Input("network2", "tapNodeData"),
    Input("network2", "tapEdgeData"),
)
def display_click_data(node_data, edge_data, node_data2, edge_data2):
    ctx = callback_context

    from_slug = to_slug = ""
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

    return [from_slug, to_slug], node_data, edge_data, node_data2, edge_data2


def iframe(system, url):
    return html.Iframe(
        src=f"/assets/results/{system}/{url}?{random.random()}",
        style=dict(width="100%", height="300px"),
    )


def img(system, slug):
    return html.Img(
        src=f"/assets/results/{system}/png/{slug}.png",
        style=dict(verticalAlign="middle", maxHeight="250px", maxWidth="20vw"),
    )


def make_comparison(system, from_slug, to_slug):
    cmp = None
    net = json.loads(json.dumps(results[system]["network_elements"]))
    try:
        # add to default outputs
        if from_slug != to_slug:
            for elem in net:
                if elem["data"]["id"] == from_slug + "__" + to_slug:
                    elem["classes"] = "selected"
                else:
                    elem["classes"] = "unselected"
            df = results[system]["df"]
            row = df[(df["from"] == from_slug) & (df["to"] == to_slug)]
            cost = row["cost"].values[0]
            cmp = [
                html.H3(f"{from_slug} ➞ {to_slug} = {cost}"),
                html.Div(
                    [
                        img(system, from_slug),
                        html.Span("➞", style=dict(margin="20px")),
                        img(system, to_slug),
                    ],
                    style=dict(height="250px"),
                ),
                iframe(system, f"html/{from_slug}__{to_slug}.html"),
                iframe(system, f"cost/{from_slug}__{to_slug}.txt"),
            ]
        elif from_slug != "":
            for elem in net:
                if elem["data"]["id"] == from_slug:
                    elem["classes"] = "selected"
                else:
                    elem["classes"] = "unselected"
            cmp = [
                html.H3(from_slug),
                html.Div([img(system, from_slug)], style=dict(height="250px")),
                iframe(system, f"source/{from_slug}.txt"),
            ]

    except Exception as e:
        print(repr(e))

    return (cmp, net)


@app.callback(
    Output("comparison", "children"),
    Output("network", "elements"),
    Output("comparison", "style"),
    Output("network_container", "style"),
    Output("comparison2", "children"),
    Output("network2", "elements"),
    Output("comparison2", "style"),
    Output("network2_container", "style"),
    Input("system", "value"),
    Input("system2", "value"),
    Input("selection", "data"),
)
def display_click_data(system, system2, selection_data):
    from_slug, to_slug = selection_data
    cmp, net = make_comparison(system, from_slug, to_slug)
    if system2:
        style = dict()
        style2 = dict(gridColumnStart=2, visibility="visible")
        cmp2, net2 = make_comparison(system2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(visibility="hidden", gridRowStart=3)
        cmp2, net2 = None, []

    return (cmp, net, style, style, cmp2, net2, style2, style2)


if __name__ == "__main__":
    app.run_server(debug=True)
