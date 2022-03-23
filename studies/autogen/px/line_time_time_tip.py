import plotly.express as px

df = px.data.tips()

fig = px.line(df, x="time", y="time", color="tip")
fig
