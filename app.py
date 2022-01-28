from dash import Dash, html, dcc, Input, Output
import random
import plotly.express as px
import pandas as pd

df = pd.read_csv("results/px/costs.csv", names=["from", "to", "cost"])
order = list(df["from"].unique())
app = Dash(__name__)


app.layout = html.Div(
    [
        dcc.Graph(
            id="heatmap",
            figure=px.density_heatmap(
                df,
                x="from",
                y="to",
                z="cost",
                color_continuous_scale="reds",
                category_orders={"from": order, "to": order},
            )
            .update_xaxes(side="top", scaleanchor="y", scaleratio=1, constrain="domain")
            .update_coloraxes(colorbar_title="cost"),
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
