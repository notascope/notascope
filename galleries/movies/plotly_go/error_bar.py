import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre")["Production Budget"].agg(["mean", "sem"]).reset_index()
fig = go.Figure(
    go.Scatter(
        x=df2["mean"], y=df2["Major Genre"], error_x_array=df2["sem"], mode="markers"
    )
)

fig
