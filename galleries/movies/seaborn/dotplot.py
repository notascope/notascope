import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.pointplot(
    df,
    x=df.index,
    y="Major Genre",
    linestyles="",
    errorbar=None,
    estimator="count",
)
