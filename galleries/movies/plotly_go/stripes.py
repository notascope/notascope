import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df = df.groupby("Release Date").sum("Worldwide Gross").reset_index()
df["y"] = 1
fig = go.Figure(
    go.Bar(x=df["Release Date"], y=df["y"], marker_color=df["Worldwide Gross"])
)
fig
