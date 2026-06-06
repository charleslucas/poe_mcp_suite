# Playbook: Crafting Lookup

For questions about what mods can roll on an item, fossil/essence affinities, crafting bench options, mod weights, or odds of hitting a target mod combination. The core principle: **do not answer from training memory** — mod pools change with every patch and your built-in knowledge is unreliable. Always fetch current data first.

---

## Step 0 — Frame the work

*"Checking craftofexile.com data for current mod pool info — won't rely on training memory for this."*

---

## Step 1 — Confirm cache is ready

Call `craftofexile_cache_status()`. If any files are listed as MISSING, call `update_craftofexile_cache()` before proceeding. If the last version check was more than 12 hours ago, call `update_craftofexile_cache()` to check for updates (it won't re-download unchanged files).

---

## Step 2 — Classify the question

**Mod pool / what can roll:**
- Use `search_craft_mods(query)` to find mods by keyword.
- Narrow with `item_class` param if the user specifies a slot (e.g. "helmet", "ring", "bow").
- For base-specific lookup, use `get_craft_base_items(query)` to confirm the exact base name first.

**Tier ranges and spawn weights:**
- Use `get_craft_tiers(base_type, query)` to get every tier's min iLvl, value range, and spawn weight for a mod on a specific item class (e.g. `get_craft_tiers("staff", "increased physical damage")`).
- Weight numbers are relative pool weights — higher = more common. Divide a tier's weight by the sum of all tier weights for that mod to get its raw probability share.
- Only tiers with non-zero weight are returned; zero-weight entries are unrollable variants.

**Fossil affinities:**
- Use `get_fossil_info(fossil_name)` to see which mod type categories a fossil boosts, reduces, or blocks.
- Returns `more_list` (boosted), `less_list` (reduced), `block_list` (blocked), plus raw affinity weights from `mod_data`.
- Cross-reference: confirm a target mod's type category from `search_craft_mods` or `get_craft_tiers` output (the `modgroup` field), then check `get_fossil_info` to see if that category is boosted.

**Essence guaranteed mods:**
- Use `get_essence_mods(essence_name, item_type="")` to see what mod an essence guarantees on each slot.
- Filter by slot with `item_type` (e.g. `get_essence_mods("dread", "staff")` to see only staff mods).
- If an essence guarantees one of the target mods, the crafting plan simplifies: use the essence to lock that mod, then alt-orb or fossil-craft the remaining mods.

**Crafting bench recipes:**
- Bench cost data is in `poec_common.json` (`benchcosts` key).
- No dedicated tool yet — pull via `search_craft_mods` with the target stat as keyword and note results come from the full mod pool, not bench-only.

**Probability / expected cost:**
- The data from `get_craft_tiers` (weights) gives you the raw ingredients for probability math, but the full simulation (prefix/suffix slot interaction, expected orb cost for a mod combination) lives in the craftofexile Calculator UI.
- For rough estimates: if a target mod has weight W out of total pool weight T, the probability of hitting it on any given roll is approximately W/T. For two mods simultaneously it's roughly (W1/T) × (W2/T) × (prefix_slots × suffix_slots adjustment). Use the Calculator for precise numbers.

---

## Step 3 — Cross-reference with PoB if a build is loaded

If the user has a build loaded and is asking whether a specific mod matters:
- Use `get_build_stats` or `get_calc_breakdown` to check whether the stat is already capped or has diminishing returns before recommending effort to chase it.
- A great mod on paper may be worthless if that layer is already maxed.

---

## Step 4 — Supplement with poedb if needed

`search_craft_mods` covers the craftofexile mod pool (which is crafting-focused and well-maintained). If the user needs additional context — like which item level a specific tier requires, or corrupted implicits — `search_mods(item_type, query)` pulls from poedb.tw and includes iLvl requirements and mod family groupings.

Use both when completeness matters; craftofexile for weights/affinities, poedb for tier/iLvl structure.

---

## Trust hierarchy for crafting data

1. **craftofexile.com cached data** (via `search_craft_mods`, `get_craft_base_items`) — authoritative for what can roll and affinities, current as of last cache update
2. **poedb.tw** (via `search_mods`) — authoritative for iLvl tiers and mod families
3. **Your training data** — do not use for specific mod values, weights, or what rolls on what; use only for explaining mechanics (how fossils work conceptually, how prefix/suffix slots are shared, etc.)
