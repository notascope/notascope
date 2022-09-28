from .utils import ext, slug_from_path  # noqa
from .distances import get_distance, distance_types, merged_distances  # noqa

from .scatter import get_scatter, get_scatter3d
from .dendro import get_dendro
from .network import get_network

vis_types = ["network", "tsne", "umap", "umap_3d", "dendro"]


def get_vis(study, notation, distance, vis, from_slug, to_slug):
    net = []
    fig = {}
    if vis == "network":
        net = get_network(study, notation, distance, from_slug, to_slug)
    elif vis == "tsne":
        fig = get_scatter(study, notation, distance, from_slug, to_slug, method="tsne")
    elif vis == "umap":
        fig = get_scatter(study, notation, distance, from_slug, to_slug, method="umap")
    elif vis == "umap_3d":
        fig = get_scatter3d(study, notation, distance, from_slug, to_slug, method="umap")
    elif vis == "dendro":
        fig = get_dendro(study, notation, distance, from_slug, to_slug)
    else:
        raise Exception("invalid vis")
    return net, fig
