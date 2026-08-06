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


# ---------------------------------------------------------------- atlas tree
# ATLAS passive tree — keystones (Synthesised Stability...), notables, smalls. Absent
# from the lake until 2026-08-05: gen_passives reads the CHARACTER tree only, and the
# atlas tree lives in reference_data/atlastree/data.json (GGG's own export, mirrored in
# the poe-atlastree-export fork) — a source this generator never touched. Found when
# "Synthesised Stability" — load-bearing for a farming strategy — was ungreppable.
#
# NOTE the astrolabe CONSUMABLES themselves (the 10 varieties and their Shaped-Region
# mod pools) exist in NO local source — not PoB's data, not the atlas export. Like
# rare-monster mods: wiki/community only. Documented in the MANIFEST.

def gen_atlas():
    import json as _json
    f = SUITE / "reference_data" / "atlastree" / "data.json"
    if not f.exists():
        return []
    nodes = _json.loads(f.read_text(encoding="utf-8")).get("nodes", {})
    agg = {}
    for key, node in nodes.items():
        if not isinstance(node, dict) or "name" not in node:
            continue
        if node.get("isKeystone"): ntype = "ATLAS-KEYSTONE"
        elif node.get("isNotable"): ntype = "ATLAS-NOTABLE"
        elif node.get("isMastery"): ntype = "ATLAS-MASTERY"
        elif node.get("isWormholeRelated") or node.get("isJewelSocket"): ntype = "ATLAS-SOCKET"
        else: ntype = "ATLAS-SMALL"
        stats = [one_line(x) for x in lua_list(node.get("stats", {}))] if not isinstance(node.get("stats"), list) else [one_line(x) for x in node.get("stats", [])]
        nid = node.get("skill", key)
        agg.setdefault((ntype, node["name"], " | ".join(stats)), []).append(nid)
    lines = []
    for (ntype, name, statstr), ids in agg.items():
        shown = ",".join(f"#{i}" for i in sorted(ids)[:3])
        if len(ids) > 3:
            shown += f" (+{len(ids)-3} more)"
        lines.append(f"{ntype}	{name}	{shown}	{statstr}")
    lines.sort()
    return lines


# ---------------------------------------------------------------- bases
# Item BASE data: implicits and base-type properties. Data/Bases/*.lua was read ZERO
# times by this generator until 2026-08-03, so the lake could not answer "what implicit
# does this base have?" at all.
#
# The case that exposed it: the Granite Flask's "+1500 to Armour" is a BASE-TYPE
# property (flask.buff), not an implicit and not an explicit — it appears in no mod
# pool. It turned out to be the single most important defensive number on a character,
# and had to be grepped straight out of the submodule because the lake had nothing.
#
# These files are statements (`itemBases["X"] = {...}`), not a returned table, so we
# locate each assignment and parse the table literal that follows.

_BASE_ASSIGN = re.compile(r'itemBases\[\s*"([^"]+)"\s*\]\s*=\s*(?=\{)')


def gen_bases():
    lines = []
    for f in sorted((POB / "Data" / "Bases").glob("*.lua")):
        src = f.read_text(encoding="utf-8")
        for m in _BASE_ASSIGN.finditer(src):
            name = m.group(1)
            try:
                base = LuaParser(src[m.end():]).parse()
            except Exception:
                continue
            if not isinstance(base, dict):
                continue
            itype = base.get("type", "?")
            sub = base.get("subType", "") or "-"
            req = base.get("req") or {}
            lvl = req.get("level", 0) if isinstance(req, dict) else 0

            # Base-type properties that read as stats to a player but live nowhere else.
            props = []
            imp = base.get("implicit")
            if isinstance(imp, str) and imp.strip():
                props.append("IMPLICIT: " + one_line(imp))
            fl = base.get("flask")
            if isinstance(fl, dict):
                for b in lua_list(fl.get("buff", {})):
                    if isinstance(b, str):
                        props.append("FLASK-BUFF: " + one_line(b))
                bits = []
                for k, label in (("life", "life"), ("mana", "mana"), ("duration", "duration"),
                                 ("chargesUsed", "chargesUsed"), ("chargesMax", "chargesMax")):
                    if fl.get(k) is not None:
                        bits.append(f"{label}={fl[k]}")
                if bits:
                    props.append("FLASK: " + ", ".join(bits))
            if not props:
                continue  # plain stat-stick bases add noise, not searchable text
            lines.append(f"BASE\t{itype}\t{name}\t{sub}\treq{lvl}\t{' | '.join(props)}")
    lines.sort()
    return lines


