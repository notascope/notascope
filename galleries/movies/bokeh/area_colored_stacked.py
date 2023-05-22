from bokeh.plotting import figure
from bokeh.palettes import Category10_8
import pandas as pd


df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df2 = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
).fillna(0)

df2 = df2.div(df2.sum(axis=1), axis=0)
p = figure()

p.varea_stack(df2.columns, x="Release Date", color=Category10_8, source=df2)
