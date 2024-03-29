import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.layouts import gridplot

df = pd.read_csv("data/movies.csv")


df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df["Major Genre"] = df["Major Genre"].fillna("Unknown")
y_min = df["Production Budget"].min()
y_max = df["Production Budget"].max()

group_values = df["MPAA Rating"].unique()
color_mapper = factor_cmap("MPAA Rating", palette="Category10_10", factors=group_values)

plots = []

for label, df_facet in df.groupby("Major Genre"):
    grouped = df_facet.groupby("MPAA Rating")["Production Budget"]
    categories = list(grouped.groups.keys())

    q1 = grouped.quantile(q=0.25)
    q2 = grouped.quantile(q=0.5)
    q3 = grouped.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5 * iqr
    lower = q1 - 1.5 * iqr

    source = pd.DataFrame(
        dict(cat=categories, q1=q1, q2=q2, q3=q3, upper=upper, lower=lower)
    )

    p = figure(title=label, x_range=group_values, y_range=[y_min, y_max])

    p.segment(categories, upper, categories, q3, line_color="black")
    p.segment(categories, lower, categories, q1, line_color="black")

    for top, bottom in [["q3", "q2"], ["q2", "q1"]]:
        p.vbar(
            x="cat",
            width=0.7,
            top=top,
            bottom=bottom,
            source=source,
            fill_color=color_mapper,
            line_color="black",
        )

    plots.append(p)

p = gridplot(plots, ncols=5)
