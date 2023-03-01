import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = (
    df.groupby("Release Date")[["Worldwide Gross", "Production Budget"]]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots()

ax.plot(df2["Production Budget"], df2["Worldwide Gross"], "o-")
