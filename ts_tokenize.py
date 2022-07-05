#!/usr/bin/env python3

from tree_sitter import Language, Parser
import sys
from utils import slug_from_path

basedir = "/Users/nicolas/ets/tree-sitter-parser"

Language.build_library(
    basedir + "/build/languages.so",
    [basedir + "/tree-sitter-%s" % l for l in ["python", "javascript", "r"]],
)
langmap = dict(py="python", json="javascript", js="javascript", R="r")


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


if __name__ == "__main__":
    full_path = sys.argv[1]
    _, study, notation, spec = full_path.split("/")
    for token in get_tokens_for_file(full_path):
        print("\t".join([study, notation, slug_from_path(spec), token[1]]))
