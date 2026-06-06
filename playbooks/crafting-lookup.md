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

**Fossil / essence affinities:**
- The affinity data is in `reference_data/craftofexile/poec_affinities.json` (loaded by the cache).
- Currently no dedicated tool surfaces this — note the gap and use `search_craft_mods` to cross-reference fossil-specific mods by keyword (e.g. "aberrant" for chaos resistance mods).

**Crafting bench recipes:**
- Bench cost data is in `poec_common.json` (`benchcosts` key).
- No dedicated tool yet — pull via `search_craft_mods` with the target stat as keyword and note results come from the full mod pool, not bench-only.

**Mod weights / odds:**
- craftofexile data does not directly expose raw numeric weights in the lang/data files at this level of access.
- For odds, direct the user to the craftofexile website's Calculator UI — it has the full simulation engine client-side.
- For weight comparisons (which fossil is better), use affinity data if accessible, or note it requires the Calculator UI.

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
