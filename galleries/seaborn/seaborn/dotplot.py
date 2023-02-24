import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.catplot(
    df,
    kind="point",
    x="Production Budget",
    y="Major Genre",
    estimator="size",
    linestyles="",
    errorbar=None,
)
