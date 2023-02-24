import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross", "IMDB Rating"]]
    .mean()
    .reset_index()
)

ax = sns.relplot(
    df2,
    x="Production Budget",
    y="Worldwide Gross",
    hue="MPAA Rating",
    size="IMDB Rating",
)
