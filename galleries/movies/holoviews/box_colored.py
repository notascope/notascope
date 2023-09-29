import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")

p = hv.BoxWhisker(df, ["Major Genre", "MPAA Rating"], "Production Budget").opts(
    box_fill_color=hv.dim("MPAA Rating").str(), cmap="Set1"
)

p
