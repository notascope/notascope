import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv").groupby("Major Genre").median().reset_index()
fig = px.scatter(df, x="Production Budget", y="Major Genre")
fig
