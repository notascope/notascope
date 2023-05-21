import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import viridis
import numpy as np

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("NaN")

categories = df["MPAA Rating"].unique()

bin_num = 50
bin_edges = np.linspace(
    df["Production Budget"].min(), df["Production Budget"].max(), bin_num
)

df2 = pd.DataFrame({"bins": bin_edges[:-1]})
for i, category in enumerate(categories):
    hist, _ = np.histogram(
        df[df["MPAA Rating"] == category]["Production Budget"].dropna(), bins=bin_edges
    )
    df2[category] = hist

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
    legend_label=categories.tolist(),
)
