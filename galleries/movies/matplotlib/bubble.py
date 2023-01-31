import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")

groups = df.groupby("MPAA Rating")[
    ["Production Budget", "Worldwide Gross", "IMDB Rating"]
]
fig, ax = plt.subplots()
for label, df2 in groups:
    ax.scatter(
        df2["Production Budget"],
        df2["Worldwide Gross"],
        s=df2["IMDB Rating"] * 3,
        label=label,
    )
ax.legend()
ax.set_xlabel("Production Budget")
ax.set_ylabel("Worldwide Gross")
