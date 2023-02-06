import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = df["MPAA Rating"].value_counts()

fig, p = plt.subplots()

p.pie(df2, labels=df2.index)
