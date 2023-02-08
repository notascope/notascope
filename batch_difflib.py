from itertools import permutations
from difflib import SequenceMatcher
from glob import glob
import os
import sys
from src.utils import slug_from_path
from tree_sitter import Language, Parser

basedir = "/Users/nicolas/ets/tree-sitter-parser"

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
tokens = dict()
for fpath in glob(os.path.join(inpath, "*.*")):
    tokens[slug_from_path(fpath)] = get_tokens_for_file(fpath)


def cost(from_slug, to_slug):
    s = SequenceMatcher(None, tokens[from_slug], tokens[to_slug])
    total_cost = 0
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag != "equal":
            total_cost += max(i2 - i1, j2 - j1)
    return total_cost


with open(f"results/{gallery}/{notation}/tokens.tsv", "w") as f:
    for slug, tokens_list in tokens.items():
        for token in tokens_list:
            print("\t".join([gallery, notation, slug, token[1]]), file=f)

with open(f"results/{gallery}/{notation}/difflib_costs.csv", "w") as f:
    for (from_slug, to_slug) in permutations(tokens, 2):
        print(
            ",".join(
                [gallery, notation, from_slug, to_slug, str(cost(from_slug, to_slug))]
            ),
            file=f,
        )
