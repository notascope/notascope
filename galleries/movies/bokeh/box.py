import pandas as pd
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv")

df["Major Genre"] = df["Major Genre"].fillna("Unknown")

grouped = df.groupby("Major Genre")["Production Budget"]
categories = list(grouped.groups.keys())

q1 = grouped.quantile(q=0.25)
q2 = grouped.quantile(q=0.5)
q3 = grouped.quantile(q=0.75)
iqr = q3 - q1
upper = q3 + 1.5 * iqr
lower = q1 - 1.5 * iqr

p = figure(x_range=df["Major Genre"].unique())
p.segment(categories, upper, categories, q3, line_color="black")
p.segment(categories, lower, categories, q1, line_color="black")
p.vbar(x=categories, width=0.7, top=q3, bottom=q2, line_color="black")
p.vbar(x=categories, width=0.7, top=q2, bottom=q1, line_color="black")
