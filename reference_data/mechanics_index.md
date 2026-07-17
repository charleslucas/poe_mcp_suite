---
maintained: 2026-07-16
purpose: Mechanic-keyed registry of PoE mechanics/systems — each one's lifecycle (introduced → changed → removed/returned) and, critically, its CURRENT SCOPE, so analyses can filter mechanics to a character's actual context and not bleed league/event data into the wrong build.
committed: yes (gitignore exception — curated, complements freshness_index.md)
---

# PoE Mechanics Index (mechanic-keyed + scope-tagged)

A **mechanic-keyed** companion to the **patch-keyed** [`freshness_index.md`](freshness_index.md). Same
underlying facts (detail lives in `leagues/*.md`), different axis:

- `freshness_index.md` answers *"given the running model, what must I verify?"* (patch vs model cutoff).
- **This file** answers *"what is the current **state** and **scope** of mechanic X, and how did it get
  there?"* (mechanic lifecycle). It is the **source of truth for a mechanic's status/scope**; freshness rows
  can stay terse and point here.

**Why mechanic-keyed:** every league adds one or more mechanics and usually removes/disables/nerfs others.
A league-keyed view fragments a single mechanic's history (Runegrafts span 3.25→3.28; Trial of the Ancestors
is a 3.22 league that's now a 2026 event). Tracking per-mechanic keeps each one's lifecycle and **current
availability** in one place.

---

## ⚠ Compartmentalization rule (the point of the scope tags)

**Before applying any mechanic to a character, check its Scope against that character's context.** At
character pre-flight (see `playbooks/README.md` §2c), establish: which **league/realm** is the character in,
and is it an **event** character? Then:

> **Only consider mechanics whose Scope includes the character's context.**
> A `challenge-league` mechanic does not exist for a Standard character. An `event-only` mechanic does not
> exist for a normal league character. A `removed` mechanic does not exist at all. A `disabled-this-league`
> mechanic is off right now even though it's normally core.

This is what keeps **Return of the Ancestors** (event-only) from contaminating **Mirage** or **3.29** work,
and **Mirage** mechanics (Djinn coins, etc.) from being assumed present in **3.29**.

### Scope / status vocabulary

