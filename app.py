from dash import Dash, html, dcc, Input, Output, callback_context
import random
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.manifold import MDS
import os
import dash_cytoscape as cyto


np.random.seed(1)

results = dict()
for s in [d for d in os.listdir("./results") if os.path.isdir("./results/" + d)]:
    df = pd.read_csv(f"results/{s}/costs.csv", names=["system", "from", "to", "cost"])
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

    square = np.maximum(square.values, square.values.T)
    edges = []
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
                edges.append((i, j, direct))

    results[s] = dict(
        df=df,
        emb_df=emb_df,
        emb_min=emb_min,
        emb_max=emb_max,
        order=order,
        edges=edges,
        emb_span=emb_span,
    )


app = Dash(__name__, title="NotaScope")


app.layout = html.Div(
    [
        dcc.Dropdown(
            id="system",
            value=s,
            options=[{"label": s, "value": s} for s in results],
            style=dict(width="200px", margin="0 auto"),
            clearable=False,
        ),
        cyto.Cytoscape(
            id="network",
            layout={"name": "preset"},
            minZoom=0.3,
            maxZoom=2,
            style=dict(height="700px", width="700px", float="left"),
        ),
        html.Div(
            id="comparison",
            style=dict(textAlign="center", width="calc(100% - 750px)", float="right"),
        ),
        dcc.Store(id="selection", data=["", ""]),
    ],
)


@app.callback(
    Output("selection", "data"),
    Output("network", "tapNodeData"),
    Output("network", "tapEdgeData"),
    Input("network", "tapNodeData"),
    Input("network", "tapEdgeData"),
)
def display_click_data(node_data, edge_data):
    ctx = callback_context

    from_slug = to_slug = ""
    if ctx.triggered:
        click_type = ctx.triggered[0]["prop_id"].split(".")[1]

        if click_type == "tapNodeData":
            from_slug = to_slug = node_data["id"]
            edge_data = None
        if click_type == "tapEdgeData":
            from_slug = edge_data["source"]
            to_slug = edge_data["target"]
            node_data = None

    return [from_slug, to_slug], node_data, edge_data


@app.callback(
    Output("comparison", "children"),
    Output("network", "elements"),
    Input("system", "value"),
    Input("selection", "data"),
)
def display_click_data(system, selection_data):
    from_slug, to_slug = selection_data
    order = results[system]["order"]
    # default outputs
    comparison_tree = None
    network_elements = []
    emb_span = results[system]["emb_span"]
    for i, row in results[system]["emb_df"].iterrows():
        network_elements.append(
            {
                "data": {"id": i, "label": i},
                "position": {x: row[x] * 1000 / emb_span for x in ["x", "y"]},
            }
        )
    for i, j, _ in results[system]["edges"]:
        network_elements.append(
            {
                "data": {
                    "source": order[i],
                    "target": order[j],
                    "id": order[i] + "__" + order[j],
                }
            }
        )

    # add to default outputs
    if from_slug != to_slug:
        try:
            df = results[system]["df"]
            row = df[(df["from"] == from_slug) & (df["to"] == to_slug)]
            cost = row["cost"].values[0]
            comparison_tree = [
                html.H3("%s ➞ %s = %.1f" % (from_slug, to_slug, cost)),
                html.Img(
                    src=f"/assets/results/{system}/png/" + from_slug + ".png",
                    style=dict(verticalAlign="middle", maxHeight="250px"),
                ),
                html.Span("➞", style=dict(margin="20px")),
                html.Img(
                    src=f"/assets/results/{system}/png/" + to_slug + ".png",
                    style=dict(verticalAlign="middle", maxHeight="250px"),
                ),
                html.Iframe(
                    src=f"/assets/results/{system}/html/%s__%s.html?%f"
                    % (
                        from_slug,
                        to_slug,
                        random.random(),
                    ),
                    style=dict(width="100%", height="300px"),
                ),
                html.Iframe(
                    src=f"/assets/results/{system}/cost/%s__%s.txt?%f"
                    % (
                        from_slug,
                        to_slug,
                        random.random(),
                    ),
                    style=dict(width="100%", height="300px"),
                ),
            ]

        except Exception as e:
            print(repr(e))
            comparison_tree = None
    elif from_slug != "":
        try:
            comparison_tree = [
                html.H3(from_slug),
                html.Img(
                    src=f"/assets/results/{system}/png/" + from_slug + ".png",
                    style=dict(verticalAlign="middle", maxHeight="250px"),
                ),
                html.Iframe(
                    src=f"/assets/results/{system}/source/%s.txt?%f"
                    % (from_slug, random.random()),
                    style=dict(width="100%", height="300px"),
                ),
            ]
        except Exception as e:
            print(repr(e))
            comparison_tree = None

    return comparison_tree, network_elements


if __name__ == "__main__":
    app.run_server(debug=True)
