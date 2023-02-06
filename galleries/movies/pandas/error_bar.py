import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = (
    df.groupby("Major Genre")["Production Budget"]
    .agg(["mean", "sem"])
    .reset_index()
    .plot.scatter(x="mean", y="Major Genre", xerr="sem")
)
