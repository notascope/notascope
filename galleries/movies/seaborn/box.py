import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.boxplot(data=df, x="Major Genre", y="Production Budget")
