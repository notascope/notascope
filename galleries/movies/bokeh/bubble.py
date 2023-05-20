import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
from bokeh.palettes import Spectral6

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df["IMDB Rating"] = df["IMDB Rating"].fillna(0)
source = ColumnDataSource(df)

p = figure()

p.circle(
    x="Production Budget",
    y="Worldwide Gross",
    size="IMDB Rating",
    fill_color=factor_cmap(
        "MPAA Rating", palette=Spectral6, factors=df["MPAA Rating"].unique()
    ),
    legend_field="MPAA Rating",
    source=source,
)
