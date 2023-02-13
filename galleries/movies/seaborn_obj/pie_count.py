import pandas as pd

df = pd.read_csv("data/movies.csv")
p = df.groupby("MPAA Rating").size().plot.pie()
