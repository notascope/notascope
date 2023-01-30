import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("Major Genre")["Production Budget"].sum()

fig, ax = plt.subplots()
ax.bar(df2.index, df2)

ax.set_ylabel("Total Budget")
