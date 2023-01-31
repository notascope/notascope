import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("data/movies.csv")
fig, ax = plt.subplots()
genres = list(df["Major Genre"].unique())
ratings = list(df["MPAA Rating"].unique())
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
x = np.arange(len(genres))
width = 0.8 / len(ratings)

for i, r in enumerate(ratings):
    values = [
        df[(df["MPAA Rating"] == r) & (df["Major Genre"] == g)]["Production Budget"]
        for g in genres
    ]
    bp = ax.boxplot(
        values, positions=x + width * i - 0.5, widths=width, patch_artist=True
    )
    for box in bp["boxes"]:
        box.set_facecolor(colors[i])


ax.set_xticks(x, genres)

ax.set_xlabel("Major Genre")
ax.set_ylabel("Production Budget")
