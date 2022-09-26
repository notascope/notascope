import json
from functools import cache
from numba import njit
import numpy as np
from .utils import ext
from .distances import dmat_and_order, get_distance, get_embedding, get_mst


def get_network(study, notation, distance, from_slug, to_slug):
    net = json.loads(build_network(study, notation, distance))

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
            if source != dest:
                net.append(
                    {
                        "data": {"source": source, "target": dest, "id": source + "__" + dest + "_nnnn", "length": dmat_sym[from_index, to_index]},
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
                    if via_k <= direct:
                        # note: if via_k < direct this is a violation of the triangle inequality
                        # this... happens unfortunately
                        has_k = True
                        break
                if not has_k:
                    result[i, j] = direct
    return result


@cache
def build_network(study, notation, distance):
    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    network_elements = []
    n = len(dmat)
    if n < 20:
        emb_df = get_embedding(study, notation, distance, "mds")
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
        emb_df = get_embedding(study, notation, distance, "kk")
        spanning = get_mst(study, notation, distance)
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

    emb_span = emb_df.values.max() - emb_df.values.min()

    if n > 500:
        scale = 10000
    elif n > 15:
        scale = 2000
    else:
        scale = 1000
    imgext = ext(study, notation, "img")
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
