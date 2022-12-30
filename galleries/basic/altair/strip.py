import altair as alt
from plotly.data import tips

chart = (
    alt.Chart(tips(), width=400, height=30)
    .mark_circle(size=8)
    .encode(
        x=alt.X("total_bill"),
        y=alt.Y(
            "jitter:Q",
            title=None,
            axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
            scale=alt.Scale(),
        ),
    )
    .transform_calculate(
        # Generate Gaussian jitter with a Box-Muller transform
        jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
    )
)
chart
