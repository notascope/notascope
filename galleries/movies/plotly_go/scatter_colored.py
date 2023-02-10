import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
groups = df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross"]]
fig = go.Figure()
for label, df2 in groups:
    fig.add_trace(
        go.Scatter(
            name=label,
            x=df2["Production Budget"],
            y=df2["Worldwide Gross"],
            mode="markers",
        )
    )
fig
