import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = df.groupby(df["Release Date"].dt.year)["Worldwide Gross"].sum().reset_index()
fig = px.line(df2, x="Release Date", y="Worldwide Gross")
fig
