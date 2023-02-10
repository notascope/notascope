import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio


df = pd.read_csv("data/movies.csv")

genres = list(df["Major Genre"].unique())
ratings = list(df["MPAA Rating"].unique())
colors = pio.templates["plotly"].layout.colorway
fig = make_subplots(rows=1 + int(len(genres) / 5.0), cols=5, subplot_titles=genres)

for i, g in enumerate(genres):
    for j, r in enumerate(ratings):
        df2 = df[(df["MPAA Rating"] == r) & (df["Major Genre"] == g)]
        fig.add_trace(
            go.Histogram(
                x=df2["Production Budget"],
                marker_color=colors[j],
                name=r,
                showlegend=i == 1,
            ),
            row=1 + (i // 5),
            col=1 + (i % 5),
        )
fig.update_layout(barmode="stack")
fig
