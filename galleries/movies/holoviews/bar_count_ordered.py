import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")

p = (
    hv.Bars(df, "Major Genre", "Production Budget")
    .aggregate(function="count")
    .sort("Production Budget", reverse=True)
)
p
