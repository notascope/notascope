import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")

p = hv.BoxWhisker(df, "Major Genre", "Production Budget")
p
