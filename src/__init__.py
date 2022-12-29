from .utils import *  # noqa
from .distances import *  # noqa
from .tokens import *  # noqa

from .scatter import get_scatter, get_scatter3d
from .dendro import get_dendro
from .network import get_network
from .distributions import token_rank, token_bars, farness

vis_types = [
    "mst",
    "spanner-1",
    "spanner-1.1",
    "spanner-1.2",
    "spanner-1.5",
    "tsne",
    "umap",
    "umap_3d",
    "dendro",
    "token_rank",
    "token_bars",
    "farness",
]


def get_vis(study, notation, distance, vis, from_slug, to_slug):
    vis_list = []
    if vis.startswith("spanner"):
        vis_list.append(get_network(study, notation, distance, from_slug, to_slug, method=vis))
    elif vis == "mst":
        vis_list.append(get_network(study, notation, distance, from_slug, to_slug, method="mst"))
    elif vis == "tsne":
        vis_list.append(get_scatter(study, notation, distance, from_slug, to_slug, method="tsne"))
    elif vis == "umap":
        vis_list.append(get_scatter(study, notation, distance, from_slug, to_slug, method="umap"))
    elif vis == "umap_3d":
        vis_list.append(get_scatter3d(study, notation, distance, from_slug, to_slug, method="umap"))
    elif vis == "dendro":
        vis_list.append(get_dendro(study, notation, distance, from_slug, to_slug))
    elif vis == "token_rank":
        vis_list.append(token_rank(study, notation))
    elif vis == "token_bars":
        vis_list.append(token_bars(study, notation))
    elif vis == "farness":
        vis_list.append(farness(study, notation, distance))
    else:
        raise Exception("invalid vis")
    return vis_list