> **PoE temporary-league taxonomy** (per the [wiki](https://www.poewiki.net/wiki/League)): *temporary* leagues
> come in two recurring flavours — **challenge leagues** (the ~13–16-week **expansion** leagues: Mirage 3.28,
> Keepers 3.27, Settlers 3.25… — new mechanic + expansion + challenges; characters migrate to **Standard** at
> end) and **event leagues** (shorter, also recurring: **Legacy of Phrecia / Return of the Ancestors**, races,
> Mayhem, Endless Delve… — characters migrate to **Standard or Void** at end) — plus private leagues. So
> "Ancestors" is precisely an **event league**, a *sibling* of the Mirage challenge league, not a challenge
> league itself. **Both kinds are fresh-start, temporary, and RECUR**, so the tags below cover both and you
> **re-scope at every transition (challenge OR event)**.

| Tag | Meaning | Example |
|---|---|---|
| `core` | Permanent; present in all leagues incl. Standard | Recombinator, Runegrafts |
| `challenge-league` | Only in the named **challenge (expansion) league** (~13–16 wk); gone next league unless cored | Djinn coins (Mirage 3.28) |
| `event-only` | Only during a specific **event league** (short, recurring; sibling to challenge leagues) | Forbidden Tattoos / Phrecian ascendancies (Return of the Ancestors) |
| `removed` | Taken out of the game | Ancestral totems |
| `disabled-this-league` | Normally core, but off in the current league | Crucible (absent in Mirage) |
| `nerfed` / `reworked` | Still present but materially changed | Assassin rework (3.27) |

> **Current context anchors (update at each league roll):** live **challenge league** = **3.28 Mirage**
> (2026-03-06 → **ends 2026-07-20 3PM PDT**; does NOT go core — see freshness_index.md end-of-league entry);
> next challenge league = **3.29 Curse of the Allflame** (launches 2026-07-24); ~~event league Return of the
> Ancestors~~ **ENDED 2026-07-16** — its event-only mechanics are now `removed` (section below).

> **Canonical enumeration sources (two complementary views):**
> - Mechanic-keyed: [`League_mechanics`](https://www.poewiki.net/wiki/League_mechanics) — **every league
>   mechanic, active and removed, with its lifecycle** ("removed in X.Y.0", "not added to core", "replaced
>   in X.Y.0"). Seed new entries at league transitions (league-transition playbook Step 4.3) and audit this
>   file for missing removals — it's how we'd catch a mechanic that quietly left the game without an entry
>   here recording it.
> - League-keyed: [`League`](https://www.poewiki.net/wiki/League) — every league ever run, with **exact
>   start/end dates + release version**, each linking to a per-league detail page listing what was active
>   (mechanics, uniques, monsters) in that league. The authoritative source for the context-anchor dates
>   above and for reconstructing a past league's context (e.g. a Standard character built during Settlers).

---

## Active mechanics

| Mechanic | Scope | Introduced → lifecycle | Current state (one line) | Verify / detail |
|---|---|---|---|---|
| **Runegrafts** | `core` | 3.25 Runes → 3.26 Runegrafts → 3.27 (Recompense→Refraction rename) → live 3.28 | Currency applied to an allocated passive **Mastery** to replace it (one per type, no total cap); farmed via Kingsmarch shipments | `freshness_index.md` (3.26 row); wiki Runegraft page |
| **Recombinator** | `core` | League mechanic → cored 3.26 | Permanent mid-game crafting tool (combine two items' mods) | `leagues/secrets_of_the_atlas_3.26.md` |
| **Gold / Kingsmarch / shipments** | `core` | 3.25 Settlers → cored 3.26 | Semi-AFK gold income; town ops; shipments source Runegrafts | `leagues/settlers_3.25.md` |
| **Memory Strands** (Remembrance/Unravelling/Intention) | `core` ⚠verify | 3.26 | Mod-tier-upgrade crafting path on bases | ⚠ confirm it persisted past 3.26; `leagues/secrets_of_the_atlas_3.26.md` |
| **Shaper's / Elder's Exalted Orb** | `core` ⚠verify | 3.26 | Add influence + a new influenced mod to a rare | ⚠ confirm persistence; 3.26 cache |
| **Bloodline ascendancies / The Unseen Hand (3rd ring slot)** | `core` ⚠verify | 3.27 Keepers | Alt ascendancy classes; Unseen Hand grants a 3rd ring slot (seen on Mirage chars) | ⚠ confirm core vs league; `leagues/keepers_of_the_flame_3.27.md` |

> **Note — Legacy of Phrecia alternate ascendancies are NOT core.** The 19 "Phrecian" alternates exist
> *only* during Ancestor/Phrecia events — see the `event-only` row below. In normal/core play the standard
> 19 ascendancies are the only set.

## Challenge-league mechanics (live only in 3.28 Mirage — gone in 3.29 unless cored)

| Mechanic | Scope | Current state | Verify / detail |
|---|---|---|---|
| **Djinn coins** | `challenge-league` (Mirage) | Free random support on a lvl-20 gem (Power/Skill/Knowledge); dual-form unique swap (Restoration/Desecration) | `leagues/mirage.md`; `[[mirage-djinn-coins]]` |
| **Mirage sub-zones** | `challenge-league` (Mirage) | Free a Djinn → duplicate-mechanic sub-zone for exclusive drops | `leagues/mirage.md` |
| **Essence of Desolation** | `challenge-league` (Mirage) | New essence → slot-specific reforge | `leagues/mirage.md` |
| **Screams of the Desiccated** (belt) | `challenge-league` (Mirage) | Shrine-buff-while-flask-free belt | `leagues/mirage.md` |
| **Volatile Vaal Orb** | `challenge-league` (Mirage) | Reroll unique mod values OR destroy it | `leagues/mirage.md` |
| **Heroic Tragedy** (timeless jewel — Kalguur line) | `challenge-league` (Mirage) ⚠verify | Kalguur conversions (not Karui) | `leagues/mirage.md` |

## Event-only mechanics (Return of the Ancestors — ❌ ENDED 2026-07-16, all `removed`)
> 🔴 **The event ended 2026-07-16 3PM PDT.** Every row below is now `removed` — it does NOT exist for any live
> character (Mirage, Standard, or 3.29). Event characters migrated to Standard **lose these** (Forbidden Tattoos
> deleted; the Scavenger/Phrecian ascendancy gone → an ascendancy-less Scion). Kept here as history + as the
> re-scope record. ⚠ ToTA is the one to watch: it's *recurred* before (base-game 3.22, this event) — if it
> returns to core or a future event, re-scope it then; don't assume "removed forever."

| Mechanic | Scope (post-2026-07-16) | Current state | Verify / detail |
|---|---|---|---|
| **Forbidden Tattoos** | `removed` (was `event-only`; event ended 2026-07-16) | Deleted on migration to Standard. Gone for all live characters. | `leagues/return_of_the_ancestors.md` (historical) |
| **Phrecian alternate ascendancies (the 19)** | `removed` (was `event-only`; event ended 2026-07-16) | Binary set-swap of the 19 ascendancies — **event-only, now gone**. Migrated Scions/etc. keep the char but lose the alternate ascendancy. Normal ascendancy set applies everywhere else. | `leagues/return_of_the_ancestors.md` (historical) |
| **Trial of the Ancestors (ToTA) return** | `removed` (was `event-only`; event ended 2026-07-16) | Silver Coins / Halls of the Dead gone with the event. ⚠ ToTA has recurred before — re-scope if it comes back. | `leagues/return_of_the_ancestors.md` (historical) |

> ⚠ **Event entries are fresh-start & time-boxed.** They apply ONLY to characters made inside the event and
> expire ~2026-07-16. **Nothing transfers in from Mirage or out to 3.29** — so existing Mirage characters and
> the 3.29 build plans must ignore this whole section.

## Removed / disabled / nerfed (do NOT recommend as if present)

| Mechanic | Status | When | Note |
|---|---|---|---|
| **Ancestral totems** (Protector/Warchief) | `removed` | 3.25 | Melee rescaled to gem level; don't recommend ancestral-totem buffing |
| **"increased Item Quantity" gear affix** | `removed` | 3.25 | IIQ no longer a gear mod; breaks old MF-gearing assumptions |
| **Crucible** | `disabled-this-league` | absent in 3.28 Mirage | No furnaces/atlas nodes; existing Crucible weapon mods can't be re-applied |
| **Runegraft of Recompense** | `reworked`→Refraction | 3.27 | Renamed; effect changed to fork/chain/+1 projectile |
| **Assassin / Raider** | `reworked` / replaced | 3.27 Assassin rework; 3.25 Warden replaced Raider | Old ascendancy intuition stale |

---

## Maintenance
- **At each league roll:** re-scope. Challenge-league mechanics of the outgoing league → either `removed`/
  gone or promoted to `core` (if cored). Add the incoming league's new mechanics. Update the "context anchors."
- **At event start/end:** add/expire `event-only` rows.
- **When a mechanic changes:** append to its lifecycle and update its current-state line + scope tag here
  (this file is the status source of truth); keep the freshness/league files pointing here.
- Resolve `⚠verify` tags by checking the wiki / live tools when the mechanic next becomes load-bearing.
