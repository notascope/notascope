import sys

op = None
dest = False
cost = 0
total_cost = 0
for line in sys.stdin:
    line=line.strip()
    if line in ("","==="):
        if cost:
            print(" ",cost)
        op = None
        dest=False
        cost=0
    elif line == "---":
        pass
    elif op is None:
        op = line
        if op != "match":
            print(line)
    elif line == "to":
        dest = True
    elif op != "match" and not dest:
        print("    "+line)
        increment = 0.5 if op.startswith("del") else 1
        cost += increment
        total_cost += increment

if cost:
    print(" ",cost)
print("---")
print(",".join([sys.argv[1], sys.argv[2], str(total_cost)]))
