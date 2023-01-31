import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby("Release Date").sum().reset_index()

fig, ax = plt.subplots()

ax.plot(df2["Production Budget"], df2["Worldwide Gross"], "o-")
