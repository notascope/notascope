import pandas as pd
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")
df2 = (
    pd.read_csv("data/movies.csv")
    .groupby("Major Genre")["Production Budget"]
    .agg(["mean", "sem"])
)

p = figure(y_range=df2.index.to_list())

p.segment(
    x0=df2["mean"] - df2["sem"], x1=df2["mean"] + df2["sem"], y0=df2.index, y1=df2.index
)
p.circle(x=df2["mean"], y=df2.index)
