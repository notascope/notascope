import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("MPAA Rating")["MPAA Rating"].count()
fig = go.Figure()
for label, count in df2.items():
    fig.add_trace(go.Bar(name=label, y=[1], x=[count], orientation="h"))
fig.update_layout(barmode="stack")
