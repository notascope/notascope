from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
import pandas as pd


df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().unstack().fillna(0)
p = figure(x_range=df2.index.to_list())

p.vbar_stack(
    df2.columns,
    x="Major Genre",
    width=0.9,
    color=Category10[8][:7],
    source=ColumnDataSource(df2),
)
