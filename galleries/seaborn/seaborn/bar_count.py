import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.catplot(df, kind="count", x="Major Genre")
