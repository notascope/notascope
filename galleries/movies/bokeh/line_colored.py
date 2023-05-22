import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Category10_8

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
)

p = figure()
for i, col in enumerate(df2.columns):
    p.line(df2.index, df2[col], line_width=2, legend_label=col, color=Category10_8[i])
