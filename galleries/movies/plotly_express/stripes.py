import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()
fig = px.bar(df2, x="Release Date", y=px.Constant(1), color="Worldwide Gross")
fig
