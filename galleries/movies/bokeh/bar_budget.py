from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import pandas as pd


df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre")["Production Budget"].sum()

source = ColumnDataSource(df2.reset_index())

p = figure(x_range=source.data["Major Genre"])
p.vbar(x="Major Genre", top="Production Budget", width=0.8, source=source)
