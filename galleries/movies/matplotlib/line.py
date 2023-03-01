import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()

fig, ax = plt.subplots()

ax.plot(df2["Release Date"], df2["Worldwide Gross"])

ax.set_xlabel("Release Date")
ax.set_ylabel("Worldwide Gross")
