import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()
ax = sns.histplot(df2, x="Release Date", y=1, weights="Worldwide Gross", bins=100)
ax.set_ylim(1, 1.01)
