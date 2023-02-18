import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
df2 = df["Production Budget"].value_counts(bins=10).reset_index()
df2["index"] = df2["index"].apply(lambda x: x.mid)
df2.columns = ["Production Budget", "count"]
fig = px.line(df2, x="Production Budget", y="count")
fig
