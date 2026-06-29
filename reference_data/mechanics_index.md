---
maintained: 2026-06-29
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
| Tag | Meaning | Example |
|---|---|---|
| `core` | Permanent; present in all leagues incl. Standard | Recombinator, Runegrafts |
| `challenge-league` | Only in the named temp league; gone next league unless cored | Djinn coins (Mirage 3.28) |
| `event-only` | Only during a time-boxed event | Forbidden Tattoos (Return of the Ancestors) |
| `removed` | Taken out of the game | Ancestral totems |
| `disabled-this-league` | Normally core, but off in the current league | Crucible (absent in Mirage) |
| `nerfed` / `reworked` | Still present but materially changed | Assassin rework (3.27) |

> **Current context anchors (update at each league roll):** live challenge league = **3.28 Mirage** (ends
> ~2026-07-20); next = **3.29** (launches 2026-07-24); active event = **Return of the Ancestors**
> (2026-06-25 → 07-16, fresh-start characters only).

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
| **Legacy of Phrecia alternate ascendancies** | `core` (selectable) / **`event-only` when FORCED** | added 3.26; **forced event-wide** in Return of the Ancestors | Alternate "Phrecian" ascendancies; normally optional, but the event **replaces all 19 base ascendancies** with them | `leagues/return_of_the_ancestors.md` |

## Challenge-league mechanics (live only in 3.28 Mirage — gone in 3.29 unless cored)

| Mechanic | Scope | Current state | Verify / detail |
|---|---|---|---|
| **Djinn coins** | `challenge-league` (Mirage) | Free random support on a lvl-20 gem (Power/Skill/Knowledge); dual-form unique swap (Restoration/Desecration) | `leagues/mirage.md`; `[[mirage-djinn-coins]]` |
| **Mirage sub-zones** | `challenge-league` (Mirage) | Free a Djinn → duplicate-mechanic sub-zone for exclusive drops | `leagues/mirage.md` |
| **Essence of Desolation** | `challenge-league` (Mirage) | New essence → slot-specific reforge | `leagues/mirage.md` |
| **Screams of the Desiccated** (belt) | `challenge-league` (Mirage) | Shrine-buff-while-flask-free belt | `leagues/mirage.md` |
| **Volatile Vaal Orb** | `challenge-league` (Mirage) | Reroll unique mod values OR destroy it | `leagues/mirage.md` |
| **Heroic Tragedy** (timeless jewel — Kalguur line) | `challenge-league` (Mirage) ⚠verify | Kalguur conversions (not Karui) | `leagues/mirage.md` |

## Event-only mechanics (Return of the Ancestors — fresh-start chars, ~2026-06-25 → 07-16)

| Mechanic | Scope | Current state | Verify / detail |
|---|---|---|---|
| **Forbidden Tattoos** | `event-only` | NOT class-restricted — splice another class's random ascendancy notable; shared limit 1; can strategically disable unwanted ascendancy passives; deleted on migration | `leagues/return_of_the_ancestors.md` |
| **Forced Phrecian ascendancies** | `event-only` | Every event character runs an alternate ascendancy — normal ascendancy intuition does not apply | `leagues/return_of_the_ancestors.md` |
| **Trial of the Ancestors (ToTA) return** | `event-only` | Re-enabled via drop-anywhere Silver Coins → Halls of the Dead tournament; tattoos/rewards farmable | `leagues/return_of_the_ancestors.md` |

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
