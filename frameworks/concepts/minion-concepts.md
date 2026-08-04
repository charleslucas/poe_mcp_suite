> **Canonical home:** `poe_mcp_suite/frameworks/` (public). Instance data is patch-stamped (3.29) — re-verify after any league/patch change. `local library:` references point into the maintainer's private guide library (character data + digested third-party guides, not distributed); treat them as worked-example citations, not links.

# Minion Build Concept Library

**Purpose:** the durable index of EVERY minion build concept we've encountered — banked, candidate, idea,
or rejected — so nothing discovered (lake sweeps, surveys, character imports, guide digests) gets lost when
a league-scoped decision doc is superseded. **One line of truth per concept; detail lives at the pointer.**
Created 2026-07-18. Update whenever a concept appears, changes status, or gets a verdict.

**Status legend:** `BANKED` = full archetype dir exists · `CANDIDATE` = on an active roster, not banked ·
`IDEA` = concept only, no investment yet · `SHELL/VARIANT` = leveling/variant of another entry ·
`PARKED` = viable but nobody's pursuing · `REJECTED` = eliminated, cause recorded

| Concept | Status | One-line thesis | Detail lives at |
|---|---|---|---|
| **Holy Relic of Conviction Necro** | BANKED — **3.29 league-start primary** | Relics nova on your Lancing Steel hits; poison; CDR-breakpoint scaling; block tank | `../holy-relic-necromancer/` |
| **pRAW (Poison Ranged Animate Weapon)** | BANKED — 3.29 bridge-starter option | Temp weapon army w/ 38% more dmg/speed premium; poison; boss-rebuild risk deprioritized it | `../praw-necromancer/` |
| **SRS/Absolution leveling shell** | BANKED — shared trunk of every plan | The 1→~70 campaign core all Necro minion endgames level as; swap at early maps | `../srs-absolution-leveling/` |
| **Luminary merc-summoner** ("warlord") | BANKED — speculative, 3.29 launch-gated | Hire Darakos (minion-summoning merc); Luminary scales merc+their minions; you support | `../luminary-merc-summoner/build-plan.md` |
| **Raise Spectre gem-level Necro** | CANDIDATE (unbanked) | 3.28 gem-level scaling ("70M" claims); spectre life nerfed 3.29 — re-verify | `../_comparisons/minion-builds-3.29.md` roster |
| **Absolution / Holy Strike Guardian** | CANDIDATE (unbanked) | Hybrid self-attack + sentinels; forks at ascendancy | comparison doc roster |
| **Reliquarian tanky-minion Scion** | CANDIDATE — promoted 2026-07-17 | Minions kill; YOU tank via copied unique mods (Kaom's/Chayula/Melding) + Femurs army-defense | comparison doc §Scion wildcards; roster in league cache §Reliquarian |
| **Cold-conversion melee minions (Triad Grip)** | PARKED — proven lineage (a maintainer character, L95, prior league) | Phys→cold conversion + Hatred/Frostbite; block facetank shell. 3.29: Triad Grip reworked (gem-colour), Absolution cast buff, **Fleshcrafter res-ignore enabler banked** | the maintainer's prior-league character notes (local); Fleshcrafter note in comparison doc lake block |
| **Poison skeleton archers (Dead Reckoning chassis)** | IDEA — survey-confirmed real archetype | Flat-ES stat-stick shield → skeletons gain added chaos (DR post-3.23) → poison; Skeletons of Archers transfig + Covenant/UiD | comparison doc lake block (2026-07-18) |
| **Broken Elegy wardless CWDT loop** | IDEA — community-documented | Heartbound Loop self-damage absorbed by Rotten Bulwark (≈Ward from dying minions); automated loop, no ward gear | comparison doc lake block |
| **Broken Elegy phys→chaos staff minions** | IDEA | Brute-force: 113-157% minion dmg + 59-83% phys-as-extra-chaos; Carrion Golems/zombies; Ceaseless Flesh free zombie stream | comparison doc lake block |
| **Popcorn SRS (Minion Instability)** | IDEA — survey-updated 2026-07-18 | MI + SRS of Enormity (+111% more life, always crits) = exploding skulls; Tavukai optional accelerator; avoid minion chaos-res | shell README gear table note |
| **"Lazy Pop" MI skeletons (leveling)** | SHELL/VARIANT | Skeletons + Infernal Legion + early MI rush = disposable homing bombs; fixes phase-boss deficit | shell README §Derivatives |
| **Dominating Blow sentinels (leveling)** | SHELL/VARIANT | Attack-based sentinel army; fixes cast stutter; claimed strongest early DPS | shell README §Derivatives |
| **Soulwrest phantasms** | IDEA (untouched) | Staff auto-summons phantasms from corpse consumption; classic pocket build | lake `uniques.txt`; no notes yet |
| **Fire→Chaos conversion minions** (a friend's build) | IDEA — mechanism corrected 2026-07-19; ⚠ enabler-availability gated | Minions convert phys→fire (Triad Grip red / SRS innate), THEN **"Minions convert 100% of Fire Damage to Chaos"** prefix → pure chaos; scale phys+fire+chaos ladder + poison. Flat fire (Anger) → flat chaos. **Chaos scaling lever: "Minions have Unholy Might" (Foulborn, 100% phys→chaos — ⚠ 3.28 Mirage mutated-unique mechanic, verify 3.29)** | `_concepts/minion-fire-to-chaos.md` |
| **Minion-mods-affect-you hybrid** ("ride your own minion buffs") | IDEA — new 2026-07-19 (mods.txt sweep) | Catarina veiled prefixes **"Increases and Reductions to Minion Damage / Attack Speed / Cast Speed also affect you"** → a PLAYER build inherits all its stacked minion-damage gear. Turns a minion-gear tree into a personal-damage multiplier; pairs with a minion off-hand for hybrid clear + player single-target. Untested seed | this table; mods.txt `Veiled` rows (catarina_veiled_prefix) |
| **Wraithlord high-level spectres** | REJECTED for league-start (2026-07-12) | Boss-gated helmet, 10-15+ div days 1-3, forbids non-spectre minions — "pocket starter" | comparison doc axis-4 table |
| **SRS as a destination build** | REJECTED as destination (2026-07-12) | Weakest endgame ceiling; repositioned as the universal leveling core | comparison doc |
| **Skeleton Mages** | NOTE — mechanism moved | No longer via Dead Reckoning (3.23); now a standalone transfigured gem. Untracked as a concept | shell README stale-warning |
| **Player-summoner Luminary** | REJECTED (verified 2026-07-17) | Luminary has ZERO "your minions" scaling — player-summoner impossible under it | comparison doc §Luminary |

## Cross-cutting staple items (build-agnostic — see the market watchlist)
- **Ashes of the Stars** (Onyx Amulet) — the generic minion-power amulet: **+1 to all Skill Gems** (every minion
  + support gains a level) **+ (20–30)% Quality of all Skill Gems** (a free quality roll across the whole link).
  No life/res, Uber-Eater drop-restricted (chase). Verified current stats poewiki 2026-07-20 (the old Reservation
  Efficiency line is legacy/pre-3.23). Universal to any minion endgame; specifically pushes Holy Relic's CDR
  breakpoint. → on the **`local library: market watchlist`** ("buy on any real dip").

## Conventions
- **Promote:** IDEA → CANDIDATE when it enters a roster; CANDIDATE → BANKED when it gets an archetype dir
  (guide digest / build-plan). Move the detail, keep this row as the pointer.
- **Reject:** keep the row, record the cause + date (the design-attempt-log pattern) — rejected concepts
  resurface every league and the cause is the valuable part.
- **League re-scope:** at each league transition, sweep the table — statuses shift (e.g. Reliquarian roster
  reshuffles every league; 3.29 spectre nerf hits the Spectre candidate).
- **Sources feeding this index:** text-lake sweeps (`_comparisons/minion-builds-3.29.md` §lake sweep has the
  vocabulary), community surveys, character imports, guide digests.
