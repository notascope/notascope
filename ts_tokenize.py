#!/usr/bin/env python3

from tree_sitter import Language, Parser

basedir = "/Users/nicolas/ets/tree-sitter-parser"

Language.build_library(
    basedir + "/build/languages.so",
    [basedir + "/tree-sitter-%s" % x for x in ["python", "javascript", "r"]],
)
langmap = dict(py="python", vl="javascript", json="javascript", js="javascript", R="r")


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