# ---------------------------------------------------------------- map mods
# Map modifiers — CORE content, and the input to any map-mod blacklist (see
# playbooks/atlas-planning.md). Absent from the lake until 2026-08-03.
#
# ModMap.lua embeds `apply = function(...) ... end` bodies, so LuaParser (tables/strings/
# numbers only) cannot read it. The searchable content is the affix name, the GUI label and
# tooltipLines, so those are extracted directly. printf escapes are normalised for grep:
# `%d%%` -> `N%`, so "+%d%% Monster Physical Damage Reduction" becomes a line a human would
# actually search for.

_MAPMOD_BLOCK = re.compile(
    r'\["([^"]+)"\]\s*=\s*\{(.*?)\n\t\t\}', re.DOTALL)
_MAPMOD_TIP = re.compile(r'"((?:[^"\\]|\\.)*)"')


def _fmt_printf(s):
    return (s.replace("%d%%", "N%").replace("%d", "N")
             .replace("%%", "%").replace("\\n", " / "))


def _balanced_braces(text, start):
    """Return the contents of the {...} beginning at/after `start`, brace-matched.
    A plain `\\{([^}]*)\\}` regex truncates nested value tables like { {20,29}, {30,39} }."""
    i = text.find("{", start)
    if i < 0:
        return ""
    depth, j = 0, i
    while j < len(text):
        if text[j] == "{":
            depth += 1
        elif text[j] == "}":
            depth -= 1
            if depth == 0:
                return text[i + 1:j]
        j += 1
    return ""


def gen_mapmods():
    f = POB / "Data" / "ModMap.lua"
    if not f.exists():
        return []
    src = f.read_text(encoding="utf-8")
    lines = []
    for m in _MAPMOD_BLOCK.finditer(src):
        name, body = m.group(1), m.group(2)
        lab = re.search(r'label\s*=\s*"((?:[^"\\]|\\.)*)"', body)
        tip_at = body.find("tooltipLines")
        val_at = body.find("values")
        texts = []
        if tip_at >= 0:
            texts = [_fmt_printf(t)
                     for t in _MAPMOD_TIP.findall(_balanced_braces(body, tip_at))
                     if t.strip()]
        if not texts and lab:
            texts = [_fmt_printf(lab.group(1))]
        if not texts:
            continue
        vtxt = "-"
        if val_at >= 0:
            raw = _balanced_braces(body, val_at)
            nums = re.findall(r'-?\d+(?:\.\d+)?', raw)
            vtxt = ",".join(nums) if nums else "-"
        lines.append(f"MAPMOD\t{name}\t{vtxt}\t{' | '.join(texts)}")
    lines.sort()
    return lines


# ---------------------------------------------------------------- essences
# Essence.lua stores mod IDs per item class (`["Helmet"] = "ColdResist3"`), NOT text, which
# is why it was skipped in the first pass — grepping it for "cold resistance" finds nothing.
# Every ID resolves against ModExplicit (verified 622/622), so we resolve them here and emit
# the guaranteed mod TEXT, which is the thing anyone actually searches for.
#
# Emitted per (essence, mod-text) rather than per (essence, slot): one essence typically maps
# many slots onto the same handful of mods, so slot-per-line would be ~20x the rows for no
# extra searchable content. Slots are listed in the row instead.

