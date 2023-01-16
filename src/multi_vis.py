from dash import dcc
from .tokens import load_tokens
import plotly.express as px


def tokens(gallery, distance, vis):
    tokens_df = load_tokens()

    gallery = "movies"

    df = (
        tokens_df.query(f"gallery == '{gallery}'")
        .groupby(["token", "notation"])["slug"]
        .nunique()
        .reset_index()
    )
    fig = px.ecdf(
        df,
        x="slug",
        color="notation",
        hover_name="token",
        ecdfnorm=None,
        height=600,
        markers=True,
        lines=True,
        # ecdfmode="complementary",
        labels=dict(slug="token frequency"),
    )
    fig.update_traces(line_shape="linear", marker_size=5, line_width=1)
    fig.update_yaxes(title_text="token frequency rank")
    fig.update_layout(scattermode="group")
    return fig


multi_vis_map = {
    "tokens": tokens,
}
multi_vis_types = list(multi_vis_map)


def wrap_multi_vis(gallery, distance, vis):
    fig = multi_vis_map[vis](gallery, distance, vis)
    return dcc.Graph(
        id=dict(type="figure", suffix="multi", seq="1"),
        figure=fig,
        style=dict(width=str(fig.layout.width or "800") + "px", margin="0 auto"),
        clear_on_unhover=True,
    )
