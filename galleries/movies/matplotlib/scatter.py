import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")

fig, ax = plt.subplots()

ax.scatter(df["Production Budget"], df["Worldwide Gross"])

ax.set_xlabel("Production Budget")
ax.set_ylabel("Worldwide Gross")
