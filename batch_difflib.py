from itertools import permutations
from ts_tokenize import get_tokens_for_file
from difflib import SequenceMatcher
from glob import glob
import os
import sys
from utils import slug_from_path


inpath = sys.argv[1]
pieces = inpath.split("/")
study = pieces[-2]
system = pieces[-1]
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


with open(f"results/{study}/{system}/difflib_costs.csv", "w") as f:
    for (from_slug, to_slug) in permutations(tokens, 2):
        print(",".join([study, system, from_slug, to_slug, str(cost(from_slug, to_slug))]), file=f)
