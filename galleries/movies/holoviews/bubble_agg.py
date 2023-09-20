import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross", "IMDB Rating"]]
    .mean()
    .reset_index()
)
p = (
    hv.Dataset(
        df2, ["Production Budget", "MPAA Rating"], ["Worldwide Gross", "IMDB Rating"]
    )
    .to(hv.Scatter)
    .opts(size=hv.dim("IMDB Rating"))
    .overlay()
)
p
