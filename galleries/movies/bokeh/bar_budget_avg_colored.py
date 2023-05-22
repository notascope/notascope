from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.palettes import Category10_8
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.pivot_table(
    index="Major Genre",
    columns="MPAA Rating",
    values="Production Budget",
    aggfunc="mean",
)
width = 0.8 / len(df2.columns)

p = figure(x_range=df2.index.unique().to_list())
for i, (label, counts) in enumerate(df2.items()):
    p.vbar(
        x=dodge("Major Genre", width * i - 0.5, range=p.x_range),
        top=label,
        color=Category10_8[i],
        width=width,
        source=df2.reset_index(),
    )
