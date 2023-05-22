import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()

df2["y"] = 1

p = figure()

p.vbar(
    x="Release Date",
    top="y",
    width=0.5,
    color=linear_cmap(
        "Worldwide Gross",
        "Viridis256",
        df2["Worldwide Gross"].min(),
        df2["Worldwide Gross"].max(),
    ),
    source=df2,
)
