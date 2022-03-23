import plotly.express as px

df = px.data.tips()

fig = px.line(df, x="tip", y="tip", color="time")
fig
