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

plot_df = df.pivot(index="Contestant", columns="Fruit", values="Number Eaten")

contestants = list(plot_df.index)

source = ColumnDataSource(plot_df)

p = figure(width=500, height=250, x_range=contestants)

p.line(
    x="Contestant", y="Apples", source=source, color="steelblue", legend_label="Apples"
)
p.line(
    x="Contestant", y="Oranges", source=source, color="orange", legend_label="Oranges"
)
p.line(
    x="Contestant", y="Bananas", source=source, color="green", legend_label="Bananas"
)
