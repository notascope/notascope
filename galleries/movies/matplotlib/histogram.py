import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
fig, ax = plt.subplots()

ax.hist(df["Production Budget"])

ax.set_xlabel("Production Budget")
ax.set_ylabel("Count")
