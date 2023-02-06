import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
genres = list(df["Major Genre"].unique())
ratings = list(df["MPAA Rating"].unique())
fig, axes = plt.subplots(
    nrows=1 + int(len(genres) / 5.0), ncols=5, sharex=True, sharey=True
)
axes_list = [item for sublist in axes for item in sublist]

for i, g in enumerate(genres):
    ax = axes_list.pop(0)
    ax.set_title(g)
    values = [
        df[(df["MPAA Rating"] == r) & (df["Major Genre"] == g)]["Production Budget"]
        for r in ratings
    ]
    ax.hist(values, stacked=True, label=ratings if i == 0 else None)

fig.legend()
