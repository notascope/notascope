import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(pd.cut(df["Production Budget"], bins=30))[["Worldwide Gross"]]
    .mean()
    .fillna(0)
)
df2["Production Budget"] = [x.mid for x in df2.index]


ax = sns.histplot(df2, x="Production Budget", weights="Worldwide Gross", bins=len(df2))
