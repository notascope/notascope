import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

df["Release Date"] = df["Release Date"].dt.year
df2 = df.pivot_table(
    index="Major Genre",
    columns="MPAA Rating",
    values="Production Budget",
    aggfunc="sum",
).fillna(0)
df2 = df2.div(df2.sum(axis=1), axis=0)
df2 = df2.reset_index().melt(id_vars="Major Genre", value_name="Production Budget")

p = hv.Bars(df2, ["Major Genre", "MPAA Rating"], "Production Budget").opts(stacked=True)
p
