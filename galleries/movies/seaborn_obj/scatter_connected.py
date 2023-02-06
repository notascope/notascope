import pandas as pd
import seaborn.objects as so

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year

df2 = df.groupby("Release Date").sum().reset_index()


p = (
    so.Plot(df2, x="Production Budget", y="Worldwide Gross")
    .add(so.Dot())
    .add(so.Path())
)
