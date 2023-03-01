import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()
fig = go.Figure(go.Scatter(x=df["Release Date"], y=df["Worldwide Gross"]))
fig
