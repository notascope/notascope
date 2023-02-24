import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")

p = (
    so.Plot(df, x="Major Genre")
    .add(so.Bar(), so.Count())
    .scale(x=so.Nominal(order=df["Major Genre"].value_counts().index))
)
