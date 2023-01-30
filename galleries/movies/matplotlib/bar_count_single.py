import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["Major Genre"].value_counts()

fig, ax = plt.subplots()

last_height = 0
for label, count in df2.items():
    ax.barh([0], [count], left=[last_height], label=label)
    last_height += count

ax.set_xlabel("Count")
