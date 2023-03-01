import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = df.groupby("MPAA Rating").mean(numeric_only=True)

ax = sns.relplot(
    df2,
    x="Production Budget",
    y="Worldwide Gross",
    hue="MPAA Rating",
    size="IMDB Rating",
)
