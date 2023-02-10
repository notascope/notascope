import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre").median().reset_index()
fig = go.Figure(go.Scatter(x=df2[0], y=df2["Major Genre"], mode="markers"))

fig
