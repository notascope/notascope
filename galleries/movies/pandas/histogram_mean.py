import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(pd.cut(df["Production Budget"], bins=30))["Worldwide Gross"]
    .mean()
    .fillna(0)
)
bins = [df2.index[0].left] + [x.right for x in df2.index]

fig, ax = plt.subplots()

ax.hist(bins[:-1], bins, weights=df2)

ax.set_xlabel("Production Budget")
ax.set_ylabel("Mean Worldwide Gross")
