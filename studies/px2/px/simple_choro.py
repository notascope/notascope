import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.choropleth(df, locations="iso_alpha")
