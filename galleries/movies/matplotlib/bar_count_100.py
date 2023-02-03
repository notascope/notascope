import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().unstack()
df2 = df2.div(df2.sum(axis=1), axis=0)

fig, ax = plt.subplots()
bottom = 0
for label, counts in df2.items():
    ax.bar(counts.index, counts, bottom=bottom, label=label)
    bottom += counts.fillna(0)

ax.set_ylabel("Count")
