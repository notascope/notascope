import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre").size().reset_index()
fig = px.scatter(df2, x=0, y="Major Genre")
fig
