import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")

df2 = df.groupby("MPAA Rating")[
    ["Production Budget", "Worldwide Gross", "IMDB Rating"]
].mean()
fig, ax = plt.subplots()
for label, row in df2.iterrows():
    ax.scatter(
        row["Production Budget"],
        row["Worldwide Gross"],
        s=row["IMDB Rating"] * 3,
        label=label,
    )
ax.legend()
ax.set_xlabel("Production Budget")
ax.set_ylabel("Worldwide Gross")
