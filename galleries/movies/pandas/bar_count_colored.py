import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = df.groupby(["Major Genre", "MPAA Rating"]).size().unstack().plot.bar(stacked=True)
