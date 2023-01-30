import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.pivot_table(
    index="Major Genre", columns="MPAA Rating", values="Title", aggfunc=len
)

fig, ax = plt.subplots()
bottom = 0
for label, counts in df2.items():
    ax.bar(counts.index, counts, bottom=bottom, label=label)
    bottom += counts.fillna(0)

ax.set_ylabel("Count")
