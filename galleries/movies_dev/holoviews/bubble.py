import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")

p = (
    hv.Dataset(
        df, ["Production Budget", "MPAA Rating"], ["Worldwide Gross", "IMDB Rating"]
    )
    .to(hv.Scatter)
    .opts(size=hv.dim("IMDB Rating"))
    .overlay()
)
p
