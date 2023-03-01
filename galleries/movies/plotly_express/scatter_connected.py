import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = df.groupby(df["Release Date"].dt.year).sum(numeric_only=True)
fig = px.line(df2, x="Production Budget", y="Worldwide Gross", markers=True)
fig
