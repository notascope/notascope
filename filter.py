import sys

op = None
dest = False
cost = 0
total_cost = 0
for line in sys.stdin:
    line = line.strip()
    if line in ("", "==="):
        if cost:
            print(" ", cost)
        op = None
        dest = False
        total_cost += cost
        cost = 0
    elif line == "---":
        pass
    elif op is None:
        op = line
        if op != "match":
            print(line)
    elif line == "to":
        dest = True
    elif op != "match" and not dest:
        print("    " + line)
        if op.startswith("del"):
            cost = 1
        elif op.startswith("move"):
            cost = 1
        elif op == "insert-node":
            cost = 1
        elif op == "update-node":
            cost = 1
        else:
            cost += 1

if cost:
    print(" ", cost)
    total_cost += cost
print("---")
_, system, from_slug, to_slug = sys.argv
print(",".join([system, from_slug, to_slug, str(total_cost)]))
