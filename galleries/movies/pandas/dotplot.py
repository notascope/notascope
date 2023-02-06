import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = df.groupby("Major Genre").size().reset_index().plot.scatter(x=0, y="Major Genre")
