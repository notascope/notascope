import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().reset_index()

ax = sns.histplot(
    df2,
    x="Major Genre",
    weights=0,
    hue="MPAA Rating",
    multiple="stack",
)
