from pyedictor import fetch
from lingpy import Wordlist


wl = fetch(
        "sinocon",
        remote_dbase="sinocon.sqlite3",
        base_url="https://lingulist.de/edev/",
        to_lingpy=Wordlist)

wl.output('tsv', filename="fanqie", ignore="all")
