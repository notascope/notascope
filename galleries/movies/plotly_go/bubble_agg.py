import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("MPAA Rating").mean()
fig = go.Figure()
for label, group in df2.iterrows():
    fig.add_trace(
        go.Scatter(
            name=label,
            x=[group["Production Budget"]],
            y=[group["Worldwide Gross"]],
            marker_size=[group["IMDB Rating"]],
            mode="markers",
        )
    )
