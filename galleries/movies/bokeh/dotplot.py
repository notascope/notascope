import pandas as pd
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")
df2 = df["Major Genre"].value_counts()

p = figure(y_range=df2.index.to_list())
p.circle(df2, df2.index)
