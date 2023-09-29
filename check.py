from lingpy import *
from collections import defaultdict
from tabulate import tabulate

wl = Wordlist("fanqie.tsv")

etd = wl.get_etymdict(ref="cogid")

# make mappings

maps = defaultdict(list)
char_maps = defaultdict(list)

for key, (v1, v2) in etd.items():
    if v1 and v2:
        c1 = v1[0]
        c2 = v2[0]
        
        tks1, tks2 = wl[c1, "tokens"], wl[c2, "tokens"]
        if len(tks1) == len(tks2) == 5:
            for s, a, b in zip("imnct", tks1, tks2):
                if not (a == "." and b == "."):
                    maps[a, s] += [(b, c1, c2)]
        else:
            print(c1, c2, wl[c1, "tokens"], wl[c2, "tokens"])

for s in "imnct":
    table = []
    for a, b in maps:
        if b == s:
            chars = [row[0] for row in maps[a, b]]
            different_chars = sorted(set(chars), key=lambda x: chars.count(x),
                                     reverse=True)
            out = " / ".join(different_chars)
            freqs = " / ".join([str(chars.count(x)) for x in different_chars])
            row = [s, a, out, freqs]
            table += [row]
    print(tabulate(table, tablefmt="pipe"))


D = {0: wl.columns}
for idx, tks, alm in wl.iter_rows("tokens", "alignment"):
    wl[idx, "alignment"] = tks
    if wl[idx, "cogid"] != 0:
        D[idx] = wl[idx]
wl2 = Wordlist(D)
wl2.output('tsv', filename="shang-corr", ignore="all")
        
