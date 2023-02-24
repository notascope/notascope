import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year

p = so.Plot(df, x="Release Date", y="Worldwide Gross", color="MPAA Rating").add(
    so.Area(), so.Agg("sum"), so.Norm("sum", by=["x"]), so.Stack()
)
