import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Category10_8
import numpy as np
from bokeh.layouts import gridplot


df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")

categories = df["MPAA Rating"].unique()

bin_edges = np.linspace(
    df["Production Budget"].min(), df["Production Budget"].max(), 50
)

plots = []
y_max = 0
for label, df_facet in df.groupby("Major Genre"):

    df2 = pd.DataFrame({"bins": bin_edges[:-1]})
    for i, category in enumerate(categories):
        hist, _ = np.histogram(
            df_facet[df_facet["MPAA Rating"] == category]["Production Budget"].dropna(),
            bins=bin_edges,
        )
        df2[category] = hist
    y_max = max([y_max, df2.drop("bins", axis=1).sum(axis=1).max()])

    p = figure(title=label)

    p.vbar_stack(
        stackers=categories.tolist(),
        x="bins",
        source=df2,
        width=np.diff(bin_edges)[0],
        color=Category10_8,
    )
    plots.append(p)
for p in plots:
    p.y_range.end = y_max

p = gridplot(plots, ncols=5, width=200, height=200)
