import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")
df2 = (
    pd.read_csv("data/movies.csv")
    .groupby("Major Genre")["Production Budget"]
    .agg(["mean", "sem"])
)
p = (
    hv.Scatter(df2, "Major Genre", ("mean", "Production Budget"))
    * hv.ErrorBars(df2, "Major Genre", ["mean", "sem"])
).opts(invert_axes=True)
p
