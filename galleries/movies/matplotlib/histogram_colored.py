import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
groups = df.groupby("MPAA Rating")["Production Budget"]
fig, ax = plt.subplots()

ax.hist([x for _, x in groups], stacked=True, label=[label for label, _ in groups])

ax.legend()
ax.set_xlabel("Production Budget")
ax.set_ylabel("Count")