def _explicit_mod_text_by_id():
    """id -> human-readable mod text, from ModExplicit."""
    data = LuaParser((POB / "Data" / "ModExplicit.lua").read_text(encoding="utf-8")).parse()
    out = {}
    if not isinstance(data, dict):
        return out
    for mid, m in data.items():
        if not isinstance(m, dict):
            continue
        texts = [m[k] for k in sorted(k for k in m if isinstance(k, int))]
        texts = [one_line(t) for t in texts if isinstance(t, str) and t.strip()]
        if texts:
            out[mid] = " / ".join(texts)
    return out


def gen_essences():
    f = POB / "Data" / "Essence.lua"
    if not f.exists():
        return []
    by_id = _explicit_mod_text_by_id()
    data = LuaParser(f.read_text(encoding="utf-8")).parse()
    if not isinstance(data, dict):
        return []
    lines = []
    for _, ess in data.items():
        if not isinstance(ess, dict):
            continue
        name = ess.get("name", "?")
        tier = ess.get("tier", "?")
        mods = ess.get("mods")
        if not isinstance(mods, dict):
            continue
        # group slots by the mod text they grant
        by_text = {}
        for slot, mid in mods.items():
            if not isinstance(mid, str):
                continue
            text = by_id.get(mid)
            if text:
                by_text.setdefault(text, []).append(str(slot))
        for text, slots in by_text.items():
            lines.append(f"ESSENCE\t{name}\ttier{tier}\t{','.join(sorted(slots))}\t{text}")
    lines.sort()
    return lines


# ---------------------------------------------------------------- enchants + pantheon
# Lab/Instilling enchants and pantheon god powers. Both absent until 2026-08-03.
# The pantheon gap was felt directly: identifying Soul of Ralakesh as the bleed/phys-DoT
# god required grepping Pantheons.lua out of the submodule, because the lake had nothing.

ENCHANT_FILES = ["EnchantmentHelmet", "EnchantmentBoots", "EnchantmentGloves",
                 "EnchantmentBody", "EnchantmentBelt", "EnchantmentWeapon", "EnchantmentFlask"]


def gen_enchants():
    lines = []
    for fname in ENCHANT_FILES:
        path = POB / "Data" / f"{fname}.lua"
        if not path.exists():
            continue
        slot = fname.replace("Enchantment", "")
        data = LuaParser(path.read_text(encoding="utf-8")).parse()
        if not isinstance(data, dict):
            continue
        for skill, tiers in data.items():
            if not isinstance(tiers, dict):
                continue
            for tier, texts in tiers.items():
                for t in lua_list(texts) if isinstance(texts, dict) else []:
                    if isinstance(t, str) and t.strip():
                        lines.append(f"ENCHANT\t{slot}\t{skill}\t{tier}\t{one_line(t)}")
    lines.sort()
    return lines


def gen_pantheon():
    f = POB / "Data" / "Pantheons.lua"
    if not f.exists():
        return []
    data = LuaParser(f.read_text(encoding="utf-8")).parse()
    lines = []
    if not isinstance(data, dict):
        return []
    for key, god in data.items():
        if not isinstance(god, dict):
            continue
        kind = "MAJOR" if god.get("isMajorGod") else "MINOR"
        for soul in lua_list(god.get("souls", {})):
            if not isinstance(soul, dict):
                continue
            sname = soul.get("name", "?")
            mods = [one_line(m["line"]) for m in lua_list(soul.get("mods", {}))
                    if isinstance(m, dict) and isinstance(m.get("line"), str)]
            if mods:
                lines.append(f"PANTHEON\t{kind}\t{key}\t{sname}\t{' | '.join(mods)}")
    lines.sort()
    return lines


# ---------------------------------------------------------------- spectres
# The full raisable-monster roster. Absent from the lake until 2026-08-03 despite being
# the single largest body of minion-relevant text in PoB's data (~325 minion/spectre
# lines), which made "which spectre should I use?" unanswerable by a sweep.
#
# Emits the searchable dimensions: display name, monster tags (how you actually filter —
# "undead", "ranged", "caster"...), and the skill list (what the spectre DOES). Numeric
# multipliers (life/damage/resists) are included compactly because spectre choice is
# usually a durability-vs-damage tradeoff.

_MINION_ASSIGN = re.compile(r'minions\[\s*"([^"]+)"\s*\]\s*=\s*(?=\{)')


