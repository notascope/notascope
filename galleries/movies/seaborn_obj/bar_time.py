import pandas as pd
import seaborn.objects as so

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
p = so.Plot(df, x="Release Date", y="Worldwide Gross").add(so.Bar(), so.Agg("sum"))
