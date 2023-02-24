import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(pd.cut(df["Production Budget"], bins=30))[["Worldwide Gross"]]
    .mean()
    .fillna(0)
)
df2["Production Budget"] = [x.mid for x in df2.index]
p = so.Plot(df2, x="Production Budget", y="Worldwide Gross").add(so.Bars())
