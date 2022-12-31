import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df = df.groupby("Release Date").sum("Worldwide Gross").reset_index()
fig = px.line(df, x="Release Date", y="Worldwide Gross")
fig