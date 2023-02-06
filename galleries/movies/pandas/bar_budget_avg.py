import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = df.groupby("Major Genre")["Production Budget"].mean().plot.bar()
