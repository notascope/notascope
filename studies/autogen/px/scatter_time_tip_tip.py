import plotly.express as px

df = px.data.tips()

fig = px.scatter(df, x="time", y="tip", color="tip")
fig
