import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.histogram(df, x="Release Date", y="Worldwide Gross")
fig