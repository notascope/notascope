import pandas as pd
import seaborn.objects as so

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year

p = so.Plot(df, x="Release Date", y="Worldwide Gross").add(so.Bar(), so.Agg("sum"))
