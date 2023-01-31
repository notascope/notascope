import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
)

fig, ax = plt.subplots()

for rating in df2.columns:
    ax.plot(df2.index, df2[rating], label=rating)

ax.set_xlabel("Release Date")
ax.set_ylabel("Worldwide Gross")
