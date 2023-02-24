import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()

p = so.Plot(df2, x="Release Date", y=1, color="Worldwide Gross").add(so.Bar())
