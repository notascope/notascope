from ts_tokenize import get_tokens_for_file
from difflib import SequenceMatcher
import sys

_, f1, f2 = sys.argv

pieces = f1.split("/")
from_slug = pieces[-1].split(".")[0]
system = pieces[-2]
study = pieces[-3]
to_slug = f2.split("/")[-1].split(".")[0]

t1 = get_tokens_for_file(f1)
t2 = get_tokens_for_file(f2)

s = SequenceMatcher(None, t1, t2)
total_cost = 0
for tag, i1, i2, j1, j2 in s.get_opcodes():
    if tag != "equal":
        cost = max(i2 - i1, j2 - j1)
        total_cost += cost
        print("{:2} {:7} {!r} --> {!r}".format(cost, tag, t1[i1:i2], t2[j1:j2]))

print(",".join([study, system, from_slug, to_slug, str(total_cost)]))
