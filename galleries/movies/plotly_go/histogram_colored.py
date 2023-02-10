import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
fig = go.Figure()
for label, group in df.groupby("MPAA Rating"):
    fig.add_trace(
        go.Histogram(name=label, x=group["Production Budget"], histfunc="sum")
    )
fig.update_layout(barmode="stack")
