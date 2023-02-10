import pandas as pd
import plotly.graph_objects as go
import numpy as np


df = pd.read_csv("data/movies.csv")
df2 = df[["Production Budget", "Worldwide Gross"]].dropna()
x = df2["Production Budget"]
y = df2["Worldwide Gross"]
b, a = np.polyfit(x, y, deg=1)
xseq = np.array([x.min(), x.max()])

fig = go.Figure()
groups = df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross"]]
for label, df2 in groups:
    fig.add_trace(
        go.Scatter(
            name=label,
            x=df2["Production Budget"],
            y=df2["Worldwide Gross"],
            mode="markers",
        )
    )


fig.add_trace(go.Scatter(x=xseq, y=a + b * xseq, line_color="black", showlegend=False))
fig
