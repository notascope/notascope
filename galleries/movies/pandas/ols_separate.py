import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("data/movies.csv")

groups = df.groupby("MPAA Rating")[["Production Budget", "Worldwide Gross"]]
fig, ax = plt.subplots()

for label, df2 in groups:
    df2 = df2.dropna()
    x = df2["Production Budget"]
    y = df2["Worldwide Gross"]
    b, a = np.polyfit(x, y, deg=1)
    xseq = np.array([x.min(), x.max()])
    ax.plot(xseq, a + b * xseq, label=label)
ax.legend()
ax.set_xlabel("Production Budget")
ax.set_ylabel("Worldwide Gross")
