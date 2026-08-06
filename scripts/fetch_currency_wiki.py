#!/usr/bin/env python3
"""Fetch all currency-class items + descriptions from poewiki's Cargo API into a
local cache (reference_data/currency_wiki.json) for the text lake's currency.txt.

Separate from generate_text_lake.py ON PURPOSE: the lake generator is offline-pure
(PoB submodule + local GGG exports); network sources go through dated caches like
the rest of reference_data/ (see its README's fetched:/staleness conventions).

Run after league launches / when the wiki catches up; regenerate the lake after.
"""
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent
OUT = SUITE / "reference_data" / "currency_wiki.json"
API = "https://www.poewiki.net/w/api.php"
UA = "poe-data-mcp/0.3 (+https://github.com/charleslucas/poe-data-mcp) python-urllib"
CLASSES = ["Currency Item", "Stackable Currency"]

def cargo(where, offset):
    q = urllib.parse.urlencode({
        "action": "cargoquery", "tables": "items",
        "fields": "items.name,items.class,items.description",
        "where": where, "limit": 500, "offset": offset, "format": "json",
    })
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

rows, seen = [], set()
for cls in CLASSES:
    offset = 0
    while True:
        d = cargo(f'items.class="{cls}"', offset)
        batch = d.get("cargoquery", [])
        for it in batch:
            t = it.get("title", {})
            key = t.get("name", "")
            if key and key not in seen:
                seen.add(key)
                rows.append({"name": key, "class": t.get("class", cls),
                             "description": t.get("description") or ""})
        if len(batch) < 500:
            break
        offset += 500

rows.sort(key=lambda r: r["name"])
OUT.write_text(json.dumps({
    "fetched": datetime.date.today().isoformat(),
    "source": "poewiki cargo API (items.name/class/description; classes: %s)" % ", ".join(CLASSES),
    "count": len(rows), "items": rows,
}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(rows)} currency items -> {OUT}")
