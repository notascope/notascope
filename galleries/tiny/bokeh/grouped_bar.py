from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.transform import dodge

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

source = ColumnDataSource(plot_df)

p = figure(width=500, height=250, x_range=fruits)

p.vbar(
    x=dodge("Fruit", -0.15, range=p.x_range),
    top="Alex",
    source=source,
    width=0.2,
    color="steelblue",
    legend_label="Alex",
)
p.vbar(
    x=dodge("Fruit", 0.15, range=p.x_range),
    top="Jordan",
    source=source,
    width=0.2,
    color="orange",
    legend_label="Jordan",
)
