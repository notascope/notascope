import plotly.express as px

df = px.data.tips()

fig = px.box(df, x="total_bill", color="day", facet_col="time")
fig
