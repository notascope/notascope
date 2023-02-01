import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(["Major Genre", "MPAA Rating"])["Production Budget"].mean().reset_index()
)

ax = sns.barplot(df2, x="Major Genre", y="Production Budget", hue="MPAA Rating")
