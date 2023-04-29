from itertools import combinations
from glob import glob
import os
import sys
from src.utils import spec_from_path
from lz4.frame import compress
from tree_sitter import Language, Parser
import pandas as pd
import textdistance


basedir = "./tree_sitter_languages"

Language.build_library(
    basedir + "/build/languages.so",
    [basedir + "/tree-sitter-%s" % x for x in ["python", "javascript", "r"]],
)
langmap = dict(
    py="python",
    vl="javascript",
    vg="javascript",
    json="javascript",
    js="javascript",
    mjs="javascript",
    R="r",
)


def get_tokens_for_file(infilepath):
    langname = langmap[infilepath.split(".")[-1]]
    lang = Language(basedir + "/build/languages.so", langname)
    parser = Parser()
    parser.set_language(lang)
    with open(infilepath, "r") as f:
        tree = parser.parse(bytes(f.read(), "utf8"))

    result = []

    def recurse(c, level=0):
        if c.node.type not in ["string", "identifier"] and c.goto_first_child():
            recurse(c, level + 1)
            while c.goto_next_sibling():
                recurse(c, level + 1)
            c.goto_parent()
        else:
            if c.node.type.strip() != "":
                result.append((c.node.type, c.node.text.decode("utf-8")))

    recurse(tree.walk())
    return result


inpath = sys.argv[1]
pieces = inpath.split("/")
gallery = pieces[1]
notation = pieces[2]
file_bytes = dict()
single_compressed_length = dict()
single_length = dict()
tokens = dict()

paths = glob(os.path.join(inpath, "*.*"))
for fpath in paths:
    spec = spec_from_path(fpath)
    with open(fpath, "rb") as f:
        file_bytes[spec] = f.read()
    single_compressed_length[spec] = len(compress(file_bytes[spec]))
    single_length[spec] = len(file_bytes[spec])
    tokens[spec] = get_tokens_for_file(fpath)


token_rows = []
for spec, tokens_list in tokens.items():
    for token in tokens_list:
        token_rows.append([gallery, notation, spec, token[1]])

token_df = pd.DataFrame.from_records(
    token_rows, columns=["gallery", "notation", "spec", "token"]
)
token_df.to_parquet(f"results/{gallery}/{notation}/tokens.pqt")


def voi(from_spec, to_spec):
    a = single_compressed_length[from_spec]
    b = single_compressed_length[to_spec]
    ab = len(compress(file_bytes[from_spec] + file_bytes[to_spec]))
    return 2 * ab - a - b


def cd(from_spec, to_spec):
    a = single_compressed_length[from_spec]
    b = single_compressed_length[to_spec]
    ab = len(compress(file_bytes[from_spec] + file_bytes[to_spec]))
    return ab - min(a, b)


def ncd(from_spec, to_spec):
    a = single_compressed_length[from_spec]
    b = single_compressed_length[to_spec]
    ab = len(compress(file_bytes[from_spec] + file_bytes[to_spec]))
    return 1000 * (ab - min(a, b)) / max(a, b)


def distances(args):
    from_spec, to_spec = args
    voi_avg = (voi(from_spec, to_spec) + voi(to_spec, from_spec)) / 2
    cd_avg = (cd(from_spec, to_spec) + cd(to_spec, from_spec)) / 2
    ncd_avg = (ncd(from_spec, to_spec) + ncd(to_spec, from_spec)) / 2
    lev = textdistance.levenshtein.distance(tokens[from_spec], tokens[to_spec])
    return (
        [
            gallery,
            notation,
            from_spec,
            to_spec,
            int(single_length[from_spec]),
            voi_avg,
            cd_avg,
            ncd_avg,
            lev,
        ],
        [
            gallery,
            notation,
            to_spec,
            from_spec,
            int(single_length[to_spec]),
            voi_avg,
            cd_avg,
            ncd_avg,
            lev,
        ],
    )


distance_rows = []
for xy, yx in map(distances, combinations(file_bytes, 2)):
    distance_rows.append(xy)
    distance_rows.append(yx)

distance_df = pd.DataFrame.from_records(
    distance_rows,
    columns=[
        "gallery",
        "notation",
        "from_spec",
        "to_spec",
        "from_length",
        "voi",
        "cd",
        "ncd",
        "levenshtein",
    ],
)
distance_df.to_parquet(f"results/{gallery}/{notation}/distances.pqt")
