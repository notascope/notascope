import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross", "IMDB Rating"]]
    .mean()
    .reset_index()
)
fig = px.scatter(
    df2,
    x="Production Budget",
    y="Worldwide Gross",
    color="MPAA Rating",
    size="IMDB Rating",
)
fig
