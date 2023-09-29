import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df = df[["Production Budget", "Worldwide Gross", "MPAA Rating"]].dropna()

p = hv.Overlay(
    [
        hv.Slope.from_scatter(p)
        for p in hv.Dataset(
            df, ["Production Budget", "MPAA Rating"], "Worldwide Gross"
        ).to(hv.Scatter)
    ]
).opts(xlim=(0, 300_000_000), ylim=(0, 1_000_000_000))
