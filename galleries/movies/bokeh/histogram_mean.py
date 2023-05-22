import pandas as pd
from bokeh.plotting import figure
import numpy as np

df = pd.read_csv("data/movies.csv")
df = df[["Production Budget", "Worldwide Gross"]].dropna()

bins = np.histogram_bin_edges(df["Production Budget"], bins="auto")


def mean_per_bin(bin):
    mask = (df["Production Budget"] >= bin.left) & (df["Production Budget"] < bin.right)
    return df.loc[mask, "Worldwide Gross"].mean()


df_bins = pd.IntervalIndex.from_breaks(bins)
means = df_bins.map(mean_per_bin)

df2 = pd.DataFrame(dict(x=bins[:-1], top=means))

p = figure()
p.vbar(x="x", top="top", source=df2, width=np.diff(bins)[0])
