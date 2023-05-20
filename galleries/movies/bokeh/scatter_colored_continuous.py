import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

df = pd.read_csv("data/movies.csv")

p = figure()

p.circle(
    x="Production Budget",
    y="Worldwide Gross",
    source=df,
    color=linear_cmap(
        "IMDB Rating", "Viridis256", df["IMDB Rating"].min(), df["IMDB Rating"].max()
    ),
)
