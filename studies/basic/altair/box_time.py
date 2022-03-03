import altair as alt
from plotly.data import tips

chart = alt.Chart(tips()).mark_boxplot().encode(x="total_bill", color="time", y="time")
chart
