import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().reset_index()
df2[0] /= df2.groupby("Major Genre")[0].transform("sum")
p = so.Plot(df2, x="Major Genre", y=0, color="MPAA Rating").add(
    so.Bar(), so.Agg("sum"), so.Stack()
)
