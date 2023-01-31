import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
groups = df.groupby("Major Genre")["Production Budget"]
fig, ax = plt.subplots()

ax.boxplot([x for _, x in groups], labels=[label for label, _ in groups])

ax.legend()
ax.set_xlabel("Major Genre")
ax.set_ylabel("Production Budget")
