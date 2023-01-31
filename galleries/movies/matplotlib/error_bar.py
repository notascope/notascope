import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby("Major Genre")["Production Budget"]
    .agg(["median", lambda g: g.quantile(0.25), lambda g: g.quantile(0.75)])
    .reset_index()
)
df2["error_x_minus"] = df2["median"] - df2["<lambda_0>"]
df2["error_x"] = df2["<lambda_1>"] - df2["median"]
fig, ax = plt.subplots()
ax.errorbar(
    df2["median"], df2.index, xerr=df2[["error_x_minus", "error_x"]].values.T, fmt="."
)

ax.set_xlabel("Average Budget")
