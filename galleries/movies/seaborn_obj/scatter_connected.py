import pandas as pd
import seaborn.objects as so

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = df.groupby(df["Release Date"].dt.year).sum(numeric_only=True)

p = (
    so.Plot(df2, x="Production Budget", y="Worldwide Gross")
    .add(so.Dot())
    .add(so.Path())
)
