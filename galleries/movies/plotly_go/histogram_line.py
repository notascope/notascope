import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
counts = df["Production Budget"].value_counts(bins=10).reset_index()
counts["index"] = counts["index"].apply(lambda x: x.mid)
counts.columns = ["Production Budget", "count"]
fig = go.Figure(go.Scatter(x=counts["Production Budget"], y=counts["count"]))
