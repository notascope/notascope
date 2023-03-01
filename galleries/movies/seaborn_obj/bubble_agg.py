import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("MPAA Rating").mean(numeric_only=True)
p = so.Plot(
    df2,
    x="Production Budget",
    y="Worldwide Gross",
    color="MPAA Rating",
    pointsize="IMDB Rating",
).add(so.Dot())
