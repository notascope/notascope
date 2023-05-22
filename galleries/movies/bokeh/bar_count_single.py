from bokeh.plotting import figure
from bokeh.palettes import Category10_8
import pandas as pd


df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
values = {k[0]: [v] for k, v in df[["MPAA Rating"]].value_counts().items()}
df2 = pd.DataFrame(dict(y=["count"], **values))
p = figure(y_range=["count"])
p.hbar_stack(list(values.keys()), y="y", color=Category10_8, source=df2)
