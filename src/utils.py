import json
from pathlib import Path
import os
from time import time


import functools
from typing import Callable, TypeVar, cast

FuncT = TypeVar("FuncT", bound=Callable)


def cache(func: FuncT) -> FuncT:
    return cast(FuncT, functools.cache(func))


@cache
def debug_mode():
    return os.environ.get("DASH_DEBUG") == "true"


@cache
def load_registry():
    with open("results/registry.json", "r") as f:
        return json.load(f)


@cache
def galleries():
    return list(load_registry().keys())


@cache
def gallery_notations(gallery):
    return list(load_registry()[gallery].keys())


@cache
def gallery_specs(gallery):
    specs = set()
    for _, notation in load_registry()[gallery].items():
        specs.update(notation["specs"])
    return sorted(specs)


@cache
def pretty_source(gallery, notation, spec):
    try:
        return spec_path("results", gallery, notation, "pretty", spec).read_text()
    except:
        return ""


@cache
def vscode_link(gallery, notation, spec):
    return f"vscode://file/{str(spec_path('galleries', gallery, notation, '.', spec).resolve())}"


@cache
def spec_path(prefix, gallery, notation, subdir, spec):
    srcext = ext(gallery, notation, "source")
    return Path(prefix, gallery, notation, subdir, f"{spec}.{srcext}")


@cache
def ext(gallery, notation, obj):
    return load_registry()[gallery][notation]["ext"][obj]


@cache
def md_lang(gallery, notation):
    langs = dict(py="python", R="R", json="json", vl="json")
    return langs[ext(gallery, notation, "source")]


@cache
def img_path(gallery, notation, spec):
    imgext = ext(gallery, notation, "img")
    return f"/assets/results/{gallery}/{notation}/img/{spec}.{imgext}?{time()}"


def spec_from_path(path):
    return ".".join(path.split("/")[-1].split(".")[:-1])
