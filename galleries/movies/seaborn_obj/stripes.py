import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = df.groupby(df["Release Date"].dt.year)["Worldwide Gross"].sum().reset_index()

p = so.Plot(df2, x="Release Date", y=1, color="Worldwide Gross").add(so.Bar())
