import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
fig = go.Figure(go.Histogram(x=df["Release Date"], y=df["Worldwide Gross"]))
