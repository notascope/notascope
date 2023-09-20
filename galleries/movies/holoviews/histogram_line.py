import holoviews as hv
import pandas as pd
import numpy as np

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")
hist, edges = np.histogram(df["Production Budget"].dropna(), bins="auto")
p = hv.Curve((edges, hist))
p
