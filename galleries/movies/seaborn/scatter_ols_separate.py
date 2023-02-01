import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.lmplot(
    data=df, x="Production Budget", y="Worldwide Gross", hue="MPAA Rating", ci=None
)
