import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(["Major Genre", "MPAA Rating"])["Production Budget"].mean().reset_index()
)
fig = px.line(df2, x="Major Genre", y="Production Budget", color="MPAA Rating")
fig
