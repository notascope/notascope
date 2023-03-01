import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"])[["Production Budget"]].mean()
ax = sns.displot(df2, x="Major Genre", y="MPAA Rating", weights="Production Budget")
