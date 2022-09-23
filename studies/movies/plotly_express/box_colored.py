import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.box(df, x="Major Genre", y="Production Budget", color="MPAA Rating")
fig
