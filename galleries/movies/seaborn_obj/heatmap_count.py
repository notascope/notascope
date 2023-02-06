import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

p = sns.displot(df, x="Major Genre", y="MPAA Rating")
