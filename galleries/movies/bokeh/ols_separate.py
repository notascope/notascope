import pandas as pd
from bokeh.plotting import figure
from bokeh.palettes import Category10_10
import numpy as np

df = pd.read_csv("data/movies.csv")
df["MPAA Rating"] = df["MPAA Rating"].fillna("Unknown")

groups = df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross"]]
p = figure()

for i, (label, df2) in enumerate(groups):
    df2 = df2.dropna()
    x = df2["Production Budget"]
    y = df2["Worldwide Gross"]
    b, a = np.polyfit(x, y, deg=1)
    xseq = np.array([x.min(), x.max()])
    p.line(xseq, a + b * xseq, color=Category10_10[i], legend_label=label)
