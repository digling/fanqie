from lingpy import *
from collections import defaultdict



wl = Wordlist("fanqie.tsv")
etd = wl.get_etymdict(ref="cogid")
pairs = []
fanqie = {"shang": defaultdict(list), "xia": defaultdict(list)}

for k, (a, b) in etd.items():
    if (a and b) and (a[0] and b[0]):
        idx_b, idx_a = a[0], b[0]
        pairs += [[idx_a, idx_b]]
        fqs, fqx = wl[idx_a, "fanqie"][:2]
        tks_zhou, tks_bax = wl[idx_a, "tokens"], wl[idx_b, "tokens"]
        # initial and medial are important for the spelling
        s_zhou, s_bax = tks_zhou[:2], tks_bax[:2]
        x_zhou, x_bax = tks_zhou[1:], tks_bax[1:]
        fanqie["shang"][fqs] += [(tuple(s_zhou), tuple(s_bax))]
        fanqie["xia"][fqx] += [(tuple(x_zhou), tuple(x_bax))]

# refine by frequency
ambiguity = {"shang": [], "xia": []}
pred = {}
for sx in ["shang", "xia"]:
    for char, vals in fanqie[sx].items():
        uniqs = sorted(set(vals), key=lambda x: vals.count(x),
                reverse=True)
        ambiguity[sx] += [len(uniqs)]
        pred[sx, char] = uniqs

# finding: medial is more important for rhyme / final than for initial / shang
# TODO: add Baxter readings
# TODO: check Baxter readings against our characters (!)

def predict(fq):
    
    try:
        i = pred["shang", fq[0]][0][0][0]
        m1 = pred["shang", fq[0]][0][0][1]
    except:
        i, m1 = "?", "?"
    try:
        m2 = pred["xia", fq[1]][0][0][0]
        n = pred["xia", fq[1]][0][0][1]
        c = pred["xia", fq[1]][0][0][2]
        t = pred["xia", fq[1]][0][0][3]
        if len(t) == 2:
            t = t[1]
    except:
        m2, n, c, t = "?", "?", "?", "?"

    if m1 == m2:
        m = m2
    elif m2 == "." and m1 == "w":
        m = "w"
    else:
        m = m2

    comb = [i, m, n, c, t]
    out = []
    for elm in comb:
        if elm.strip("."):
            out += [elm.strip(".")]
    return "".join(out)


gy = csv2list("raw/guangyun_new.tsv", strip_lines=False)
visited = set()
scores = []
missing = {"shang": [], "xia": [], "readings": []}
for row in gy[2:]:
    fq = row[6]
    zhou = row[5].replace("˩˥", "˥").replace("˥˩", "˩")

    if len(fq) == 3 and zhou not in visited:
        prediction = predict(fq[:2])
        #print(zhou, "->", prediction)
        if not "?" in prediction:
            if prediction == zhou:
                scores += [1]
            else:
                scores += [0]
                print(zhou, "->", prediction)
        else:
            missing["readings"] += [1]
            if not ("shang", fq[0]) in pred:
                missing["shang"] += [(zhou, fq[0])]
            if not ("xia", fq[1]) in pred:
                missing["xia"] += [(zhou, fq[1])]
                
        visited.add(zhou)
print(len(scores), sum(scores) / len(scores), sum(missing["readings"]))
