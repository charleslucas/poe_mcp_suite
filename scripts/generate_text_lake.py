#!/usr/bin/env python3
"""Generate the local text lake — grep-able flat-text corpus of PoE game text.

Parses the PathOfBuilding submodule's data files and emits one line-oriented
text file per category under reference_data/text_lake/ so that a single Grep
can exhaustively sweep "everything <concept>-related" across categories.

LEGAL (legal_considerations.md): the OUTPUT contains expressive game content
(unique mod text, node stat text) and is LOCAL-ONLY — reference_data/* is
gitignored; never commit or publish the lake. This script (our code) is
committable.

Usage:  python scripts/generate_text_lake.py [--tree-version 3_28]
"""

import argparse
import datetime
import re
import sys
from pathlib import Path

SUITE = Path(__file__).resolve().parent.parent
POB = SUITE / "PathOfBuilding" / "src"
OUT = SUITE / "reference_data" / "text_lake"

# ---------------------------------------------------------------- Lua parser
# Minimal recursive-descent parser for PoB's machine-generated Lua tables.
# Handles: {..}, ["key"]=, bareword=, "strings" (with escapes), numbers,
# true/false/nil, comments. Tables come back as dicts (positional entries
# under integer keys 1..n).

class LuaParser:
    def __init__(self, text: str):
        self.s = text
        self.i = 0
        self.n = len(text)

    def error(self, msg):
        line = self.s.count("\n", 0, self.i) + 1
        raise ValueError(f"lua parse error line {line}: {msg}")

    def skip_ws(self):
        while self.i < self.n:
            c = self.s[self.i]
            if c in " \t\r\n":
                self.i += 1
            elif self.s.startswith("--", self.i):
                j = self.s.find("\n", self.i)
                self.i = self.n if j < 0 else j + 1
            else:
                return

    def parse(self):
        self.skip_ws()
        if self.s.startswith("return", self.i):
            self.i += 6
        return self.parse_value()

    def parse_value(self):
        self.skip_ws()
        c = self.s[self.i]
        if c == "{":
            return self.parse_table()
        if c == '"':
            return self.parse_string()
        if c == "-" or c.isdigit():
            return self.parse_number()
        m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", self.s[self.i:])
        if m:
            w = m.group(0)
            self.i += len(w)
            if w == "true":
                return True
            if w == "false":
                return False
            if w == "nil":
                return None
            self.error(f"unexpected word {w!r}")
        self.error(f"unexpected char {c!r}")

    def parse_table(self):
        self.i += 1  # {
        d, pos = {}, 0
        while True:
            self.skip_ws()
            if self.s[self.i] == "}":
                self.i += 1
                return d
            if self.s[self.i] == "[":
                self.i += 1
                self.skip_ws()
                key = self.parse_string() if self.s[self.i] == '"' else self.parse_number()
                self.skip_ws()
                if self.s[self.i] != "]":
                    self.error("expected ]")
                self.i += 1
                self.skip_ws()
                if self.s[self.i] != "=":
                    self.error("expected = after key")
                self.i += 1
                d[key] = self.parse_value()
            else:
                m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*=", self.s[self.i:])
                if m and m.group(1) not in ("true", "false", "nil"):
                    self.i += m.end()
                    d[m.group(1)] = self.parse_value()
                else:
                    pos += 1
                    d[pos] = self.parse_value()
            self.skip_ws()
            if self.i < self.n and self.s[self.i] in ",;":
                self.i += 1

    def parse_string(self):
        self.i += 1  # opening quote
        out = []
        while True:
            c = self.s[self.i]
            if c == "\\":
                nxt = self.s[self.i + 1]
                out.append({"n": "\n", "t": "\t", "r": "\r"}.get(nxt, nxt))
                self.i += 2
            elif c == '"':
                self.i += 1
                return "".join(out)
            else:
                out.append(c)
                self.i += 1

    def parse_number(self):
        m = re.match(r"-?\d+\.?\d*(?:[eE][+-]?\d+)?", self.s[self.i:])
        if not m:
            self.error("bad number")
        self.i += m.end()
        t = m.group(0)
        return float(t) if ("." in t or "e" in t or "E" in t) else int(t)


def lua_list(d):
    """Positional entries of a parsed table, in order."""
    if not isinstance(d, dict):
        return []
    return [d[k] for k in sorted(k for k in d if isinstance(k, int))]


def one_line(s):
    return re.sub(r"\s*\n\s*", " / ", s.strip())


