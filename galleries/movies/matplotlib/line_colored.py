import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.pivot_table(
    index="Release Date", columns="MPAA Rating", values="Worldwide Gross", aggfunc="sum"
)

fig, ax = plt.subplots()

ax.plot(df2)
ax.legend(df2.columns)
ax.set_xlabel("Release Date")
ax.set_ylabel("Worldwide Gross")
