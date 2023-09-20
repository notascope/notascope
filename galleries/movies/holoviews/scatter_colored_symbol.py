import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df = df[["Production Budget", "Worldwide Gross", "MPAA Rating", "Major Genre"]].dropna()

symbols = [
    "asterisk",
    "circle",
    "circle_cross",
    "circle_dot",
    "circle_x",
    "circle_y",
    "cross",
    "dash",
    "diamond",
    "diamond_cross",
    "diamond_dot",
    "dot",
    "hex",
]
df["symbol"] = df["Major Genre"].map(
    {g: symbols[i] for i, g in enumerate(df["Major Genre"].unique())}
)
p = (
    hv.Dataset(df, "Production Budget", ["Worldwide Gross", "MPAA Rating", "symbol"])
    .to(hv.Scatter)
    .opts(color=hv.dim("MPAA Rating").str(), cmap="Category10", marker="symbol")
)
p
