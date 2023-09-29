import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")

p = hv.Scatter(df, "Production Budget", "Worldwide Gross")
