import plotly.express as px

df = px.data.tips()

fig = px.scatter(df, x="tip", y="tip", color="time")
fig
