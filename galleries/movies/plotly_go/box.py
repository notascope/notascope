import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
fig = go.Figure(go.Box(x=df["Major Genre"], y=df["Worldwide Gross"]))
fig
