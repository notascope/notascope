import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")

ax = sns.displot(df, x="Major Genre", hue="MPAA Rating", multiple="fill")
