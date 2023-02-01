import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.histplot(data=df, x="Production Budget", hue="MPAA Rating", multiple="stack")
