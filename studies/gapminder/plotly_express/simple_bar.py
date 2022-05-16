import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.bar(df, x="lifeExp")
