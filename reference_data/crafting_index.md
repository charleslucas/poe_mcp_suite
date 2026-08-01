# Crafting Index — the mechanics map

**What this is:** an *organizing* map of PoE's crafting mechanics — what each method does, roughly what it
costs, whether it's deterministic, when to reach for it, and **which tool or source answers questions about
it**. A routing table, so we stop rediscovering the landscape.

**What this is NOT — deliberately:** mod pools, spawn weights, tier tables, essence/fossil mod lists. Those are
GGG's data and are **runtime-lookup only, never committed** (see [`../legal_considerations.md`](../legal_considerations.md)).
Every row below points at the tool that fetches that data live.

> `fetched: 2026-07-31` · `patch: 3.29` · Structure/rules change rarely; re-check at a league or major patch.

---

## 1. The rules everything else sits on

| Rule | Detail |
|---|---|
| **Affix limits** | Rare: **3 prefixes + 3 suffixes**. Magic: 1 + 1. Jewels: 2 + 2. Crafted mods **count toward these limits** |
| **Mod groups** | Every mod belongs to a `group`. **Two mods from one group cannot coexist** — the single biggest source of "why can't I craft this" |
| **Item level (ilvl)** | Gates which *tiers* can roll. A low-ilvl base has a hard ceiling no amount of crafting fixes → replace instead |
| **Implicit vs explicit** | Implicits come from the base (changeable only by Vaal/eldritch-style mechanics); explicits are what currency manipulates |
| **Bench crafts** | Deterministic, occupy an affix slot, **one per item** unless multimod |
| **Quality** | Scales an item's *local* defences/damage. ⚠ PoB's character import appears to drop it — confirm in-game |

## 2. Methods — cheapest and most deterministic first

| Method | What it does | Determinism | Rough cost | Reach for it when |
|---|---|---|---|---|
| **Crafting bench** | Adds one chosen mod | **Deterministic** | Low | Filling a known-open affix. First thing to check |
| **Anointing** (oils) | Adds a passive notable to amulet / Cord belt | **Deterministic** | Wildly variable — **price the oils** | An empty anoint. Often the best gain-per-chaos on a finished character |
| **Quality** (scraps/whetstones) | +20% local defences/damage | **Deterministic** | Trivial | Any piece under 20% |
| **Vendor recipes** | Fixed outcomes from ingredient sets | **Deterministic** | Trivial | Leveling gear, +1 gem-level weapons/helms → [`vendor_recipes.md`](vendor_recipes.md) |
| **Essences** | Reroll rare, **guaranteeing one specific mod** | Semi | Low–mid | You need one mod guaranteed and can accept random others |
| **Alt–aug–regal** | Roll magic → augment → regal to rare | Random | Cheap, slow | Few high-tier mods wanted; patient crafting |
| **Chaos spam** | Reroll all explicits | Random | Mid–high | Fast results on a good high-ilvl base |
| **Fossils + resonators** | Bias mod weights; can **block** mod types | Weighted | Mid | Targeting a mod family, or excluding one |
| **Harvest** | Targeted reroll/augment by mod type | Semi-targeted | Mid–high | Surgical changes without full reroll |
| **Beast crafting** | Imprints, splits, and **applying high-ilvl mods to low-ilvl bases** (Farric Alphas) | Special | Mid | Base-preservation and ilvl-bypass tricks |
| **Metacrafting** | "Prefixes/suffixes cannot be changed" + reroll — surgical | Deterministic-ish | **High** (divines) | Top-end items only |
| **Multimod** | Up to 3 crafted mods | Deterministic | 2 ex + crafts | Only economic with **2+ open affixes** |
| **Influence / Awakener's** | Unlocks influence mod pools; combines two influences | Random | High | Endgame chase mods |
| **Corruption (Vaal)** | Random outcome, item becomes unmodifiable | Gamble | Low + risk | Only on items you accept losing. Low-ilvl vaaling raises odds of some outcomes |
| **⭐ Allflame crafting** (3.29) | League mechanic; accrues an **`Intangibility: N%`** limiter as an item is modded | ◐ unknown | ◐ | ◐ **Not yet researched** — see `leagues/Allflame.md` §Rule changes #1b + its drill-down ledger row |

## 3. Question → where the answer lives

| Question | Tool / source |
|---|---|
| What mods *can* roll here? | `search_crafting_mods`, `list_craftable_mods_for_base` |
| What tier is my mod, what's next? | `analyze_item_mods` (accepts `item_slot` — reads live PoB) |
| What can I bench-craft? | `search_master_crafts` |
| What does this essence guarantee? | `get_essence_detail` |
| Odds of hitting mods X+Y? | `calculate_mod_odds` |
| Best anoint for my build? | `find_best_anointment` — **then price oils via `ninja_lookup`** |
| Strategic "how should I craft this?" | `suggest_crafting`, and [`../playbooks/crafting-optimization.md`](../playbooks/crafting-optimization.md) |
| Any easy wins across my gear? | [`../playbooks/gear-crafting-audit.md`](../playbooks/gear-crafting-audit.md) |
| Mechanic explanations | craftofexile [basics](https://www.craftofexile.com/basics) / [advanced](https://www.craftofexile.com/advanced); poewiki |
| Vendor recipes | [`vendor_recipes.md`](vendor_recipes.md) |

## 4. Standing gotchas

1. **Group collisions** block most "open affix" plans — diff candidate craft `group=` against the item's existing groups first.
2. **One bench craft per item** unless multimod.
3. **Anoint tools rank impact, not cost** — a top pick may need a 200c+ Golden Oil while #3 costs ~1c for most of the benefit.
4. **Low ilvl is a ceiling, not a bad roll** — recommend replacement.
5. **Crafting can't add a missing defensive layer.** Say so and route to gear-shopping or a build change.
6. Uniques: anoint / quality / corrupt only — no affix crafting.

## 5. Trust hierarchy

PoB data files (`PathOfBuilding/src/Data/`, ships with the patch) & live PoB sim → craftofexile → poewiki →
community opinion. **Never** AI search for craft mechanics — it blends patch versions and confabulates.
