> **Canonical home:** `poe_mcp_suite/frameworks/` (public). Instance data is patch-stamped (3.29) — re-verify after any league/patch change. `local library:` references point into the maintainer's private guide library (character data + digested third-party guides, not distributed); treat them as worked-example citations, not links.

# Concept: Fire→Chaos Conversion Minions

**Status:** ✅ **REALIZED — measured on a live character 2026-08-04.** (Was IDEA since 2026-07-19; origin:
user relayed a friend's build — the same friend co-rebuilt the character that now runs it.)

**Aliases (record as encountered, never invent):** "fire-to-chaos minions" · "minion conversion gloves" ·
skeleton-mage circles call the family "Chaos/Poison Conversion" · ◐ survey phrasing: "specific glove
conversions and unholy might scaling".

## ✅ In-game realization (maintainer's live character — L91 block SRS Necromancer)
**Golem Touch, Conjurer Gloves** (rare, ilvl 80): `Minions convert 100% of Fire Damage to Chaos Damage`
+ 40% fire res + 30% chaos res + ES. Paired with **Anger + Generosity** (flat fire → minions) on an SRS
build (innate 100% phys→fire): all minion damage exits as chaos → poisons, feeds The Covenant's added
chaos + Withering Touch. **Measured: +121,112 Full DPS (+19.8%, 612,823 → 733,935)** for −3,938 EHP
(replaced life-roll gloves). PoB models the ladder correctly.

**Cross-build confirmation (2026-08-04 surveys):** the *same glove tech* is the community's recommended
chaos/poison variant for **skeleton mages**, and the "Chaos Poison Zoomancer" meta variant scales the
identical phys/chaos+poison stack — the tech is archetype-independent, exactly why it lives in _concepts.

## References (builds/videos demonstrably using the tech or its family)
- ◐ GhazzyTV — Zoomancer build guide (poe-vault, chaos/poison variants): poe-vault.com/guides/zoomancer-necromancer-build-guide
- ◐ HelmBreaker — chaos minion army PoB (pobarchives MrxDnMaY); his 3.28 pRAW guide is digested in `../praw-necromancer/`
- ◐ "This Walking Simulator Just Got BETTER – Poison Zoomancer" (YouTube lND4JA-dVzI)
- ✅ Live implementation: the maintainer's live character notes (local)

## The correct mechanism (survey-corrected — the intuitive version is a TRAP)

**Chain:** minion Physical → Fire → Chaos, then scale every stage.
1. **Phys → Fire:** Triad Grip (4 RED sockets/gems) OR Summon Raging Spirits (innate 100% phys→fire).
2. **Fire → Chaos:** the affix **"Minions convert 100% of Fire Damage to Chaos Damage"** (lake `mods.txt`:
   Explicit Prefix, tags chaos/elemental/fire/minion). This is the linchpin.
3. **Result:** minions deal pure chaos; you stack increased Physical (base) + Fire (mid) + Chaos/extra-chaos
   (final) — the full conversion ladder — and it poisons well. Flat fire (Anger aura) becomes flat chaos.

## ⚠ THE TRAP (why the "obvious" version deals 0 damage)

**Do NOT use Avatar of Fire / Earendel's Embrace for the funnel.** Avatar of Fire grants *"Deal no Non-Fire
Damage."* Convert that fire → chaos and the chaos is **non-fire → zeroed. 0 damage.** The lake first pointed
at Earendel's Embrace (it grants skeletons Avatar of Fire) as the "only fire" enabler — that reconstruction
was WRONG for a chaos build. Same trap applies to any *"Minions deal no Non-Fire Damage"* implicit. The funnel
must be **conversion** (phys→fire), which leaves no cold/lightning to begin with — NOT a "deal no" denial.
*(This likely explains the user's memory of "items preventing cold/lightning": phys→fire conversion, or the
`Deal no Cold/Lightning Damage` Scourge downsides — now in `mods.txt` — but those don't enable the chaos step.)*

## Scope / availability (the real gate)

- **"Minions convert 100% Fire→Chaos"** is a **Mercenary-warrant Infamous mod** (poewiki
  `Modifier:MercenaryModMinionFireConvertToChaos`), surfaced via **Mercenaries of Trarthus** + **Legacy of
  Phrecia** events. In the 3.28 lake it indexes as an Explicit Prefix. **3.29 CORES the Mercenary system**
  → this enabler may be obtainable in 3.29 via merc-sourced gloves. **VERIFY at 3.29 launch** (does the
  Infamous merc mod pool carry it? which slot?). This is the single make-or-break question.
- **Sinner Saint (Lycia/Phrecia ascendancy) fire→chaos: DOES NOT apply to minions** (survey-confirmed —
  conversion without the word "Minions" never inherits to minions). Dead end; ignore.
- Community verdict: the working form is **Poison SRS** with the fire→chaos glove mod (SRS innate phys→fire
  → gloves → chaos → poison). That's the modern, viable expression — not skeletons+Avatar of Fire.

## Community survey (2026-07-19, Google AI Mode — all unverified priors)

- Query A ("Earendel's + Avatar of Fire fire→chaos"): returned **"mechanically impossible"** — CORRECT about
  the Avatar-of-Fire route (deal-no-non-fire zeroes chaos), but wrongly assumed that's the only funnel.
  Earendel's Embrace's real historical use = **popcorn skeletons** (Minion Instability fire explosions,
  ~3.3 Incursion; obsolete now, SRS-MI superseded it) — a *different* build.
- Query B ("how do minions convert fire→chaos"): the accurate answer — the **Infamous glove prefix**, popular
  for **Poison SRS**; Sinner Saint/Lycia does NOT hit minions; universal chaos-minion alternatives are
  phys→chaos (Unholy Might 100% phys→chaos, Triad Grip 4 WHITE, Added Chaos support).

## Verdict

A real, coherent build **IF** the fire→chaos minion mod is obtainable in the target league (event/merc-gated,
not a standard craftable). Best modern form = Poison SRS, not skeletons. **Next step if pursued:** verify the
merc Infamous mod at 3.29 launch; if present, it's a legit chaos-SRS variant. Otherwise it's Phrecia/merc-event
-locked.

## Lake-tooling payoff (why this concept mattered beyond the build)

This investigation drove the **mods.txt** addition to the text lake (2026-07-19): the fire→chaos enabler and
the `deal no <element>` pieces live in `Data/Mod*.lua`, which the lake didn't index — proving a gap the
passives/uniques/gems corpus couldn't cover. Now greppable. See `reference_data/text_lake/MANIFEST.md`.
