import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv").groupby("MPAA Rating").mean(["Production Budget", "Worldwide Gross", "IMDB Rating"]).reset_index()
fig = px.scatter(df, x="Production Budget", y="Worldwide Gross", color="MPAA Rating", size="IMDB Rating")
fig
