import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["Major Genre"].value_counts()

fig, ax = plt.subplots()
ax.scatter(df2, df2.index)

ax.set_xlabel("Count")
