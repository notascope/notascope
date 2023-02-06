import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = (
    df.groupby("Major Genre")["Production Budget"]
    .mean()
    .reset_index()
    .plot.scatter(x="Production Budget", y="Major Genre")
)
