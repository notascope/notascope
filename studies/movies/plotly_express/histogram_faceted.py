import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.histogram(df, x="Production Budget", color="MPAA Rating", facet_col="Major Genre", facet_col_wrap=5)
fig
