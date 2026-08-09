"""Find spectres that cast AURAS -- the buffs that live in skillList, not in mods.

The `grants:` column of the text lake only captures mod()/flag() entries, so a sweep
for PlayerModifier/MinionModifier/AllyModifier structurally cannot find aura-granting
spectres (Guardian Turtle's Determination, Forest Tiger's Haste). This closes that gap:
collect every skill flagged SkillType.Aura in PoB's skill data, then report which
spectres list one.
"""
import re
from pathlib import Path

POB = Path(r"c:/Users/charl/OneDrive/tools/poe_mcp_suite/PathOfBuilding/src/Data/Skills")
LAKE = Path(r"c:/Users/charl/OneDrive/tools/poe_mcp_suite/reference_data/text_lake/spectres.txt")

# 1. Every skill id whose definition flags SkillType.Aura, plus its display name.
aura = {}
for f in POB.glob("*.lua"):
    src = f.read_text(encoding="utf-8", errors="replace")
    for m in re.finditer(r'skills\["([^"]+)"\]\s*=\s*\{', src):
        sid = m.group(1)
        # scan forward to the next skill definition (or 4000 chars, whichever first)
        nxt = src.find('skills["', m.end())
        block = src[m.end(): nxt if nxt != -1 else m.end() + 4000]
        if "SkillType.Aura" in block:
            nm = re.search(r'name\s*=\s*"([^"]+)"', block)
            aura[sid] = nm.group(1) if nm else sid

print("aura-flagged skills in PoB data: %d" % len(aura))

# 2. Which spectres list one? Report corpse (buyable) spectres separately.
rows = []
for line in LAKE.read_text(encoding="utf-8").splitlines():
    parts = line.split("\t")
    if len(parts) < 7:
        continue
    name, meta, skills_col = parts[1], parts[2], parts[5]
    skills = skills_col.replace("skills:", "").split(",")
    hits = sorted({aura[s] for s in skills if s in aura})
    if hits:
        rows.append((("CORPSE " if "SpecialCorpses" in meta else "wild   "), name, hits))

rows.sort(key=lambda r: (r[0], r[1]))
print("spectres casting at least one aura: %d\n" % len(rows))
for tag, name, hits in rows:
    print("%s %-34s %s" % (tag, name, ", ".join(hits)))
