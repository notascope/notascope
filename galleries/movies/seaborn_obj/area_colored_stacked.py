import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby(["Release Date", "MPAA Rating"])["Worldwide Gross"].sum().reset_index()
df2["Worldwide Gross"] /= df2.groupby("Release Date")["Worldwide Gross"].transform(
    "sum"
)

p = so.Plot(df2, x="Release Date", y="Worldwide Gross", color="MPAA Rating").add(
    so.Area(), so.Stack()
)
