import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.histogram(df, x="Production Budget", y="Worldwide Gross", histfunc="avg")
fig
