import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("data/movies.csv")
df2 = df.pivot_table(
    index="Major Genre",
    columns="MPAA Rating",
    values="Production Budget",
    aggfunc="mean",
)

x = np.arange(len(df2))
width = 0.8 / len(df2.columns)

fig, ax = plt.subplots()

for i, (label, counts) in enumerate(df2.items()):
    ax.bar(x + width * i - 0.5, counts, width, label=label)

ax.set_xticks(x, df2.index)
ax.set_ylabel("Average Budget")
