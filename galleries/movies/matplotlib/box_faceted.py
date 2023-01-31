import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
genres = list(df["Major Genre"].unique())
ratings = list(df["MPAA Rating"].unique())
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
width = 0.8 / len(ratings)
fig, axes = plt.subplots(
    nrows=1 + int(len(genres) / 5.0), ncols=5, sharex=True, sharey=True
)
axes_list = [item for sublist in axes for item in sublist]

for i, g in enumerate(genres):
    ax = axes_list.pop(0)
    ax.set_title(g)
    for j, r in enumerate(ratings):
        values = df[(df["MPAA Rating"] == r) & (df["Major Genre"] == g)][
            "Production Budget"
        ]
        bp = ax.boxplot(
            [values], positions=[width * j - 0.5], widths=width, patch_artist=True
        )
        for box in bp["boxes"]:
            box.set_facecolor(colors[j])
