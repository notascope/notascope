import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = df["Major Genre"].value_counts(sort=True).plot.bar()
