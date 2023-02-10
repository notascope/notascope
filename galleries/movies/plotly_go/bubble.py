import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
groups = df.fillna({"IMDB Rating": 0}).groupby("MPAA Rating")
fig = go.Figure()
for label, group in groups:
    fig.add_trace(
        go.Scatter(
            name=label,
            x=group["Production Budget"],
            y=group["Worldwide Gross"],
            marker_size=group["IMDB Rating"],
            mode="markers",
        )
    )

fig
