---
maintained: 2026-06-16
purpose: Model-aware index of PoE mechanics/items/systems that postdate (or are unreliable in) Claude training data, so the running model knows what it must verify rather than answer from memory.
committed: yes (gitignore exception — this is curated, not regenerable)
---

# PoE Freshness Index (model-aware)

This is a **router, not a data dump.** Each entry says *what exists*, *which patch it landed in*, and
*where the real data is* — it does not reproduce the data. The point is to defeat **unknown unknowns**:
the cases where the running model doesn't realize its training is stale and asserts a mechanic confidently
and wrongly.

## How to use it (the procedure)

1. **Identify the running model.** `mcp__pob__get_context_usage` reports the active model ID. (You may
   already know it from the session.)
2. **Look up that model's training cutoff** in the table below.
3. **Anything in the index with a patch *newer* than the running model's cutoff = MUST VERIFY** before you
   assert how it works. Use the "Where / verify via" pointer (a cached file, a memory, or a fresh fetch).
4. **Entries at-or-before the cutoff** are usually safe from memory, but still defer to live tool data when
   it conflicts (trust hierarchy in `playbooks/README.md` §5).
5. This check is most load-bearing **when about to assert how a mechanic works, or evaluate a unique /
   node / item's *current* stats** — it does not need to run at every step of an analysis, only at the
   stages where patch-specific knowledge is the input.

> **Removals count as much as additions.** A *removed* mechanic breaks old assumptions just as hard as a
> new one — e.g. Ancestral totems removed (3.25), the "increased Item Quantity" gear affix removed (3.25).
> "It isn't listed as newly added" ≠ "it still works the way you remember." When a model recommends a
> mechanic from memory, that mechanic still existing is itself a freshness claim.

## Model training cutoffs (PoE patch)

| Model | Cutoff patch | Approx date | Notes |
|---|---|---|---|
| **Opus 4.8** (`claude-opus-4-8`) | **3.26** Secrets of the Atlas | Jan 2026 | Best PoE meta knowledge of current models |
| **Sonnet 4.6** (`claude-sonnet-4-6`) | **3.25** Settlers of Kalguur | Aug 2025 | Default for analysis; stale on 3.26+ |
| **Haiku 4.5** (`claude-haiku-4-5`) | **≤3.24 (unconfirmed)** | — | ⚠ cutoff not documented — treat conservatively; verify anything 3.25+ |
| **Fable 5** (`claude-fable-5`) | **unconfirmed** | — | ⚠ cutoff not documented — treat conservatively |

> Current league is **3.28 Mirage**. So **3.27 and 3.28 are past EVERY current model's cutoff**, and **3.26
> is past Sonnet/Haiku** but within Opus. When in doubt, verify.

---

## Source bookmarks (quick reference)

The wiki **league page** (mechanic overview + unique/gem tables) and **Version X.Y.0 page** (full patch
notes / balance changes) for each recent league. Fetch via `mcp__poemcp__fetch_wiki_page`.