# ---------------------------------------------------------------- passives
def gen_passives(tree_version):
    tree_file = POB / "TreeData" / tree_version / "tree.lua"
    tree = LuaParser(tree_file.read_text(encoding="utf-8")).parse()
    nodes = tree.get("nodes", {})
    # The tree contains many identical instances of masteries/small nodes at
    # different locations — dedupe by content, aggregating node IDs.
    agg = {}  # (ntype, name, asc, stats) -> [ids]
    for key, node in nodes.items():
        if not isinstance(node, dict) or "name" not in node:
            continue
        name = node["name"]
        if node.get("isProxy"):
            continue
        asc = node.get("ascendancyName", "")
        if node.get("isKeystone"):
            ntype = "KEYSTONE"
        elif node.get("isMastery"):
            ntype = "MASTERY"
        elif node.get("isNotable"):
            ntype = "NOTABLE"
        elif node.get("isJewelSocket"):
            ntype = "JEWELSOCKET"
        elif node.get("isMultipleChoiceOption"):
            ntype = "CHOICE"
        else:
            ntype = "SMALL"
        if asc:
            ntype = "ASC-" + ntype
        stats = [one_line(s) for s in lua_list(node.get("stats", {}))]
        # Mastery nodes carry their effects separately
        for eff in lua_list(node.get("masteryEffects", {})):
            stats.extend(one_line(s) for s in lua_list(eff.get("stats", {})))
        nid = node.get("skill", key)
        agg.setdefault((ntype, name, asc or "-", " | ".join(stats)), []).append(nid)
    lines = []
    for (ntype, name, asc, statstr), ids in agg.items():
        shown = ",".join(f"#{i}" for i in sorted(ids)[:3])
        if len(ids) > 3:
            shown += f" (+{len(ids) - 3} more)"
        lines.append(f"{ntype}\t{name}\t{asc}\t{shown}\t{statstr}")
    lines.sort()
    return lines


# ---------------------------------------------------------------- uniques
# NOTE: "Requires Level"/"LevelReq" are deliberately KEPT (useful for leveling-gear
# sweeps; their absence caused a stale-req error on 2026-07-18).
UNIQ_META = re.compile(
    r"^(Implicits:|Source:|Upgrade:|League:|"
    r"Selected Variant|Selected Alt Variant|Has Alt Variant|Variant: )"
)
BLOCK = re.compile(r"\[\[(.*?)\]\]", re.DOTALL)


def gen_uniques():
    lines = []
    files = sorted((POB / "Data" / "Uniques").glob("*.lua"))
    files += sorted((POB / "Data" / "Uniques" / "Special").glob("*.lua"))
    for f in files:
        src = f.stem
        for m in BLOCK.finditer(f.read_text(encoding="utf-8")):
            raw = [ln.strip() for ln in m.group(1).strip().splitlines() if ln.strip()]
            if len(raw) < 2:
                continue
            name, base = raw[0], raw[1]
            variants = [ln[len("Variant: "):] for ln in raw if ln.startswith("Variant: ")]
            mods = [ln for ln in raw[2:] if not UNIQ_META.match(ln)]
            vnote = f" {{variants: {'; '.join(variants)}}}" if variants else ""
            lines.append(f"{name}\t{base}\t{src}\t" + " | ".join(mods) + vnote)
    lines.sort()
    return lines


# ---------------------------------------------------------------- gems
def gen_gems():
    gems = LuaParser((POB / "Data" / "Gems.lua").read_text(encoding="utf-8")).parse()
    lines = []
    for gid, g in gems.items():
        if not isinstance(g, dict) or "name" not in g:
            continue
        kind = "SUPPORT" if g.get("tags", {}).get("support") else "ACTIVE"
        if g.get("vaalGem"):
            kind += "-VAAL"
        lines.append(
            f"{kind}\t{g['name']}\t{g.get('tagString', '')}\t{g.get('variantId', '')}"
        )
    lines.sort(key=lambda x: x.split("\t")[1])
    return lines


# ---------------------------------------------------------------- mods
# Craftable/rollable affix pools. These live in Data/Mod*.lua — NOT in the
# passives/uniques/gems the other categories index — so "cannot deal X",
# "Minions convert fire to chaos", corrupted/scourge/eldritch enablers etc.
# are only greppable here. Deduped by the game's own tier `group` (one line per
# mod family, highest-tier text kept). ModItemExclusive (unique-only mods) is
# skipped — already covered by uniques.txt; ModCache is derived — skipped.
MOD_FILES = [
    "ModExplicit", "ModImplicit", "ModCorrupted", "ModEldritch", "ModScourge",
    "ModVeiled", "ModDelve", "ModSynthesis", "ModFoulborn", "ModMaster",
    "ModTincture", "ModJewel", "ModJewelAbyss",
]


