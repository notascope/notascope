import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("MPAA Rating").size().reset_index()
df2["y"] = 1
ax = sns.histplot(df2, y="y", weights=0, multiple="stack", hue="MPAA Rating")
