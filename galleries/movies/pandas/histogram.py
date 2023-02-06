import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = df["Production Budget"].plot.hist()
