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
UNIQ_META = re.compile(
    r"^(Requires Level |LevelReq:|Implicits:|Source:|Upgrade:|League:|"
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
  - uniques.txt: name, base, source-file, mods (ALL variants kept, {{variant:N}} markers
    retained, legend appended as {{variants: ...}}; metadata lines stripped)
  - gems.txt: kind, name, tagString, variantId (per-level stat text is runtime-only —
    use pob-mcp get_gem_detail)

| file | lines |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in counts.items()) + "\n"
    (OUT / "MANIFEST.md").write_text(manifest, encoding="utf-8")
    print(f"  MANIFEST.md written -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
