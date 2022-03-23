import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.histogram(df, x="lifeExp", y="pop", color="continent")
