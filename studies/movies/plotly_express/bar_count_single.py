import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.histogram(df, y=px.Constant(1), color="MPAA Rating")
fig
