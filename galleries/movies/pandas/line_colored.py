import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
ax = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
).plot.line()
