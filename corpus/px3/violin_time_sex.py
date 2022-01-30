import plotly.express as px

df = px.data.tips()

fig = px.violin(df, x="total_bill", color="sex", facet_col="time")
fig
