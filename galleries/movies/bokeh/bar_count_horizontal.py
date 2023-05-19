from bokeh.plotting import figure
import pandas as pd


df = pd.read_csv("data/movies.csv")
df2 = df["Major Genre"].value_counts()


p = figure(y_range=df2.index.to_list())
p.hbar(y=df2.index.to_list(), right=df2, height=0.8)
