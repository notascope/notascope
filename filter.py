import fileinput

op = None
dest = False
cost = 0
total_cost = 0
for line in fileinput.input():
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
        cost += 1
        total_cost += 1

print("---")
print("total cost:", total_cost)
print("---")
