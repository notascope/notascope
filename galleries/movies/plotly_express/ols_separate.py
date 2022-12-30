import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
fig = px.scatter(df, x="Production Budget", y="Worldwide Gross", color="MPAA Rating", trendline="ols")
fig.data = [t for t in fig.data if t.mode == "lines"]
fig.update_traces(showlegend=True)
fig
