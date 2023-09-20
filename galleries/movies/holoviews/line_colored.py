import holoviews as hv
import pandas as pd

hv.extension("bokeh")
df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = (
    df.groupby(["Release Date", "MPAA Rating"])[["Worldwide Gross"]].sum().reset_index()
)
p = (
    hv.Dataset(df2, ["Release Date", "MPAA Rating"], "Worldwide Gross")
    .to(hv.Curve)
    .overlay()
)
