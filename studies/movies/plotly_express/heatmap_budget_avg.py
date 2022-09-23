import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.density_heatmap(df, x="Major Genre", z="Production Budget", y="MPAA Rating", histfunc="avg")
fig
