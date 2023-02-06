import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
ax = (
    df.groupby("Release Date")
    .sum()
    .reset_index()
    .plot.line(x="Production Budget", y="Worldwide Gross", style="o-")
)
