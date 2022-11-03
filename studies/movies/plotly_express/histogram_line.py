import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv")
counts = df["Production Budget"].value_counts(bins=10).reset_index()
counts["index"] = counts["index"].apply(lambda x: x.mid)
counts.columns = ["Production Budget", "count"]
fig = px.line(counts, x="Production Budget", y="count")
fig
