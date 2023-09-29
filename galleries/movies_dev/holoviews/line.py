import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

df["Release Date"] = df["Release Date"].dt.year


p = (
    hv.Curve(df, "Release Date", "Worldwide Gross")
    .sort("Release Date")
    .aggregate(function="sum")
)
p
