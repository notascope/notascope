import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.histogram(df, x="Major Genre").update_xaxes(categoryorder="total descending")
fig
