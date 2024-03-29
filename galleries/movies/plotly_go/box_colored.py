import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
fig = go.Figure()
for label, group in df.groupby("MPAA Rating"):
    fig.add_trace(
        go.Box(name=label, x=group["Major Genre"], y=group["Production Budget"])
    )
fig.update_layout(boxmode="group")
