import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
fig = go.Figure(
    go.Scatter(
        x=df["Production Budget"],
        y=df["Worldwide Gross"],
        marker_color=df["IMDB Rating"],
        mode="markers",
    )
)
fig
