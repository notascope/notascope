import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")

p = so.Plot(df, y=1, color="MPAA Rating").add(
    so.Bar(), so.Count(), so.Stack(), orient="h"
)
