import plotly.express as px
from .tokens import load_tokens


def token_bars(study, notation):
    tokens_df = load_tokens()

    df = tokens_df.query(f"study == '{study}' and notation== '{notation}'").groupby(["token", "notation"])["slug"].nunique().reset_index()
    return px.bar(
        df, x="slug", y=px.Constant(1), facet_col="notation", hover_name="token", height=600
    )  # .add_shape(type="line", x0=0,y0=0, x1=30, y1=30, row="all", col="all")


def token_ecdf(study, notation):

    tokens_df = load_tokens()

    df = tokens_df.query(f"study == '{study}' and notation== '{notation}'").groupby(["token", "notation"])["slug"].nunique().reset_index()
    return px.ecdf(df, color="notation", hover_name="token", ecdfnorm=None, height=800, markers=True)
