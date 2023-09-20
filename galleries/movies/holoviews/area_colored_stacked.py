import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

df["Release Date"] = df["Release Date"].dt.year
df2 = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
).fillna(0)
df2 = df2.div(df2.sum(axis=1), axis=0)
df2 = df2.reset_index().melt(id_vars="Release Date", value_name="Worldwide Gross")
p = hv.Area.stack(
    hv.Dataset(df2, ["Release Date", "MPAA Rating"], "Worldwide Gross")
    .to(hv.Area)
    .overlay()
)
p