def gen_spectres():
    f = POB / "Data" / "Spectres.lua"
    if not f.exists():
        return []
    src = f.read_text(encoding="utf-8")
    lines = []
    for m in _MINION_ASSIGN.finditer(src):
        meta = m.group(1)
        try:
            mon = LuaParser(src[m.end():]).parse()
        except Exception:
            continue
        if not isinstance(mon, dict):
            continue
        name = mon.get("name", "?")
        tags = ",".join(str(t) for t in lua_list(mon.get("monsterTags", {})))
        skills = ",".join(str(s) for s in lua_list(mon.get("skillList", {})))
        stats = []
        for k, label in (("life", "life"), ("damage", "dmg"), ("attackTime", "atkTime"),
                         ("fireResist", "fireRes"), ("coldResist", "coldRes"),
                         ("lightningResist", "lightRes"), ("chaosResist", "chaosRes")):
            v = mon.get(k)
            if v is not None:
                stats.append(f"{label}={v}")
        lines.append(
            f"SPECTRE\t{name}\t{meta}\t{', '.join(stats)}\ttags:{tags}\tskills:{skills}"
        )
    lines.sort()
    return lines


# ---------------------------------------------------------------- clusters
# Cluster jewel SMALL-passive skills live ONLY in Data/ClusterJewels.lua — they are
# NOT in TreeData/*/tree.lua, so gen_passives() never saw them. Cluster NOTABLES are
# in the tree node list and therefore already covered by passives.txt; this file
# deliberately does not duplicate them (it cross-references instead).
#
# Found 2026-08-03: a sweep for "what can a cluster jewel small passive grant?"
# returned ZERO hits across the whole lake and read as a confident absence.

def gen_clusters():
    f = POB / "Data" / "ClusterJewels.lua"
    data = LuaParser(f.read_text(encoding="utf-8")).parse()
    lines = []

    # SMALL rows: one per (jewel size, skill). The enchant is the searchable text
    # players actually see on the jewel; stats are what each added small grants.
    for jname, jewel in (data.get("jewels") or {}).items():
        if not isinstance(jewel, dict):
            continue
        size = jewel.get("size", "?")
        for tag, skill in (jewel.get("skills") or {}).items():
            if not isinstance(skill, dict):
                continue
            stats = " | ".join(one_line(s) for s in lua_list(skill.get("stats", {})))
            ench = " | ".join(one_line(s) for s in lua_list(skill.get("enchant", {})))
            lines.append(
                f"CLUSTER-SMALL\t{size}\t{skill.get('name', '?')}\t{tag}\t{ench}\t{stats}"
            )

    # Cluster-only keystones (large jewels can roll these; names only in this file).
    for ks in lua_list(data.get("keystones", {})):
        if isinstance(ks, str):
            lines.append(f"CLUSTER-KEYSTONE\t-\t{ks}\t-\t-\tsee passives.txt for stats")

    # Notable NAME index only — stats come from the tree (passives.txt).
    for name in sorted(data.get("notableSortOrder") or {}):
        lines.append(
            f"CLUSTER-NOTABLE\t-\t{name}\t-\t-\tstats in passives.txt (NOTABLE {name})"
        )

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
    # ModFlask was missing until 2026-08-03 — every flask prefix/suffix (Flagellant's,
    # Bubbling, Seething, of Staunching, the armour/evasion "during Effect" suffixes)
    # was absent from the lake, so a whole gear slot's mod pool had to be grepped out of
    # the submodule by hand. ModJewelCluster covers cluster jewels' OWN explicits (e.g.
    # "Added Small Passive Skills have N% increased Effect"), distinct from the small
    # passives themselves in clusters.txt.
    "ModFlask", "ModJewelCluster",
    # Added 2026-08-03. All verified mod-shaped before inclusion. The `source` column IS
    # the scope marker — a `ModNecropolis` row is self-labelling as dead-league content,
    # so these are included-and-labelled rather than suppressed (see MANIFEST scope note).
    "ModGraft",        # Runegrafts — core per mechanics_index
    "BeastCraft",      # beastcrafting (Aspect suffixes etc.) — core; Bestiary reworked 3.29
    "ModNecropolis",   # Necropolis (3.24) — verify scope before recommending
    "ModJewelCharm",   # charms — verify scope before recommending
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
        ("atlas.txt", gen_atlas),
        ("clusters.txt", gen_clusters),
        ("bases.txt", gen_bases),
        ("spectres.txt", gen_spectres),
        ("enchants.txt", gen_enchants),
        ("essences.txt", gen_essences),
        ("mapmods.txt", gen_mapmods),
        ("pantheon.txt", gen_pantheon),
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
- source: PathOfBuilding submodule @ src/Data + src/TreeData + src/Data/ClusterJewels.lua

