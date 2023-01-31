import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.pivot_table(
    index="Major Genre",
    columns="MPAA Rating",
    values="Production Budget",
    aggfunc="mean",
).fillna(0)

fig, ax = plt.subplots()

for rating in df2.columns:
    ax.plot(df2.index, df2[rating], label=rating)

ax.set_xlabel("Major Genre")
ax.set_ylabel("Mean Production Budget")
