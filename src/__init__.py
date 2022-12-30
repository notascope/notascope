from .utils import *  # noqa
from .distances import *  # noqa
from .tokens import *  # noqa

from .scatter import get_scatter
from .dendro import get_dendro
from .network import get_network
from .distributions import token_rank, token_bars, farness

vis_map = {
    "mst": get_network,
    "spanner-1": get_network,
    "spanner-1.1": get_network,
    "spanner-1.2": get_network,
    "spanner-1.5": get_network,
    "tsne": get_scatter,
    "umap": get_scatter,
    "dendro": get_dendro,
    "token_rank": token_rank,
    "token_bars": token_bars,
    "farness": farness,
}
vis_types = list(vis_map.keys())


def get_vis(gallery, notation, distance, vis, from_slug, to_slug):
    return [vis_map[vis](gallery, notation, distance, from_slug, to_slug, vis)]
