from itertools import permutations
from glob import glob
import os
import sys
from src.utils import spec_from_path
from lz4.frame import compress
from tree_sitter import Language, Parser
from difflib import SequenceMatcher
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


for fpath in glob(os.path.join(inpath, "*.*")):
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


def distances(args):
    from_spec, to_spec = args
    a = single_compressed_length[from_spec]
    b = single_compressed_length[to_spec]
    ab = len(compress(file_bytes[from_spec] + file_bytes[to_spec]))
    s = SequenceMatcher(None, tokens[from_spec], tokens[to_spec])
    difflib_cost = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != "equal":
            difflib_cost += max(i2 - i1, j2 - j1)
    return [
        gallery,
        notation,
        from_spec,
        to_spec,
        int(single_length[from_spec]),
        int(a),
        int(b),
        int(ab),
        int(difflib_cost),
        int(textdistance.levenshtein.distance(tokens[from_spec], tokens[to_spec])),
    ]


distance_rows = [r for r in map(distances, permutations(file_bytes, 2))]
distance_df = pd.DataFrame.from_records(
    distance_rows,
    columns=[
        "gallery",
        "notation",
        "from_spec",
        "to_spec",
        "from_length",
        "a",
        "b",
        "ab",
        "difflib",
        "levenshtein",
    ],
)
distance_df.to_parquet(f"results/{gallery}/{notation}/distances.pqt")
