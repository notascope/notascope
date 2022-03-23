import plotly.express as px

df = px.data.tips()

fig = px.line(df, x="time", y="tip", color="time")
fig
