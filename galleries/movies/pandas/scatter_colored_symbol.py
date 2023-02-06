import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")

genres = list(df["Major Genre"].unique())
ratings = list(df["MPAA Rating"].unique())
colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
symbols = [".", ",", "o", "v", "<", ">", "^", "p", "P", "1", "2", "3", "4"]
fig, ax = plt.subplots()

for i, r in enumerate(ratings):
    for j, g in enumerate(genres):
        df2 = df[(df["MPAA Rating"] == r) & (df["Major Genre"] == g)][
            ["Production Budget", "Worldwide Gross"]
        ]
        ax.scatter(
            df2["Production Budget"],
            df2["Worldwide Gross"],
            label=f"{r}-{g}",
            c=colors[i],
            marker=symbols[j],
        )
ax.set_xlabel("Production Budget")
ax.set_ylabel("Worldwide Gross")
