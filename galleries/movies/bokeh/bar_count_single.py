from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Category10
import pandas as pd


df = pd.read_csv("data/movies.csv")
values = {k[0]: [v] for k, v in df[["MPAA Rating"]].value_counts().items()}
source = ColumnDataSource(dict(y=["count"], **values))
p = figure(y_range=["count"])
p.hbar_stack(list(values.keys()), y="y", color=Category10[8][:7], source=source)
