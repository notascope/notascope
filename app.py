from dash import Dash, html, dcc, Input, Output
import random
import plotly.express as px
import pandas as pd
from sklearn.manifold import MDS


df = pd.read_csv("results/px/costs.csv", names=["from", "to", "cost"])
square = df.pivot_table(index="from", columns="to", values="cost").fillna(0)
order = square.index
mds = MDS(n_components=2, dissimilarity="precomputed")
embedding = mds.fit_transform((square.values + square.values.T) / 2)
emb_min = embedding.min() * 2
emb_max = embedding.max() * 2

app = Dash(__name__)


app.layout = html.Div(
    [
        dcc.Graph(
            id="embedding",
            figure=px.scatter(
                embedding,
                x=0,
                y=1,
                text=order,
                range_x=[emb_min, emb_max],
                range_y=[emb_min, emb_max],
            )
            .update_layout(plot_bgcolor="white")
            .update_traces(mode="text", cliponaxis=False)
            .update_xaxes(scaleanchor="y", scaleratio=1, constrain="domain", title="")
            .update_yaxes(title=""),
            style=dict(width="49%", float="right"),
        ),
        dcc.Graph(
            id="heatmap",
            figure=px.density_heatmap(
                df,
                x="from",
                y="to",
                z="cost",
                text_auto=True,
                color_continuous_scale="reds",
                category_orders={"from": order, "to": order},
            )
            .update_xaxes(side="top", scaleanchor="y", scaleratio=1, constrain="domain")
            .update_coloraxes(colorbar_title="cost"),
            style=dict(width="49%"),
        ),
        html.Iframe(
            id="diff",
            style=dict(width="100%", height="500px"),
        ),
    ],
)


@app.callback(
    Output("diff", "src"), Input("heatmap", "clickData"), prevent_initial_call=True
)
def display_click_data(clickData):
    x = clickData["points"][0]["x"]
    y = clickData["points"][0]["y"]
    if x == y:
        return ""
    return "/assets/results/px/html/%s__%s.html?%f" % (x, y, random.random())


if __name__ == "__main__":
    app.run_server(debug=True)
