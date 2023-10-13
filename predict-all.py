from lingpy import *
from collections import defaultdict
import json
from tabulate import tabulate


wl = Wordlist("fanqie.tsv")
etd = wl.get_etymdict(ref="cogid")

predis = {"shang": {}, "xia": {}}

for idx, doculect, concept, tokens in wl.iter_rows("doculect", "concept",
                                                   "tokens"):
    if "(shang)" in concept:
        if len(tokens) == 2:
            predis["shang"][doculect, concept.split(" ")[0]] = tokens
    if "(xia)" in concept:
        if len(tokens) == 4:
            predis["xia"][doculect, concept.split(" ")[0]] = tokens
    

def predict(fq, what="Zhou", pred=None):
    if not pred:
        pred = predis
    
    try:
        i = pred["shang"][what, fq[0]][0]
        m1 = pred["shang"][what, fq[0]][1]
    except:
        i, m1 = "?", "?"
    try:
        m2 = pred["xia"][what, fq[1]][0]
        n = pred["xia"][what, fq[1]][1]
        c = pred["xia"][what, fq[1]][2]
        t = pred["xia"][what, fq[1]][3].replace("˥˩", "˩")
    except:
        m2, n, c, t = "?", "?", "?", "?"

    if m1 == m2:
        m = m2
    else:
        m = m2

    comb = [i, m, n, c, t]
    out = []
    for elm in comb:
        if elm.strip("."):
            out += [elm.strip(".")]
    out_string = "".join(out)
    if what == "Baxter":
        st = [
                ("yj", "y"),
                ("'", "ʔ"),
                ("tsyhj", "tsyh"),
                ("pjw", "pj"),
                ("phjw", "phj"), ("bjw", "bj"), ("mjw", "mj"),
                ("pjwo", "pjo"),
                ("bjwo", "bjo"),
                ("phjwo", "phjo"),
                ("mjwo", "mjo"),
                ("pwo", "pO"),
                ("phwo", "phO"),
                ("bwo", "bO"),
                ("mwo", "mO"),
                ("ae", "æ"),
                ("bw", "b"),
                ("pw", "p"),
                ("phw", "ph"),
                ("mw", "m"),
                ("phO", "phwo"), ("pO", "pwo"), ("bO", "bwo"), ("mO", "mwo"),
                ]
        for s, t in st:
            out_string = out_string.replace(s, t)
    return out_string


gy = csv2list("raw/guangyun_new.tsv", strip_lines=False)

visited = set()
scores = []
missing = {"shang": [], "xia": [], "readings": []}
results = []
num = 1
char2fan = defaultdict(list)
visited = set()
for row in gy[2:]:
    fq = row[6]
    if fq[0] != "*":
        char2fan[row[2]] += [fq]
        zhou = row[5].replace("˥˩", "˩")

        if len(fq) == 3 and zhou not in visited:
            prediction = predict(fq[:2], what="Zhou", pred=predis)
            baxter = predict(fq[:2], what="Baxter", pred=predis)
            #print(zhou, "->", prediction)
            if not "?" in prediction:
                if prediction == zhou:
                    scores += [1]
                else:
                    scores += [0]
                    results += [[num, row[2], fq, prediction, zhou, baxter]]
                    num += 1
                    #print(zhou, "->", prediction, "/", fq)
            else:
                missing["readings"] += [1]
                if not ("Zhou", fq[0]) in predis["shang"]:
                    missing["shang"] += [(zhou, fq[0])]
                if not ("Zhou", fq[1]) in predis["xia"]:
                    missing["xia"] += [(zhou, fq[1])]

                results += [[num, row[2], fq, prediction, zhou, baxter]]
                scores += [0]
                num += 1
                    
            visited.add(zhou)

print(tabulate(results, headers=["Number", "Character", "Fanqie", "Prediction",
                                 "Reading", "Baxter"], tablefmt="pipe"))

print(len(scores), sum(scores) / len(scores), sum(missing["readings"]))
# convert to json
predictions = {"shang": {"baxter": {}, "zhou": {}}, "xia": {"baxter": {},
    "zhou": {}}}
#for (sx, char), vals in pred.items():
#    predictions[sx]["baxter"][char] = list(vals[0][1])
#    predictions[sx]["zhou"][char] = list(vals[0][0])
#with open("app/data.js", "w") as f:
#    f.write('var fanqie = '+json.dumps(predictions, indent=2)+";\n")
input()
scores = []
fails = []
fail = 1
for row in csv2list("raw/ocbs.tsv", strip_lines=False):
    char = row[0]
    mch = row[3]
    mch = mch.replace("jie", "je").replace("jwie", "jwe")
    if char in char2fan:
        preds = []
        for fq in char2fan[char]:
            bax = predict(fq[:2], "Baxter", predis)
            preds += [bax]
        if mch in preds:
            scores += [1]
        else:
            scores += [0]
            fails += [[fail, char, " ".join(char2fan[char]), mch, " ".join(preds)]]
            fail += 1
print(tabulate(fails, headers=["Number", "Character", "Fanqie", "MCH",
                               "Predictions"], tablefmt="pipe"))
print(sum(scores) / len(scores))

