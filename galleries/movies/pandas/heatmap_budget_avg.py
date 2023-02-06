import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("data/movies.csv")
df2 = df.pivot_table(
    index="MPAA Rating",
    columns="Major Genre",
    values="Production Budget",
    aggfunc="mean",
)

fig, ax = plt.subplots()

im = ax.imshow(df2)

ax.set_xticks(np.arange(len(df2.columns)), labels=df2.columns)
ax.set_yticks(np.arange(len(df2.index)), labels=df2.index)

fig.colorbar(im)
