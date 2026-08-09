"""Insert a spectre-buff MODELING socket group into a Path of Building build XML.

Why this exists
---------------
PoB applies a spectre's buffs only when that spectre is the selected minion of a
Raise Spectre skill instance (`CalcPerform.lua:2169` collects `activeSkill.minion.type`
per instance, then applies buffs only for spectres in that list). With one Raise
Spectre gem that is exactly ONE spectre -- every other raised spectre is inert in the
calc, and adding one changes nothing at all, which reads as "no effect" but means
"not selected".

This adds an unassigned, Full-DPS-excluded socket group holding one Raise Spectre gem
per extra spectre, each pinned via the per-gem `skillMinion` attribute, so every raised
spectre's buffs apply at once.

Design notes (each was a failure mode, not a preference)
--------------------------------------------------------
* **Unassigned group** (no `slot=`): weapon-swap groups are inactive while the main
  weapon set is live, so gems parked there contribute nothing.
* **includeInFullDPS="false"**: keeps the fake instances from adding spectre *damage*.
  Verify after loading -- `minion_dps_breakdown` must show exactly ONE Raise Spectre row.
* **Both `skillMinion` and `skillMinionCalcs`** are set; PoB tracks the main and Calcs
  selections separately.
* Metadata ids are NOT guessable ("Perfect Hulking Miscreation" is `RobotArgusHigh__`,
  trailing double underscore). Copy them from `reference_data/text_lake/spectres.txt`.

⚠ A character import replaces skill gems and therefore DESTROYS this group. Re-run it
as part of the post-import checklist.

Usage
-----
    python scripts/pob_spectre_modeling_group.py <build.xml> <metadata_id> [<metadata_id> ...]

Pass the ids of the spectres that are NOT already selected in a real socket group.
Every id passed must also be present in the build's spectre list (`set_spectres`), or
PoB will ignore it.
"""
import sys
from pathlib import Path

LABEL = "SPECTRE BUFF MODELING (not a real link)"

GEM = (
    '\t\t\t\t<Gem nameSpec="Raise Spectre" skillId="RaiseSpectre" count="1"'
    ' enableGlobal1="true" enabled="true" variantId="RaiseSpectre" quality="0"'
    ' skillMinionSkill="1" gemId="Metadata/Items/Gems/SkillGemRaiseSpectre" level="21"'
    ' skillMinionSkillCalcs="1" skillMinionCalcs="{m}" skillMinion="{m}"'
    ' enableGlobal2="false"/>'
)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2

    xml_path = Path(sys.argv[1])
    spectres = sys.argv[2:]

    for m in spectres:
        if not m.startswith("Metadata/Monsters/"):
            print("ERROR: %r is not a metadata id — copy it from the text lake" % m)
            return 1

    text = xml_path.read_text(encoding="utf-8")

    if LABEL in text:
        print("modeling group already present — remove it first to rebuild")
        return 0

    marker = "\t\t</SkillSet>"
    if marker not in text:
        print("ERROR: could not find a SkillSet close marker in %s" % xml_path)
        return 1

    lines = [
        '\t\t\t<Skill mainActiveSkillCalcs="1" includeInFullDPS="false"'
        ' mainActiveSkill="1" label="%s" enabled="true">' % LABEL
    ]
    lines += [GEM.format(m=m) for m in spectres]
    lines.append("\t\t\t</Skill>")
    block = "\n".join(lines) + "\n"

    # First SkillSet only — that is the active one.
    xml_path.write_text(text.replace(marker, block + marker, 1), encoding="utf-8")
    print("inserted modeling group with %d Raise Spectre gem(s):" % len(spectres))
    for m in spectres:
        print("  - %s" % m)
    print("Now reload the build in PoB (lua_load_build) and verify with "
          "minion_dps_breakdown that only ONE Raise Spectre row appears.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
