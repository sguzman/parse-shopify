new_lines = set(x.strip() for x in open('../new.csv').readlines())
old_lines = set(x.strip() for x in open('../old.csv').readlines())

new_unique = []
for o in new_lines:
    if o not in old_lines:
        new_unique.append(o)

new_unique.sort()

for n in new_unique:
    print(n.strip())
