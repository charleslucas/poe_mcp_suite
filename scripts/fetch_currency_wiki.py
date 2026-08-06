#!/usr/bin/env python3
"""Fetch all currency-class items + descriptions from poewiki's Cargo API into a
local cache (reference_data/currency_wiki.json) for the text lake's currency.txt.

Separate from generate_text_lake.py ON PURPOSE: the lake generator is offline-pure
(PoB submodule + local GGG exports); network sources go through dated caches like
the rest of reference_data/ (see its README's fetched:/staleness conventions).

Run after league launches / when the wiki catches up; regenerate the lake after.
"""
import html
import json
import datetime
import urllib.request
import urllib.parse
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent
OUT = SUITE / "reference_data" / "currency_wiki.json"
API = "https://www.poewiki.net/w/api.php"
UA = "poe-data-mcp/0.3 (+https://github.com/charleslucas/poe-data-mcp) python-urllib"
# Trade-site "General" categories + league consumables (user-driven list 2026-08-05,
# mapped to poewiki class names via a Cargo group_by sweep of all 80 item classes).
# Oils / Omens / Tattoos / Ducats / Djinn Coins / Artifacts are INSIDE "Currency Item".
CLASSES = [
    "Currency Item", "Map Fragment", "Breachstone", "Divination Card",
    "Ember of the Allflame", "Wombgift", "Graft", "Chart", "Incubator",
    "Harvest Seed", "Memory", "Corpse item", "Idol", "Tincture", "Charm",
    "Relic", "Sanctified Relic", "Resonator", "Expedition Logbook", "Sentinel",
    "Captured Soul", "Vault Key", "Voidstone", "Watchstone", "Contract",
    "Blueprint", "Heist Target", "Gold", "Map", "Incursion Item",
    "Miscellaneous Map Item", "Labyrinth Key",
]
PAUSE_S = 0.5  # politeness: sequential, throttled; poewiki is community-run.
# Content licence is CC BY-NC-SA — the lake output is LOCAL-ONLY (gitignored) per
# legal_considerations.md conventions, so nothing fetched here is redistributed.

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
        import time; time.sleep(PAUSE_S)
        d = cargo(f'items.class="{cls}"', offset)
        batch = d.get("cargoquery", [])
        for it in batch:
            t = it.get("title", {})
            key = html.unescape(html.unescape(t.get("name", "")))
            if key and key not in seen:
                seen.add(key)
                rows.append({"name": key,
                             "class": html.unescape(html.unescape(t.get("class", cls))),
                             "description": html.unescape(html.unescape(t.get("description") or ""))})
        if len(batch) < 500:
            break
        offset += 500

# ---- uniques supplement: ALL wiki uniques w/ stat text (for names PoB lacks:
# unique maps, contracts, watchstones, memories, relics...) -> wiki_uniques.json
urows, offset = [], 0
while True:
    import time as _t; _t.sleep(PAUSE_S)
    d = cargo('items.rarity="Unique"', offset)
    batch = d.get("cargoquery", [])
    for it in batch:
        t = it.get("title", {})
        urows.append({"name": html.unescape(html.unescape(t.get("name", ""))),
                      "class": html.unescape(html.unescape(t.get("class", "") or "")),
                             "description": html.unescape(html.unescape(t.get("description") or ""))})
    if len(batch) < 500:
        break
    offset += 500
UOUT = SUITE / "reference_data" / "wiki_uniques.json"
UOUT.write_text(json.dumps({"fetched": datetime.date.today().isoformat(),
    "note": "all poewiki uniques (name/class/description); supplement for non-equipment "
            "uniques absent from PoB's DB. Mods would need items.stat_text (heavier).",
    "count": len(urows), "items": sorted(urows, key=lambda r: r["name"])},
    indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(urows)} wiki uniques -> {UOUT}")

rows.sort(key=lambda r: r["name"])
OUT.write_text(json.dumps({
    "fetched": datetime.date.today().isoformat(),
    "source": "poewiki cargo API (items.name/class/description; classes: %s)" % ", ".join(CLASSES),
    "count": len(rows), "items": rows,
}, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(rows)} currency items -> {OUT}")
