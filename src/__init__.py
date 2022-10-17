from .utils import ext, slug_from_path  # noqa
from .distances import get_distance, distance_types, merged_distances  # noqa

from .scatter import get_scatter, get_scatter3d
from .dendro import get_dendro
from .network import get_network

vis_types = ["mst", "spanner-1", "spanner-1.1", "spanner-1.2", "spanner-1.5", "tsne", "umap", "umap_3d", "dendro"]


def get_vis(study, notation, distance, vis, from_slug, to_slug):
    net = []
    fig = {}
    if vis.startswith("spanner"):
        net = get_network(study, notation, distance, from_slug, to_slug, method=vis)
    elif vis == "mst":
        net = get_network(study, notation, distance, from_slug, to_slug, method="mst")
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
