import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import viridis

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
)

p = figure(
    title="Worldwide Gross over time",
    x_axis_label="Release Date",
    y_axis_label="Worldwide Gross",
)

palette = viridis(len(df2.columns))

for i, col in enumerate(df2.columns):
    p.line(df2.index, df2[col], line_width=2, legend_label=col, color=palette[i])
