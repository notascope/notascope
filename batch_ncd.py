from itertools import permutations
from glob import glob
import os
import sys
from src.utils import spec_from_path
from lz4.frame import compress


inpath = sys.argv[1]
pieces = inpath.split("/")
gallery = pieces[1]
notation = pieces[2]
file_bytes = dict()
single_compressed_length = dict()
single_length = dict()
for fpath in glob(os.path.join(inpath, "*.*")):
    spec = spec_from_path(fpath)
    with open(fpath, "rb") as f:
        file_bytes[spec] = f.read()
    single_compressed_length[spec] = len(compress(file_bytes[spec]))
    single_length[spec] = len(file_bytes[spec])


def cost(args):
    from_spec, to_spec = args
    a = single_compressed_length[from_spec]
    b = single_compressed_length[to_spec]
    ab = len(compress(file_bytes[from_spec] + file_bytes[to_spec]))
    return [
        gallery,
        notation,
        from_spec,
        to_spec,
        str(int(single_length[from_spec])),
        str(int(a)),
        str(int(b)),
        str(int(ab)),
    ]


if __name__ == "__main__":
    with open(f"results/{gallery}/{notation}/ncd_costs.csv", "w") as f:
        for r in map(cost, permutations(file_bytes, 2)):
            print(",".join(r), file=f)
