import holoviews as hv
import pandas as pd

hv.extension("matplotlib")

df = pd.read_csv("data/movies.csv")

p = (
    hv.Bars(df, ["Major Genre", "MPAA Rating"], "Production Budget")
    .aggregate(function="mean")
    .opts(multi_level=False)
)
p
