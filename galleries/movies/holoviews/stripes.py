import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()
df2["y"] = 1

p = hv.HeatMap(df2, ["Release Date", "y"], "Worldwide Gross")
p
