import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("MPAA Rating").count().reset_index()
df2["y"] = 1
ax = sns.histplot(df2, y="y", weights="Title", multiple="stack", hue="MPAA Rating")
