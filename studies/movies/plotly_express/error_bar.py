import pandas as pd
import plotly.express as px

df = (
    pd.read_csv("data/movies.csv")
    .groupby("Major Genre")["Production Budget"]
    .agg(["median", lambda g: g.quantile(0.25), lambda g: g.quantile(0.75)])
    .reset_index()
)
df["error_x_minus"] = df["median"] - df["<lambda_0>"]
df["error_x"] = df["<lambda_1>"] - df["median"]
fig = px.scatter(df, x="median", y="Major Genre", error_x="error_x", error_x_minus="error_x_minus")
fig
