import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")

p = figure()

p.circle(
    x="Production Budget",
    y="Worldwide Gross",
    source=df,
    color=factor_cmap("MPAA Rating", "Category10_10", df["MPAA Rating"].unique()),
)
