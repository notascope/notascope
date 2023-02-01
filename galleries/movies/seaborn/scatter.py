import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.scatterplot(df, x="Production Budget", y="Worldwide Gross")
