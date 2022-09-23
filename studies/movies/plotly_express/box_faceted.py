import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.box(df, facet_col="Major Genre", y="Production Budget", color="MPAA Rating", facet_col_wrap=5)
fig
