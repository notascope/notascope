import seaborn.objects as so
import pandas as pd

df = pd.read_csv("data/movies.csv")

p = so.Plot(df, x="Production Budget").add(so.Bars(), so.Hist())
