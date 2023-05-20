import pandas as pd
import numpy as np
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv")

hist, edges = np.histogram(df["Production Budget"].dropna())

p = figure()
p.line(edges[:-1], hist)
