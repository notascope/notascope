import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = (
    pd.read_csv("data/movies.csv")
    .groupby("Major Genre")["Production Budget"]
    .agg(["mean", "sem"])
    .reset_index()
)
fig, ax = plt.subplots()
ax.errorbar(df2["mean"], df2.index, xerr=df2["sem"], fmt=".")

ax.set_xlabel("Average Budget")
