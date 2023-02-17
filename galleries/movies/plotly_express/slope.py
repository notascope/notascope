import pandas as pd
import plotly.express as px

df = (
    pd.read_csv("data/movies.csv")
    .groupby(["Major Genre", "MPAA Rating"])["Production Budget"]
    .mean()
    .reset_index()
)
fig = px.line(df, x="Major Genre", y="Production Budget", color="MPAA Rating")
fig
