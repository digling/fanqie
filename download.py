from pyedictor import fetch
from lingpy import Wordlist


wl = fetch(
        "fanqie",
        remote_dbase="fanqie.sqlite3",
        base_url="https://lingulist.de/edev/",
        to_lingpy=Wordlist)

wl.output('tsv', filename="fanqie", ignore="all", prettify=False)
