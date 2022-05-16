import plotly.express as px

df = px.data.tips()

fig = px.bar(df, x="time", y="time", color="time")
fig
