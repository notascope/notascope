import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby("Release Date").sum("Worldwide Gross").reset_index()

fig, ax = plt.subplots()

ax.bar(df2["Release Date"], df2["Worldwide Gross"])

ax.set_xlabel("Release Date")
ax.set_ylabel("Worldwide Gross")
