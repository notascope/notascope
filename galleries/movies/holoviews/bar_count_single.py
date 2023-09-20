import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")
df["y"] = "1"

p = (
    hv.Bars(df, ["y", "MPAA Rating"], "Production Budget")
    .aggregate(function="count")
    .opts(stacked=True, invert_axes=True)
)
p
