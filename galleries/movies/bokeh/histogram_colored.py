import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Category10_8
import numpy as np

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")

categories = df["MPAA Rating"].unique()

bin_edges = np.linspace(
    df["Production Budget"].min(), df["Production Budget"].max(), 50
)

df2 = pd.DataFrame({"bins": bin_edges[:-1]})
for i, category in enumerate(categories):
    hist, _ = np.histogram(
        df[df["MPAA Rating"] == category]["Production Budget"].dropna(), bins=bin_edges
    )
    df2[category] = hist


p = figure()

p.vbar_stack(
    stackers=categories.tolist(),
    x="bins",
    source=df2,
    width=np.diff(bin_edges)[0],
    color=Category10_8,
)
