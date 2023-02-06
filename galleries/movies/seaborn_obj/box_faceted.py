import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

p = sns.catplot(
    df,
    kind="box",
    x="MPAA Rating",
    y="Production Budget",
    hue="MPAA Rating",
    col="Major Genre",
    col_wrap=5,
)
