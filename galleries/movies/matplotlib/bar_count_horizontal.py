import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["Major Genre"].value_counts()

fig, ax = plt.subplots()
ax.barh(df2.index, df2)

ax.set_ylabel("Count")
