import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()
df2["y"] = 1

fig, ax = plt.subplots()
ax.bar(
    df2["Release Date"],
    df2["y"],
    color=cm.viridis(df2["Worldwide Gross"] / df2["Worldwide Gross"].max()),
)