def gen_mods():
    seen = {}  # (file, group, type) -> aggregate
    for fname in MOD_FILES:
        path = POB / "Data" / f"{fname}.lua"
        if not path.exists():
            continue
        data = LuaParser(path.read_text(encoding="utf-8")).parse()
        for _, m in data.items():
            if not isinstance(m, dict):
                continue
            texts = [m[k] for k in sorted(k for k in m if isinstance(k, int))]
            texts = [one_line(t) for t in texts if isinstance(t, str) and t.strip()]
            if not texts:
                continue
            text = " | ".join(texts)
            atype = m.get("type", "") or "-"
            group = m.get("group") or text  # tier family; fall back to text
            wk = lua_list(m.get("weightKey", {}))
            wv = lua_list(m.get("weightVal", {}))
            classes = {k for k, v in zip(wk, wv)
                       if isinstance(v, (int, float)) and v > 0 and k != "default"}
            tags = set(lua_list(m.get("modTags", {})))
            lvl = m.get("level", 0) or 0
            key = (fname, group, atype)
            agg = seen.get(key)
            if agg is None:
                seen[key] = {"text": text, "type": atype, "classes": set(classes),
                             "tags": set(tags), "tiers": 1, "lvl": lvl}
            else:
                agg["tiers"] += 1
                agg["classes"].update(classes)
                agg["tags"].update(tags)
                if lvl > agg["lvl"]:  # keep highest-tier text as representative
                    agg["lvl"], agg["text"] = lvl, text
    lines = []
    for (fname, _group, _atype), a in seen.items():
        cls = ",".join(sorted(a["classes"])) if a["classes"] else "any"
        tg = ",".join(sorted(a["tags"])) if a["tags"] else "-"
        src = fname.replace("Mod", "", 1)
        lines.append(f"{src}\t{a['type']}\t{a['text']}\t[{cls}]\t{{{tg}}}\t{a['tiers']}t")
    lines.sort(key=lambda x: (x.split("\t")[0], x.split("\t")[2]))
    return lines


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree-version", default=None,
                    help="TreeData dir (default: latest numeric, no suffix)")
    args = ap.parse_args()

    tree_version = args.tree_version
    if not tree_version:
        cands = [d.name for d in (POB / "TreeData").iterdir()
                 if re.fullmatch(r"\d+_\d+", d.name)]
        tree_version = max(cands, key=lambda v: tuple(map(int, v.split("_"))))

    OUT.mkdir(parents=True, exist_ok=True)
    counts = {}
    for fname, gen in [
        ("passives.txt", lambda: gen_passives(tree_version)),
        ("uniques.txt", gen_uniques),
        ("gems.txt", gen_gems),
        ("mods.txt", gen_mods),
    ]:
        lines = gen()
        (OUT / fname).write_text("\n".join(lines) + "\n", encoding="utf-8")
        counts[fname] = len(lines)
        print(f"  {fname}: {len(lines)} lines")

    stamp = datetime.date.today().isoformat()
    manifest = f"""# Text Lake — MANIFEST

**LOCAL-ONLY — never commit/publish** (expressive game content; see legal_considerations.md).
Regenerate: `python scripts/generate_text_lake.py` (re-run after every PoB submodule update).

- generated: {stamp}
- tree version: {tree_version} (PoB TreeData; 'alternate'/'ruthless' variants excluded)
- source: PathOfBuilding submodule @ src/Data + src/TreeData
- format: tab-separated fields, one entity per line, stats joined with " | "
  - passives.txt: TYPE, name, ascendancy, #id, stats (masteries include all effects)
    SCOPE WARNING: PoB's tree data bundles EVENT/ALTERNATE ascendancies alongside core
    ones (e.g. Catarina, Farrul, Aul, Olroth, Warlock, Primalist...). Before recommending
    any ASC-* node, verify its ascendancy is live in the target league (core classes +
    current-league additions only) — cf. mechanics_index scope-tagging.
    ANOINT-ONLY WARNING: some NOTABLE rows are anoint-only nodes that do NOT physically
    exist on the tree (e.g. Hollow Effigy) — tree data doesn't distinguish them. Before
    treating a notable as allocatable, verify placement (get_tree_node / poedb).
  - uniques.txt: name, base, source-file, mods (ALL variants kept, {{variant:N}} markers
    retained, legend appended as {{variants: ...}}; level-req lines KEPT; other metadata stripped)
    REBASED-UNIQUE WARNING: the base column shows the FIRST base listed — for uniques whose
    base changed across patches (e.g. Ashcaller Quartz Wand -> Goat's Horn) that is the
    LEGACY base; the current base appears among the {{variant:N}}-marked lines. Trade-search
    rebased uniques by NAME, not base.
  - gems.txt: kind, name, tagString, variantId (per-level stat text is runtime-only —
    use pob-mcp get_gem_detail)
  - mods.txt: source, affix-type, mod text, [item classes it can roll on], {{modTags}}, tierCount
    Rollable/craftable AFFIX pools (Explicit/Implicit/Corrupted/Eldritch/Scourge/Veiled/Delve/
    Synthesis/Foulborn/Master/Tincture/Jewel/JewelAbyss). Deduped by the game's tier `group`
    (one line per mod family; highest-tier text shown — exact per-tier values via
    search_crafting_mods / craftofexile). This is where "cannot deal X", corrupted-implicit and
    league-mechanic enablers live — they are NOT in uniques/passives/gems. ⚠ SCOPE: includes
    league-mechanic mod pools (Scourge/Synthesis/Delve/Foulborn/Eldritch) that may not be
    obtainable in the current league — verify availability. ModItemExclusive (unique-only mods)
    excluded (covered by uniques.txt); numeric values are the top tier only.

| file | lines |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in counts.items()) + "\n"
    (OUT / "MANIFEST.md").write_text(manifest, encoding="utf-8")
    print(f"  MANIFEST.md written -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
