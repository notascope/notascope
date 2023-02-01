import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["MPAA Rating"].value_counts()

fig, ax = plt.subplots()

ax.pie(df2, labels=df2.index)
