from bokeh.plotting import figure
from bokeh.palettes import Category10_8
import pandas as pd


df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().unstack().fillna(0)
df2 = df2.div(df2.sum(axis=1), axis=0)
p = figure(x_range=df2.index.to_list())

p.vbar_stack(df2.columns, x="Major Genre", width=0.9, color=Category10_8, source=df2)
