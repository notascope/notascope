import pandas as pd
import plotly.express as px

df = (
    pd.read_csv("data/movies.csv")
    .groupby("Major Genre")["Production Budget"]
    .agg(["mean", "sem"])
    .reset_index()
)
fig = px.scatter(df, x="mean", y="Major Genre", error_x="sem")
fig
