import json
from functools import cache

import igraph
from sklearn.manifold import MDS
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import coo_matrix
from numba import njit
import dash_cytoscape as cyto


import numpy as np
import pandas as pd
from .distances import dmat_and_order, get_distance


def get_network(study, notation, distance, from_slug, to_slug, imgext):
    net = json.loads(build_network(study, notation, distance, imgext))

    if from_slug != to_slug:
        from_to_distance = get_distance(study, notation, distance, from_slug, to_slug)
        to_from_distance = get_distance(study, notation, distance, to_slug, from_slug)
        both_dirs = [[from_slug, to_slug], [to_slug, from_slug]]
        to_drop = ["__".join(x) for x in both_dirs]
        dropped = [elem for elem in net if elem["data"]["id"] in to_drop]
        net = [elem for elem in net if elem["data"]["id"] not in to_drop]
        for source, dest in both_dirs:
            id = source + "__" + dest
            new_elem = {
                "data": {
                    "source": source,
                    "target": dest,
                    "id": id,
                    "length": from_to_distance if source == from_slug else to_from_distance,
                },
                "classes": "",
            }
            if len(dropped) == 0 or (id not in [x["data"]["id"] for x in dropped] and "bidir" not in dropped[0]["classes"]):
                new_elem["classes"] += " inserted"
            if source == from_slug:
                new_elem["classes"] += " selected"
            net.append(new_elem)
    elif from_slug:
        dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
        from_index = order.index(from_slug)
        top_indices = np.argsort(dmat_sym[from_index])
        for i in range(min(10, len(dmat_sym))):
            source = from_slug
            to_index = top_indices[i]
            dest = order[to_index]
            net.append(
                {
                    "data": {"source": source, "target": dest, "id": source + "__" + dest, "length": dmat_sym[from_index, to_index]},
                    "classes": "neighbour",
                }
            )
    for elem in net:
        if elem["data"]["id"] in [from_slug, to_slug]:
            elem["classes"] += " selected"
    return net


@njit
def find_edges(dmat):
    n = len(dmat)
    result = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            has_k = False
            direct = dmat[i, j]
            if direct != 0:
                for k in range(n):
                    if k == i or k == j:
                        continue
                    via_k = dmat[i, k] + dmat[k, j]
                    if (via_k - direct) / direct <= 0:
                        has_k = True
                        break
                if not has_k:
                    result[i, j] = direct
    return result


@cache
def build_network(study, notation, distance, imgext):
    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    network_elements = []
    n = len(dmat)
    if n < 20:
        np.random.seed(123)
        mds = MDS(n_components=2, dissimilarity="precomputed")
        embedding = mds.fit_transform(dmat_sym)

        edges = find_edges(dmat)
        for i in range(n):
            for j in range(n):
                if edges[i, j] == 0:  # no zero or self-edges
                    continue
                longest = edges[i, j] > edges[j, i]
                eq = edges[i, j] == edges[j, i]
                this_eq = eq and i > j  # only first of the two bidir edges
                if longest or this_eq:
                    network_elements.append(
                        {
                            "data": {
                                "source": order[i],
                                "target": order[j],
                                "id": order[i] + "__" + order[j],
                                "length": edges[i, j],
                            },
                            "classes": (" bidir" if eq else ""),
                        }
                    )
    else:
        spanning = coo_matrix(minimum_spanning_tree(dmat_sym))
        g = igraph.Graph.Weighted_Adjacency(spanning.toarray().tolist())
        np.random.seed(123)
        layout = g.layout_kamada_kawai(maxiter=10000)
        embedding = np.array(layout.coords)

        for i, j, d in zip(spanning.row, spanning.col, spanning.data):
            network_elements.append(
                {
                    "data": {
                        "source": order[i],
                        "target": order[j],
                        "id": order[i] + "__" + order[j],
                        "length": d,
                    },
                    "classes": "",
                }
            )

    emb_df = pd.DataFrame(embedding, index=order, columns=["x", "y"])
    emb_span = embedding.max() - embedding.min()

    scale = 1000 if n < 20 else 10000
    for i, row in emb_df.iterrows():
        network_elements.append(
            {
                "data": {
                    "id": i,
                    "label": i,
                    "url": f"/assets/results/{study}/{notation}/img/{i}.{imgext}",
                },
                "position": {c: row[c] * scale / emb_span for c in ["x", "y"]},
                "classes": "",
            }
        )
    return json.dumps(network_elements)


def cytoscape(id, elements):
    return cyto.Cytoscape(
        id=id,
        className="network",
        layout={"name": "preset", "fit": True},
        minZoom=0.05,
        maxZoom=1,
        autoRefreshLayout=False,
        elements=elements,
        style=dict(height="800px", width="initial"),
        stylesheet=[
            {
                "selector": "node",
                "style": {
                    "width": 100,
                    "height": 100,
                    "shape": "rectangle",
                    "background-fit": "cover",
                    "background-image": "data(url)",
                    "label": "data(label)",
                    "border-color": "grey",
                    "border-width": 1,
                    "text-outline-color": "white",
                    "text-outline-width": "2",
                    "text-margin-y": "20",
                },
            },
            {
                "selector": "edge",
                "style": {
                    "line-color": "lightgrey",
                    "curve-style": "bezier",
                    "target-arrow-color": "lightgrey",
                    "control-point-weight": 0.6,
                    "target-arrow-shape": "triangle-backcurve",
                    "arrow-scale": 2,
                    "label": "data(length)",
                    "font-size": "24px",
                    "text-outline-color": "white",
                    "text-outline-width": "3",
                },
            },
            {
                "selector": ".bidir",
                "style": {
                    "source-arrow-color": "lightgrey",
                    "source-arrow-shape": "triangle-backcurve",
                },
            },
            {
                "selector": ".selected",
                "style": {
                    "source-arrow-color": "red",
                    "target-arrow-color": "red",
                    "line-color": "red",
                    "border-color": "red",
                    "border-width": 5,
                },
            },
            {
                "selector": ".inserted",
                "style": {"line-style": "dashed"},
            },
            {
                "selector": ".neighbour",
                "style": {"line-color": "red"},
            },
        ],
    )
