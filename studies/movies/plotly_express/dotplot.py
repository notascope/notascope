import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv").groupby("Major Genre").size().reset_index()
fig = px.scatter(df, x=0, y="Major Genre")
fig
