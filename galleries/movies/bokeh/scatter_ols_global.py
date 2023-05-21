import pandas as pd
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
import numpy as np

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")
df2 = df[["Production Budget", "Worldwide Gross"]].dropna()
x = df2["Production Budget"]
y = df2["Worldwide Gross"]
b, a = np.polyfit(x, y, deg=1)
xseq = np.array([x.min(), x.max()])

p = figure()

p.circle(
    x="Production Budget",
    y="Worldwide Gross",
    source=df,
    color=factor_cmap("MPAA Rating", "Category10_10", df["MPAA Rating"].unique()),
)
p.line(xseq, a + b * xseq, color="black")
