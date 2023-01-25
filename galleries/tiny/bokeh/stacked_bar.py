from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
import pandas as pd

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)

plot_df = df.pivot(index="Fruit", columns="Contestant", values="Number Eaten")

fruits = list(plot_df.index)
contestants = list(plot_df.columns)

source = ColumnDataSource(plot_df)

p = figure(width=500, height=250, x_range=fruits)
p.vbar_stack(
    contestants,
    width=0.7,
    x="Fruit",
    source=source,
    color=["steelblue", "orange"],
    legend_label=contestants,
)
