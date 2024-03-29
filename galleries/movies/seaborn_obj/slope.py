import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")

p = so.Plot(df, x="Major Genre", y="Production Budget", color="MPAA Rating").add(
    so.Line(), so.Agg()
)
