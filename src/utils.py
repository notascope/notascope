from functools import cache
from glob import glob


@cache
def ext(study, notation, obj):
    return sorted(glob(f"results/{study}/{notation}/{obj}/*"), key=len)[-1].split(".")[-1]


def slug_from_path(path):
    return ".".join(path.split("/")[-1].split(".")[:-1])
