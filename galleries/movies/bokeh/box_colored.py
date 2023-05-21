import pandas as pd
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.transform import dodge
from bokeh.palettes import Category10

df = pd.read_csv("data/movies.csv")


df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")
y_min = df["Production Budget"].min()
y_max = df["Production Budget"].max()

group_values = df["MPAA Rating"].unique()
width = 0.8 / len(group_values)
color_mapper = factor_cmap("MPAA Rating", palette=Category10[8], factors=group_values)

plots = []

p = figure(x_range=df["Major Genre"].unique(), y_range=[y_min, y_max])
for i, value in enumerate(df["MPAA Rating"].unique()):
    df_facet = df[df["MPAA Rating"] == value]
    grouped = df_facet.groupby("Major Genre")["Production Budget"]
    categories = list(grouped.groups.keys())

    q1 = grouped.quantile(q=0.25)
    q2 = grouped.quantile(q=0.5)
    q3 = grouped.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    source = ColumnDataSource(
        pd.DataFrame(
            dict(cat=categories, q1=q1, q2=q2, q3=q3, upper=upper, lower=lower)
        )
    )
    dodger = dodge("Major Genre", width * i - 0.5, range=p.x_range)

    p.segment(dodger, "upper", dodger, "q3", source=source, line_color="black")
    p.segment(dodger, "lower", dodger, "q1", source=source, line_color="black")

    p.vbar(
        x=dodger,
        width=width,
        top="q3",
        bottom="q2",
        source=source,
        fill_color=Category10[8][i],
        line_color="black",
    )
    p.vbar(
        x=dodger,
        width=width,
        top="q2",
        bottom="q1",
        source=source,
        fill_color=Category10[8][i],
        line_color="black",
    )
