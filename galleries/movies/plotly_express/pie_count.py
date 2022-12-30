import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.pie(df, names="MPAA Rating")
fig
