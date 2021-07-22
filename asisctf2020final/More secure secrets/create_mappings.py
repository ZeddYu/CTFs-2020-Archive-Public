inp = open('constants.txt', 'r').readlines()

ints = dict()
strs = dict()

for i in range(0, len(inp)-1, 2):
    if not inp[i].startswith('['):
        print(i)
        break

    k, v = (inp[i].strip(), inp[i + 1].strip())

    k = k[2:-4]

    if any(x in k for x in '1234567890'):
        continue

    if v.startswith('int('):
        val = int(v.split(')')[0][4:], 10)
        ints[k] = val
    elif v.startswith('string('):
        val = v.split('"')[1]
        strs[k] = val

print(len(ints), len(strs))

ints2 = {}
for k, v in ints.items():
    if v not in ints2:
        ints2[v] = k
        continue
    if len(ints2[v]) > len(k):
        ints2[v] = k


import string

mp = {c: None for c in string.ascii_letters}

for c in mp.keys():
    for (str_k, str_v) in strs.items():
        if not c in str_v:
            continue

        indices = []
        for idx in range(len(str_v)):
            if str_v[idx] == c:
                indices.append(idx)

        print(indices)

        for idx in indices:
            if idx not in ints2:
                continue
            cand = str_k + '[' + ints2[idx] + ']'

            if not mp[c] or len(cand) < len(mp[c]):
                mp[c] = cand

print(mp)
