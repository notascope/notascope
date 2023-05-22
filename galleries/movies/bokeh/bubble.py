import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10_8

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df["IMDB Rating"] = df["IMDB Rating"].fillna(0)

p = figure()

p.circle(
    x="Production Budget",
    y="Worldwide Gross",
    size="IMDB Rating",
    fill_color=factor_cmap(
        "MPAA Rating", palette=Category10_8, factors=df["MPAA Rating"].unique()
    ),
    legend_field="MPAA Rating",
    source=df,
)
