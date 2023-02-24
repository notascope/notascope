import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")

p = (
    so.Plot(df, x="Production Budget", color="MPAA Rating")
    .facet(col="Major Genre", wrap=5)
    .add(so.Bars(), so.Hist(), so.Stack())
)
