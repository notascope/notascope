import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap, factor_mark

df = pd.read_csv("data/movies.csv")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
marker_types = [
    "asterisk",
    "circle",
    "cross",
    "diamond",
    "square",
    "triangle",
    "inverted_triangle",
    "x",
    "circle_cross",
]
markers = [
    marker_types[i % len(marker_types)] for i in range(len(df["Major Genre"].unique()))
]

p = figure()

p.scatter(
    x="Production Budget",
    y="Worldwide Gross",
    source=df,
    color=factor_cmap("MPAA Rating", "Category10_10", df["MPAA Rating"].unique()),
    marker=factor_mark("Major Genre", markers, df["Major Genre"].unique()),
)
