from dash import Dash, html, dcc, Input, Output
import random
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.manifold import MDS
import os

np.random.seed(1)

results = dict()
for s in [d for d in os.listdir("./results")]:
    df = pd.read_csv(f"results/{s}/costs.csv", names=["from", "to", "cost"])
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
    results[s] = dict(
        df=df, emb_df=emb_df, emb_min=emb_min, emb_max=emb_max, order=order
    )


app = Dash(__name__)


app.layout = html.Div(
    [
        dcc.Dropdown(
            id="system",
            value=s,
            options=[{"label": s, "value": s} for s in results],
            style=dict(width="200px", margin="0 auto"),
            clearable=False,
        ),
        dcc.Graph(id="embedding", style=dict(width="49%", float="right")),
        dcc.Graph(id="heatmap", style=dict(width="49%")),
        html.Div(id="comparison", style=dict(textAlign="center")),
    ],
)


@app.callback(
    Output("comparison", "children"),
    Output("heatmap", "figure"),
    Output("embedding", "figure"),
    Input("system", "value"),
    Input("heatmap", "clickData"),
)
def display_click_data(system, click_data):

    # default outputs
    embedding_fig = (
        px.scatter(
            results[system]["emb_df"],
            x="x",
            y="y",
            text=results[system]["emb_df"].index,
        )
        .update_traces(mode="text", cliponaxis=False)
        .update_xaxes(scaleanchor="y", scaleratio=1, constrain="range")
    )
    heatmap_fig = (
        px.density_heatmap(
            results[system]["df"],
            y="from",
            x="to",
            z="cost",
            text_auto=True,
            color_continuous_scale="reds",
            category_orders={
                "from": results[system]["order"],
                "to": results[system]["order"],
            },
        )
        .update_xaxes(side="top", scaleanchor="y", scaleratio=1, constrain="domain")
        .update_coloraxes(colorbar_title="cost")
    )
    comparison_tree = None

    if click_data:
        from_slug = click_data["points"][0]["y"]
        to_slug = click_data["points"][0]["x"]
        cost = click_data["points"][0]["z"]
    else:
        from_slug = to_slug = ""

    # add to default outputs
    if from_slug != to_slug:
        try:
            comparison_tree = [
                html.H3("%s -> %s, cost=%.1f" % (from_slug, to_slug, cost)),
                html.Img(
                    src=f"/assets/results/{system}/png/" + from_slug + ".png",
                    height=200,
                ),
                html.Img(
                    src=f"/assets/results/{system}/png/" + to_slug + ".png", height=200
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
                    style=dict(width="100%", height="500px"),
                ),
            ]
            from_row = results[system]["emb_df"].loc[from_slug]
            to_row = results[system]["emb_df"].loc[to_slug]

            to_index = results[system]["order"].index(to_slug)
            from_index = (
                len(results[system]["order"])
                - results[system]["order"].index(from_slug)
                - 1
            )
            heatmap_fig.add_shape(
                y0=from_index - 0.5,
                y1=from_index + 0.5,
                x0=to_index - 0.5,
                x1=to_index + 0.5,
                line_color="cyan",
                line_width=5,
            )
            embedding_fig.add_annotation(
                x=to_row.x,
                y=to_row.y,
                ax=from_row.x,
                ay=from_row.y,
                arrowhead=2,
                arrowsize=2,
                standoff=10,
                startstandoff=10,
                axref="x",
                ayref="y",
            )
        except Exception as e:
            print(repr(e))
            comparison_tree = None
    return comparison_tree, heatmap_fig, embedding_fig


if __name__ == "__main__":
    app.run_server(debug=True)
