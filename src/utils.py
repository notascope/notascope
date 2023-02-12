from functools import cache
import json


@cache
def load_registry():
    with open("results/registry.json", "r") as f:
        return json.load(f)


@cache
def ext(gallery, notation, obj):
    return load_registry()[gallery][notation]["ext"][obj]


def spec_from_path(path):
    return ".".join(path.split("/")[-1].split(".")[:-1])
