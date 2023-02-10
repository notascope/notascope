import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df = df.groupby("Release Date").sum().reset_index()
fig = go.Figure(
    go.Scatter(x=df["Production Budget"], y=df["Worldwide Gross"], mode="lines+markers")
)
fig
