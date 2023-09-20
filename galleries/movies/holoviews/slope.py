import holoviews as hv
import pandas as pd

hv.extension("bokeh")

df = pd.read_csv("data/movies.csv")

p = (
    hv.Dataset(
        df.pivot_table(
            index="Major Genre",
            columns="MPAA Rating",
            values="Production Budget",
            aggfunc="mean",
        )
        .fillna(0)
        .reset_index()
        .melt(id_vars="Major Genre", value_name="Production Budget"),
        ["Major Genre", "MPAA Rating"],
        "Production Budget",
    )
    .to(hv.Curve)
    .overlay()
)
p
