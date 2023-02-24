import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.relplot(
    df,
    kind="line",
    x="Major Genre",
    y="Production Budget",
    hue="MPAA Rating",
    errorbar=None,
)
