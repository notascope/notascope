from bokeh.plotting import figure
import pandas as pd


df = pd.read_csv("data/movies.csv")
df2 = df["Major Genre"].value_counts(sort=True)


p = figure(x_range=df2.index.to_list())
p.vbar(x=df2.index.to_list(), top=df2, width=0.8)
