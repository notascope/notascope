import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")

p = so.Plot(df, y="Major Genre", x="Production Budget").add(so.Dot(), so.Agg("mean"))
