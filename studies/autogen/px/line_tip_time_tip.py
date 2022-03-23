import plotly.express as px

df = px.data.tips()

fig = px.line(df, x="tip", y="time", color="tip")
fig
