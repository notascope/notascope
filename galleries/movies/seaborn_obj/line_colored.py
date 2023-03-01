import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year

p = so.Plot(df, x="Release Date", y="Worldwide Gross", color="MPAA Rating").add(
    so.Line(), so.Agg("sum")
)
