import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Category10_8


df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = df.pivot_table(
    index="Major Genre",
    columns="MPAA Rating",
    values="Production Budget",
    aggfunc="mean",
).fillna(0)
p = figure(x_range=df2.index.tolist())

for i, rating in enumerate(df2.columns):
    p.line(x=df2.index, y=df2[rating], color=Category10_8[i], legend_label=rating)
