import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio


df = pd.read_csv("data/movies.csv")

genres = list(df["Major Genre"].unique())
ratings = list(df["MPAA Rating"].unique())
colors = pio.templates["plotly"].layout.colorway
symbols = [
    "circle",
    "square",
    "diamond",
    "cross",
    "x",
    "triangle-up",
    "triangle-down",
    "triangle-left",
    "triangle-right",
    "star",
    "hexagram",
    "pentagon",
    "diamond-wide",
]
fig = go.Figure()
for i, r in enumerate(ratings):
    for j, g in enumerate(genres):
        color = pio.templates["plotly"].layout.colorway[i]

        df2 = df[(df["MPAA Rating"] == r) & (df["Major Genre"] == g)][
            ["Production Budget", "Worldwide Gross"]
        ]
        fig.add_trace(
            go.Scatter(
                x=df2["Production Budget"],
                y=df2["Worldwide Gross"],
                marker_color=colors[i],
                marker_symbol=symbols[j],
                mode="markers",
                name=f"{r}-{g}",
            )
        )

fig
