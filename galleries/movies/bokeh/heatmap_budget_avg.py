import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(["MPAA Rating", "Major Genre"])["Production Budget"].mean().reset_index()
)

p = figure(y_range=df2["MPAA Rating"].unique(), x_range=df2["Major Genre"].unique())
p.rect(
    x="Major Genre",
    y="MPAA Rating",
    width=1,
    height=1,
    source=df2,
    color=linear_cmap(
        "Production Budget",
        "Viridis256",
        df2["Production Budget"].min(),
        df2["Production Budget"].max(),
    ),
)
