import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre")["Production Budget"].agg(["mean", "sem"]).reset_index()
fig = px.scatter(df2, x="mean", y="Major Genre", error_x="sem")
fig
