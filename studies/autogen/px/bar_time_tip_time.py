import plotly.express as px

df = px.data.tips()

fig = px.bar(df, x="time", y="tip", color="time")
fig