> For **official forum patch-note threads** and **granular point releases / hotfixes** (X.Y.0a..z — which
> the wiki usually doesn't have per-release), see [`patch_notes_index.md`](patch_notes_index.md). The wiki
> Version pages below are the consolidated transcription; the forum threads there are GGG's primary source.

| Patch | League page | Version (patch notes) |
|---|---|---|
| 3.28 Mirage | https://www.poewiki.net/wiki/Mirage_league | https://www.poewiki.net/wiki/Version_3.28.0 |
| 3.27 Keepers of the Flame | https://www.poewiki.net/wiki/Keepers_of_the_Flame | https://www.poewiki.net/wiki/Version_3.27.0 |
| 3.26 Secrets of the Atlas | https://www.poewiki.net/wiki/Secrets_of_the_Atlas | https://www.poewiki.net/wiki/Version_3.26.0 |
| 3.25 Settlers of Kalguur | https://www.poewiki.net/wiki/Settlers_of_Kalguur | https://www.poewiki.net/wiki/Version_3.25.0 |
| — all patches — | | https://www.poewiki.net/wiki/Version_history |

---

## Index entries

### 3.28 — Mirage league  (past ALL models' cutoffs → always verify / use cache)
Full cache: [`reference_data/leagues/mirage.md`](leagues/mirage.md).

| Mechanic / item / system | What it is (one line) | Where / verify via |
|---|---|---|
| **Mirage league mechanic** | Free a Djinn → enter a "Mirage" sub-zone that duplicates the map's league mechanics for exclusive drops | `leagues/mirage.md` |
| **Djinn coins** | Mirage currency: Power/Skill/Knowledge = free random support on a lvl-20 gem; Restoration/Desecration = dual-form unique swap | `leagues/mirage.md` → Djinn Coins; `[[mirage-djinn-coins]]` memory |
| **Essence of Desolation** | New essence (from Essence inside a Mirage) → slot-specific bonus reforge | `leagues/mirage.md` |
| **Screams of the Desiccated** | Belt rolling a shrine-buff-while-flask-free; Saresh version rolls two | `leagues/mirage.md` + `shrines.md` |
| **The Unseen Hand (Nameless bloodline)** | Grants a **3rd ring slot** — PoB correctly shows Ring 1/2/3; not an error | `leagues/mirage.md` + `[[...]]` |
| **Mirage dual-form uniques** | Fleshrender↔Skysunder, Desecrated↔Sacred Chalice, etc. (Maraketh/Afarud profiles) | `leagues/mirage.md` |
| **Heroic Tragedy** | Timeless Jewel — **Kalguur** line (not Karui); same mechanic, different conversions | `leagues/mirage.md` |
| **Volatile Vaal Orb** | Mirage currency: rerolls unique mod values OR destroys it | `leagues/mirage.md` |
| **Crucible is ABSENT in Mirage** | No Crucible furnaces/atlas nodes; existing Crucible weapon mods can't be re-applied | `leagues/mirage.md` |

### Return of the Ancestors — event league (concurrent with 3.28 Mirage, ~2026-06-25 → 07-16)
Full cache: [`reference_data/leagues/return_of_the_ancestors.md`](leagues/return_of_the_ancestors.md). A
**time-limited (~3-week) fresh-start event** on the 3.28 client — surfaced in the 3.28.0j patch notes. You
**make NEW characters** for it: **nothing transfers in from Mirage, nothing transfers out to 3.29** (event
characters migrate to Standard at the end). So **existing Mirage characters and the 3.29 build plans are
unaffected** — the entries below apply **only to characters made inside the event.** For those,
**normal ascendancy intuition does not apply.** ⚠ Time-boxed — expires when the event ends (~2026-07-16);
verify it's still running before applying.

| Mechanic / item / system | What it is (one line) | Where / verify via |
|---|---|---|
| **Legacy of Phrecia ascendancies (forced)** | All 19 base ascendancies (except Reliquarian) are replaced by alternate **Phrecian** classes for the event — every character runs an alternate ascendancy | `leagues/return_of_the_ancestors.md` (Phrecia dates to 3.26 — within Opus; the *forced event-wide* use is new) |
| **Forbidden Tattoos** (event-exclusive) | **Not class-restricted** — splice another class's random ascendancy notable onto your tree; shared limit 1; can strategically disable unwanted ascendancy passives. Deleted on migration. | `leagues/return_of_the_ancestors.md` |
| **Trial of the Ancestors (ToTA) returns** | Re-enabled via drop-anywhere **Silver Coins** → Halls of the Dead tournament; ToTA rewards/tattoos farmable | `leagues/return_of_the_ancestors.md` |

### 3.27 — Keepers of the Flame  (past ALL models)
Cache: [`leagues/keepers_of_the_flame_3.27.md`](leagues/keepers_of_the_flame_3.27.md). Breach-sequel expansion (2025-10-31).
| Mechanic / item / system | What it is (one line) | Notes |
|---|---|---|
| **Bloodline Ascendancy classes** | New ascendancy classes | ⚠ origin of **The Unseen Hand → 3rd ring slot** (seen in Mirage). Unfamiliar ascendancy / extra slot → suspect a Bloodline |
| **Assassin rework** | Shadow/Assassin ascendancy changed | old Assassin intuition stale |
| **Breach overhaul** | New Breach art/encounters/bosses/rewards (Hiveborn) | Breach farming/atlas strategy |
| **New gems** | Conflagration, Thunderstorm, Kinetic Fusillade/Rain, Wall of Force; supports **Windburst, Kinetic Instability, Living Lightning** | the 3 supports are the Djinn-coin blacklist entries (cross-ref Mirage) |
| **Full passive refund (char + atlas) with Gold** | Respec is cheap now | don't assume regret-orb scarcity when advising tree changes |
| **Spectres auto-revive on new instance**; async trading; Vaal Orb replaces Remnant of Corruption | QoL that changes workflow assumptions | — |

### 3.26 — Secrets of the Atlas  (past Sonnet/Haiku; within Opus)
Cache: [`leagues/secrets_of_the_atlas_3.26.md`](leagues/secrets_of_the_atlas_3.26.md). Additive endgame expansion + major crafting.
| Mechanic / item / system | What it is (one line) | Notes |
|---|---|---|
| **Shaper's / Elder's Exalted Orb** | Add Shaper/Elder influence + a new influenced mod to a rare | Influence crafting is accessible again |
| **Memory Strands** (Orb of Remembrance / Unravelling / Intention) | New **mod-tier-upgrade** crafting path on bases | Relevant to "improve this rare" |
| **Runegrafts** | Currency applied to an **allocated passive Mastery** to replace it with a Runegraft effect (NOT a gear enchant — corrects earlier cache). One per *type*, no cap on total → can graft several masteries. Notable: **the Fortress** (+40% global def, −10% attr), **Gemcraft** (+1 all non-exceptional supports), **Restitching** (40% of crit damage taken recouped as life), **the River** (20% chance to full-heal on reaching low life). **Farmed via Kingsmarch shipments** to Kalguuran ports (Riben Fell DEX / Pondium INT / Kalguur STR / Any). Removable via Orb of Scouring. | ✅ confirmed live in 3.28 Mirage (wiki 2026-06-16). ⚠ **trust the [wiki Runegraft page](https://www.poewiki.net/wiki/Runegraft)** — third-party blogs (e.g. aoeah) list only a partial/"all new" subset and miss the Any-pool ones (Fortress/Gemcraft) |
| **Recombinator now core** | Mid-game crafting tool, permanent | — |
| Betrayal/Syndicate revamp; Veiled Chaos Orb back; Legacy of Phrecia ascendancies; Allflame Embers; Kalguuran Scarabs | endgame/crafting/farming systems | see cache |

### 3.25 — Settlers of Kalguur  (past Haiku; at Sonnet cutoff; within Opus/Sonnet)
Cache: [`leagues/settlers_3.25.md`](leagues/settlers_3.25.md). Mechanic integrated to core in 3.26.
| Mechanic / item / system | What it is (one line) | Notes |
|---|---|---|
| **Gold currency + Kingsmarch + shipments** | Semi-AFK income layer; gold spent on town ops | economy planning |
| **Runes / Runesmithing** | Extra rune-mod enchant layer on gear (→ Runegrafts in 3.26) | gear crafting |
| **Melee rework — Ancestral totems REMOVED** | Melee rescaled, scales with gem level; no more Ancestral Protector/Warchief | ⚠ don't recommend ancestral-totem buffing |
| **"increased Item Quantity" removed from gear** | IIQ is no longer a gear affix | ⚠ breaks old MF-gearing assumptions |
| **Warden replaced Raider**; Gladiator reworked; Tinctures back | ascendancy/skill changes | — |

---

## Training-data corrections (NOT league-gated — unreliable across models regardless of cutoff)
These are things models commonly get wrong from training noise, independent of patch:

| Correction | Pointer |
|---|---|
| **No player-accessible training dummy exists** — don't suggest "test on a dummy" | `[[poe-no-training-dummy]]` memory |
| **Eldritch implicit pools differ by slot** (e.g. no "reduced mana cost" on body) — check before promising a mod | `reference_data/eldritch_implicits/` |
| **Shrine buff effects** (Diamond ≠ ailment immunity, etc.) | `reference_data/shrines.md` |

---

## Gaps / to research
- [x] **3.25 Settlers** detail cache → `leagues/settlers_3.25.md` (2026-06-16).
- [x] **3.26 Secrets of the Atlas** detail cache → `leagues/secrets_of_the_atlas_3.26.md` (2026-06-16).
- [x] **3.27 = Keepers of the Flame** (Breach sequel, 2025-10-31) — detail cache → `leagues/keepers_of_the_flame_3.27.md` (2026-06-16).
- [ ] **3.28 Mirage atlas tree nodes** — `leagues/mirage.md` notes the GGG export predated release; refresh when available.
- [ ] Confirm **Haiku 4.5 and Fable 5** training cutoffs (currently conservative placeholders).

## Maintenance
- Add a row whenever a session surfaces a mechanic/item the running model got wrong or didn't know.
- At each **league transition** (see `playbooks/league-transition.md`), add the outgoing league's entries here and start the new league's row.
- When a new Claude model ships, add its cutoff to the model table.
