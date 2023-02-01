import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.countplot(df, x="Major Genre")
