import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.displot(
    data=df,
    x="Production Budget",
    hue="MPAA Rating",
    multiple="stack",
    col="Major Genre",
    col_wrap=5,
)
