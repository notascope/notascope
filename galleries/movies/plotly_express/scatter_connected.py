import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df = (
    df.groupby("Release Date")[["Worldwide Gross", "Production Budget"]]
    .sum()
    .reset_index()
)
fig = px.line(df, x="Production Budget", y="Worldwide Gross", markers=True)
fig
