import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import linear_cmap

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["MPAA Rating", "Major Genre"]).size().reset_index()
df2.columns = ["MPAA Rating", "Major Genre", "count"]

p = figure(y_range=df2["MPAA Rating"].unique(), x_range=df2["Major Genre"].unique())
p.rect(
    x="Major Genre",
    y="MPAA Rating",
    width=1,
    height=1,
    source=df2,
    color=linear_cmap("count", "Viridis256", df2["count"].min(), df2["count"].max()),
)