## ⚠️ STILL NOT EXHAUSTIVE — remaining source gaps (audited + largely closed 2026-08-03)

A sweep of this lake is close to, but not yet, a complete sweep of the game. For the sources
below, grepping the lake returns a FALSE NEGATIVE. Until they are added, also grep the
submodule directly: `rg -i "<topic>" PathOfBuilding/src/Data/`

| Still missing | Why it matters | Why not done |
|---|---|---|
| `Crucible.lua` | Crucible weapon-tree mods | `disabled-this-league` per mechanics_index — would be pure false positives |
| `TattooPassives.lua` | Forbidden Tattoos | `event-only` per mechanics_index — not available in a normal league |
| `ModFoulbornMap.lua` | Foulborn *map* mods | base `ModFoulborn` pool is already in mods.txt; map-specific variant not yet needed |

⚠️ **`Rares.lua` is NOT rare-MONSTER mods** — it is PoB's pre-made *rare item templates* for build planning
(named items with prefix/suffix mod IDs). It was listed as a gap on 2026-08-03 based on the filename; that was
wrong. Its mods are already covered by mods.txt, so it is deliberately excluded, not missing.

**PoB ships no rare-monster modifier pool at all.** "Which monster mods one-shot me?" is therefore NOT
answerable from this lake or from PoB — it needs the wiki or a community survey. Don't hunt for it here.

**Closed 2026-08-03** (were false negatives before that date — treat any earlier "found nothing"
conclusion on these topics as unreliable): `Data/Bases/*.lua` → **bases.txt**; `Spectres.lua` →
**spectres.txt**; `Enchantment*.lua` → **enchants.txt**; `Pantheons.lua` → **pantheon.txt**;
`Essence.lua` → **essences.txt**; `ModMap.lua` → **mapmods.txt**; `ClusterJewels.lua` →
**clusters.txt**; `ModFlask`, `ModJewelCluster`, `ModGraft`, `BeastCraft`, `ModNecropolis`,
`ModJewelCharm` → folded into **mods.txt**.

**Scope handling for league pools:** mods.txt's first column is the SOURCE, which doubles as the
scope marker. ⚠ It is the file name with the `Mod` prefix STRIPPED — grep `^Necropolis`, not
`^ModNecropolis`. Current values: Explicit, Eldritch, Synthesis, Scourge, JewelCluster, Jewel,
Foulborn, JewelAbyss, Master, Corrupted, Veiled, Graft, Delve, JewelCharm, Flask, Necropolis,
Tincture, BeastCraft. A `Necropolis` or `Scourge` row is self-labelling as league content. Dead
leagues are therefore *included and labelled* rather than suppressed, so a sweep still surfaces them
(useful history / Standard characters) while making their provenance obvious. **Always scope-check a
league-pool hit against `reference_data/mechanics_index.md` before recommending it.** The two pools
excluded outright (`Crucible`, `TattooPassives`) are the ones where mechanics_index already says
`disabled-this-league` / `event-only`, i.e. guaranteed false positives today.

