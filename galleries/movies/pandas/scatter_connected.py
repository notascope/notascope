import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
ax = (
    df.groupby("Release Date")[["Worldwide Gross", "Production Budget"]]
    .sum()
    .reset_index()
    .plot.line(x="Production Budget", y="Worldwide Gross", style="o-")
)
