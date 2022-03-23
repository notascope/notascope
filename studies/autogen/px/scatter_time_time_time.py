import plotly.express as px

df = px.data.tips()

fig = px.scatter(df, x="time", y="time", color="time")
fig
