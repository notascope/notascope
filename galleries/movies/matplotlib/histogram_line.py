import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["Production Budget"].value_counts(bins=10)

fig, ax = plt.subplots()

ax.plot(df2.index.mid, df2)

ax.set_xlabel("Production Budget")
ax.set_ylabel("Count")
