import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = df.plot.scatter(x="Production Budget", y="Worldwide Gross")
