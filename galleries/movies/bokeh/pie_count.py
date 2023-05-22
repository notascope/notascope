import pandas as pd
import numpy as np
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.palettes import Category10_8

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df2 = df["MPAA Rating"].value_counts().reset_index()
df2.columns = ["MPAA Rating", "count"]

df2["angle"] = df2["count"] / df2["count"].sum() * 2 * np.pi
df2["color"] = Category10_8

p = figure()

p.wedge(
    x=0,
    y=1,
    radius=0.4,
    start_angle=cumsum("angle", include_zero=True),
    end_angle=cumsum("angle"),
    line_color="white",
    fill_color="color",
    legend_field="MPAA Rating",
    source=df2,
)

p.axis.visible = False
p.grid.grid_line_color = None
