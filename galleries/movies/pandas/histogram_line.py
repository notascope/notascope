import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["Production Budget"].value_counts(bins=10)
df2.index = df2.index.mid
ax = df2.plot.line()
