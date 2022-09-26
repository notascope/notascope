import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df = df.groupby(["Release Date", "MPAA Rating"]).sum("Worldwide Gross").reset_index()
fig = px.area(df, x="Release Date", y="Worldwide Gross", color="MPAA Rating")
fig
