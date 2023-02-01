import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.pointplot(
    df, x="Production Budget", y="Major Genre", linestyles="", errorbar="se"
)
