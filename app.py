from dash import Dash, html, dcc, Input, Output
import random
import plotly.express as px
import pandas as pd
from sklearn.manifold import MDS


df = pd.read_csv("results/px/costs.csv", names=["from", "to", "cost"])
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

app = Dash(__name__)


app.layout = html.Div(
    [
        dcc.Graph(id="embedding", style=dict(width="49%", float="right")),
        dcc.Graph(id="heatmap", style=dict(width="49%")),
        html.Div(id="comparison", style=dict(textAlign="center")),
    ],
)


@app.callback(
    Output("comparison", "children"),
    Output("heatmap", "figure"),
    Output("embedding", "figure"),
    Input("heatmap", "clickData"),
)
def display_click_data(click_data):
    if click_data:
        from_slug = click_data["points"][0]["x"]
        to_slug = click_data["points"][0]["y"]
        cost = click_data["points"][0]["z"]
    else:
        from_slug = to_slug = ""
    embedding_fig = (
        px.scatter(
            emb_df,
            x="x",
            y="y",
            text=emb_df.index,
            range_x=[emb_min, emb_max],
            range_y=[emb_min, emb_max],
        )
        .update_layout(plot_bgcolor="white")
        .update_traces(mode="text", cliponaxis=False)
        .update_xaxes(scaleanchor="y", scaleratio=1, constrain="domain")
    )
    heatmap_fig = (
        px.density_heatmap(
            df,
            x="from",
            y="to",
            z="cost",
            text_auto=True,
            color_continuous_scale="reds",
            category_orders={"from": order, "to": order},
        )
        .update_xaxes(side="top", scaleanchor="y", scaleratio=1, constrain="domain")
        .update_coloraxes(colorbar_title="cost")
    )
    comparison_tree = None
    if from_slug != to_slug:
        comparison_tree = [
            html.H3("%s -> %s, cost=%.1f" % (from_slug, to_slug, cost)),
            html.Img(src="/assets/results/px/png/" + from_slug + ".png", height=200),
            html.Img(src="/assets/results/px/png/" + to_slug + ".png", height=200),
            html.Iframe(
                id="diff",
                src="/assets/results/px/html/%s__%s.html?%f"
                % (
                    from_slug,
                    to_slug,
                    random.random(),
                ),
                style=dict(width="100%", height="500px"),
            ),
        ]
        from_row = emb_df.loc[from_slug]
        to_row = emb_df.loc[to_slug]

        from_index = order.index(from_slug)
        to_index = len(order) - order.index(to_slug) - 1
        heatmap_fig.add_shape(
            x0=from_index - 0.5,
            x1=from_index + 0.5,
            y0=to_index - 0.5,
            y1=to_index + 0.5,
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
    return comparison_tree, heatmap_fig, embedding_fig


if __name__ == "__main__":
    app.run_server(debug=True)
