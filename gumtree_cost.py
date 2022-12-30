import sys

op = None
dest = False
cost = 0
total_cost = 0
for line in sys.stdin:
    line = line.rstrip()
    if line in ("", "==="):
        if cost:
            print(" ", cost)
        op = None
        dest = False
        total_cost += cost
        cost = 0
        last_indent = None
    elif line == "---":
        pass
    elif op is None:
        op = line
        if op != "match":
            print(line)
    elif op != "match" and not dest:
        print(line)
        if op.startswith("del"):
            cost = 1
        elif op.startswith("move"):
            cost = 1
        elif op == "insert-node":
            cost = 1
        elif op == "update-node":
            cost = 1
        elif op == "insert-tree":
            indent = len(line) - len(line.lstrip())
            if last_indent is not None and indent <= last_indent:
                cost += 1
            last_indent = indent
        else:
            raise
    if line == "to":
        dest = True

if cost:
    print(" ", cost)
    total_cost += cost
print("---")
_, gallery, notation, from_slug, to_slug = sys.argv
print(",".join([gallery, notation, from_slug, to_slug, str(total_cost)]))
