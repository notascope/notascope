from dash import Dash, html, dcc, Input, Output, callback_context
import random
import plotly.express as px
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
                    "data": {"id": i, "label": i},
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


app.layout = html.Div(
    [
        dcc.Dropdown(
            id="system",
            value=default_system,
            options=[{"label": s, "value": s} for s in results],
            style=dict(width="200px", margin="0 auto"),
            clearable=False,
        ),
        cyto.Cytoscape(
            id="network",
            layout={"name": "preset"},
            minZoom=0.3,
            maxZoom=2,
            style=dict(height="45vw", width="45vw", float="left"),
        ),
        html.Div(
            id="comparison",
            style=dict(textAlign="center", width="45vw", float="right"),
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


@app.callback(
    Output("comparison", "children"),
    Output("network", "elements"),
    Input("system", "value"),
    Input("selection", "data"),
)
def display_click_data(system, selection_data):
    from_slug, to_slug = selection_data
    # default outputs
    comparison_tree = None
    network_elements = results[system]["network_elements"]

    try:
        # add to default outputs
        if from_slug != to_slug:
            df = results[system]["df"]
            row = df[(df["from"] == from_slug) & (df["to"] == to_slug)]
            cost = row["cost"].values[0]
            comparison_tree = [
                html.H3(f"{from_slug} ➞ {to_slug} = {cost}"),
                img(system, from_slug),
                html.Span("➞", style=dict(margin="20px")),
                img(system, to_slug),
                iframe(system, f"html/{from_slug}__{to_slug}.html"),
                iframe(system, f"gumtree/{from_slug}__{to_slug}.txt"),
            ]
        elif from_slug != "":
            comparison_tree = [
                html.H3(from_slug),
                img(system, from_slug),
                iframe(system, f"source/{from_slug}.txt"),
            ]

    except Exception as e:
        print(repr(e))
        comparison_tree = None

    return comparison_tree, network_elements


if __name__ == "__main__":
    app.run_server(debug=True)
