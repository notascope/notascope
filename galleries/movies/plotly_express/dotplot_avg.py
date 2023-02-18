import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre")["Production Budget"].mean().reset_index()
fig = px.scatter(df2, x="Production Budget", y="Major Genre")
fig