Deliberately excluded (no mechanical value or redundant): `ModScalability`, `QueryMods`,
`TradeSiteStats` (trade indexes, ~5MB combined), `FlavourText` (lore), `SkillStatMap`,
`Costs`, `Global`, `Misc`, `Bosses`, `BossSkills`.
- format: tab-separated fields, one entity per line, stats joined with " | "
  - passives.txt: TYPE, name, ascendancy, #id, stats (masteries include all effects)
    SCOPE WARNING: PoB's tree data bundles EVENT/ALTERNATE ascendancies alongside core
    ones (e.g. Catarina, Farrul, Aul, Olroth, Warlock, Primalist...). Before recommending
    any ASC-* node, verify its ascendancy is live in the target league (core classes +
    current-league additions only) — cf. mechanics_index scope-tagging.
    ANOINT-ONLY WARNING: some NOTABLE rows are anoint-only nodes that do NOT physically
    exist on the tree (e.g. Hollow Effigy) — tree data doesn't distinguish them. Before
    treating a notable as allocatable, verify placement (get_tree_node / poedb).
    CLUSTER NOTE: cluster-jewel NOTABLES are in the tree node list, so they ARE here.
    Cluster SMALL passives are NOT — they live only in ClusterJewels.lua → clusters.txt.
  - bases.txt: BASE, item type, base name, subType, req level, properties
    Item-BASE implicits AND base-type properties. The latter exist in NO mod pool — e.g. a
    Granite Flask's `+1500 to Armour` is `FLASK-BUFF`, not an implicit or explicit. Rows with
    no implicit/flask text are omitted (plain stat-stick bases are noise). Armour/evasion/ES
    and weapon numbers are NOT emitted — use pob-mcp item tools for those.
  - spectres.txt: SPECTRE, display name, metadata path, stat multipliers, tags, skill list
    The raisable-monster roster. `tags:` is how you actually filter (undead / ranged / caster);
    `skills:` is what it DOES. Numbers are PoB's multipliers, not absolute values.
  - mapmods.txt: MAPMOD, affix name, tier values, tooltip text
    MAP MODIFIERS — the input to a map-mod blacklist (playbooks/atlas-planning.md). printf
    escapes normalised for grep (`%d%%` → `N%`), so lines read the way a human searches.
    Extracted by regex, not LuaParser: ModMap.lua embeds `apply = function(...)` bodies.
  - essences.txt: ESSENCE, essence name, tier, applicable slots, GUARANTEED mod text
    Essence.lua stores mod IDs, not text — these are resolved through ModExplicit so the row
    carries the searchable text. One row per (essence, distinct mod); the slots that share that
    mod are listed together rather than duplicated per-slot.
  - enchants.txt: ENCHANT, slot, skill, tier (MERCILESS/ENDGAME), text
    Lab + Instilling enchants across helmet/boots/gloves/body/belt/weapon/flask.
  - pantheon.txt: PANTHEON, MAJOR/MINOR, god key, soul name, granted mods
    Both the base god and its upgrade souls (captured-monster upgrades).
  - atlas.txt: ATLAS-TYPE, name, #id, stats — the ATLAS passive tree (keystones/notables/smalls),
    from reference_data/atlastree/data.json (GGG export). Distinct from passives.txt (character tree).
    ⚠ Astrolabe CONSUMABLES (the 10 varieties + their Shaped-Region mod pools) are in NO local source —
    not PoB's data, not the atlas export. Like rare-monster mods: wiki/community/user only.
  - clusters.txt: kind, jewel-size, name, tag, enchant text, stats
    CLUSTER-SMALL rows are the "Added Small Passive Skills grant: X" pool, keyed by jewel
    size (Small/Medium/Large) — the exhaustive answer to "what can a cluster small give?".
    These exist ONLY in Data/ClusterJewels.lua and were entirely ABSENT from the lake until
    2026-08-03, so any earlier sweep for them returned a false negative.
    CLUSTER-NOTABLE / CLUSTER-KEYSTONE rows are a NAME INDEX only — their stats live in
    passives.txt. Per-size numeric values for a small (they differ Small/Medium/Large) and
    what a specific jewel actually rolled: use pob-mcp search_cluster_jewels /
    list_cluster_jewel_nodes. ⚠ Jewel mods like "Added Small Passive Skills have N% increased
    Effect" scale these — the lake shows BASE values only.
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
