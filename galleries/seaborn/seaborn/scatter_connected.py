import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = (
    df.groupby("Release Date")[["Worldwide Gross", "Production Budget"]]
    .sum()
    .reset_index()
)

ax = sns.relplot(df2, x="Production Budget", y="Worldwide Gross")
ax.ax.plot(df2["Production Budget"], df2["Worldwide Gross"])
