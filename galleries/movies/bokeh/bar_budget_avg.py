from bokeh.plotting import figure
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre")["Production Budget"].mean()
p = figure(x_range=df2.index.unique().to_list())
p.vbar(x="Major Genre", top="Production Budget", width=0.8, source=df2.reset_index())
