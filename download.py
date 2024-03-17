from pyedictor import fetch
from lingpy import Wordlist
import json

wl = fetch(
        "fanqie",
        base_url="https://lingulist.de/edev",
        to_lingpy=Wordlist)

wl.output('tsv', filename="fanqie", ignore="all", prettify=False)

data = {"shang": {"baxter": {}, "zhou": {}}, "xia": {"baxter": {}, "zhou": {}}}
for idx in wl:
    
    who = wl[idx, "doculect"].lower()
    what = "shang" if "shang" in wl[idx, "concept"] else "xia"
    char = wl[idx, "concept"].split(" ")[0]
    tokens = wl[idx, "tokens"]
    

    if what == "shang" and len(tokens) == 2:
        data[what][who][char] = list(tokens)
    elif what == "shang" and len(tokens) != 2:
        print(what, who, char, tokens)
    
    if what == "xia" and len(tokens) == 4:
        data[what][who][char] = list(tokens)
    elif what == "xia" and len(tokens) != 4:
        print(what, who, char, tokens)

with open("app/data.js", "w") as f:
    f.write("var fanqie = "+json.dumps(data)+";")
