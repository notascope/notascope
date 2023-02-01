import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.displot(data=df, x="Major Genre", y="MPAA Rating")
