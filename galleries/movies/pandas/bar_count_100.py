import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().unstack()
df2 = df2.div(df2.sum(axis=1), axis=0)

ax = df2.plot.bar(stacked=True)
