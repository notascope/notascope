import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import viridis
import numpy as np
from bokeh.layouts import gridplot


df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("NaN")
df["Major Genre"] = df["Major Genre"].fillna("NaN")

categories = df["MPAA Rating"].unique()

bin_num = 50
bin_edges = np.linspace(
    df["Production Budget"].min(), df["Production Budget"].max(), bin_num
)

plots = []
y_max = 0
for value in df["Major Genre"].unique():
    df_facet = df[df["Major Genre"] == value]

    df2 = pd.DataFrame({"bins": bin_edges[:-1]})
    for i, category in enumerate(categories):
        hist, _ = np.histogram(
            df_facet[df_facet["MPAA Rating"] == category]["Production Budget"].dropna(),
            bins=bin_edges,
        )
        df2[category] = hist
    y_max = max([y_max, df2.drop("bins", axis=1).sum(axis=1).max()])
    source = ColumnDataSource(df2)

    palette = viridis(len(categories))

    p = figure()

    p.vbar_stack(
        stackers=categories.tolist(),
        x="bins",
        source=source,
        width=np.diff(bin_edges)[0],
        color=palette,
        alpha=0.7,
    )
    plots.append(p)
for p in plots:
    p.y_range.end = y_max

p = gridplot(plots, ncols=5, width=200, height=200)
