import plotly.express as px

df = px.data.tips()

fig = px.bar(df, x="tip", y="time", color="tip")
fig
