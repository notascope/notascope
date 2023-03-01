import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
ax = sns.displot(df, y=0, multiple="stack", hue="MPAA Rating")
