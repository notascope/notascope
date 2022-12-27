from functools import cache
import json


@cache
def load_registry():
    with open("results/registry.json", "r") as f:
        return json.load(f)


@cache
def ext(study, notation, obj):
    return load_registry()[study][notation]["ext"][obj]


def slug_from_path(path):
    return ".".join(path.split("/")[-1].split(".")[:-1])
