import pandas as pd
import numpy as np
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv")

hist, edges = np.histogram(df["Production Budget"].dropna(), bins="auto")

p = figure()
p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:])
