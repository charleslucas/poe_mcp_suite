# Playbook: DPS Analysis

For Claude sessions where the user wants to improve a character's damage output. Load this playbook in full at the start of the task; it gates which data sources you need to fetch and saves context.

---

## Step 0 — Frame the work for the user

*"Using the DPS Analysis playbook — I'll run a 4-question triage to scope this, then pull only the data sources we actually need."*

Task-specific narration: before searching trade, say which pseudo-stat IDs you're using and why (they match items regardless of which explicit line the stat rolls on). Before simulating a swap in PoB, say so — numbers on paper can hide attribute or resistance problems that only show up live.

---

## Step 1 — Triage (structured)

Before loading any data, run this scoping questionnaire via `AskUserQuestion`. Skip a question if the answer is unambiguous from prior conversation context.

**Q1 — Scope of changes considered**
- Gear only
- Passive tree only
- Skill gems / supports only
- All of the above

**Q2 — Budget**
- Read live from stash via `mcp__poe__list_tabs` + `mcp__poe__price_tab` BEFORE asking. Only ask if the stash read fails or returns nothing useful. Present the computed budget back to the user for confirmation: "I see ~X chaos / Y div in your stash. Use this as the budget?"
- If they want a smaller working budget, ask.

**Q3 — DPS profile target**
- Bossing (single-target burst, stationary uptime)
- Mapping (AoE clear speed, mobility)
- Both (balanced)

**Q4 — Locked items / nodes**
- "Anything you refuse to change?" — single open question. Common answers: a signature unique (Winds of Fate, Mageblood), an ascendancy notable, a specific skill gem.

Optional follow-up if relevant:
- **Risk tolerance** — only ask if budget is high enough that corruption gambling or enchant rerolling is on the table (~10+ div).

---

## Step 2 — Data loads (driven by Q1–Q4 answers)

### Always load
- Pre-flight: `mcp__pob__get_context_usage` + league reference + character snapshot (see [`README.md`](README.md) section 2)
- Character live state: `mcp__pob__lua_get_stats` (TCP) or `mcp__pob__get_build_stats` (disk)
- Equipped items: `mcp__pob__get_equipped_items`
- Main skill setup: `mcp__pob__get_skill_setup`
- Character journal if it exists: `character_data/{Account}/{Character}/journal.md`

### Add if Q1 = Gear or All
- League context (current league name affects ninja prices, mod pool, league mechanics): `mcp__poemcp__currency_overview`
- Trade API stat IDs for mods we're about to search: `mcp__poe__get_stat_ids`
- Eldritch implicit pools from `reference_data/eldritch_implicits/` if any helmet/body/glove/boots are uniques or rares being recrafted
- Wiki page for each equipped unique if its mechanics are non-obvious: `mcp__poemcp__fetch_wiki_page`

### Add if Q1 = Tree or All
- Full passive tree allocation: `mcp__pob__lua_get_tree` with `include_node_ids: true`
- Build guide tree section if a guide is referenced in the character doc
- `mcp__pob__find_path_to_node` for any candidate new allocations
- Timeless jewel mechanics if a Lethal Pride / Glorious Vanity / Militant Faith / etc. is socketed

### Add if Q1 = Gems or All
- Gem level/quality for all gems in main socket group
- `mcp__pob__suggest_support_gems` and `mcp__pob__compare_gem_setups` for the main skill
- Wiki page for the main skill gem if mechanics need verification

### Add for Bossing target (Q3)
- Boss readiness check: `mcp__pob__check_boss_readiness`
- Burst DPS calculations (flask uptime, charges full, vaal buffs active)

### Add for Mapping target (Q3)
- Atlas tree if accessible (currently no MCP coverage — read from `reference_data/atlastree/` directly)
- Map mod interactions (especially for ele-reflect / no-leech / no-regen)

---

## Step 3 — Analysis pattern

1. **Identify top 3 DPS bottlenecks** from the current build. Examples:
   - Crit multi shortfall vs crit chance ceiling
   - Missing damage conversion (e.g., flat phys not converted)
   - Aura effect not maximized
   - Single-element scaling when build is multi-element
2. **For each bottleneck, generate 1–3 candidate fixes.** Each must include:
   - Estimated cost (chaos / divines, from live prices)
   - Estimated DPS delta (use `mcp__pob__find_item_upgrades` or `compare_builds` when possible; estimate from mod math otherwise)
   - Dependencies (e.g., "needs +50 Strength elsewhere first")
   - Risk (corruption gamble, market volatility, requires respec, etc.)
3. **Prioritize by ROI** — DPS delta per chaos spent, within the locked-item constraints from Q4.
4. **Identify phase ordering** — group into Phase 1 (immediate, cheap), Phase 2 (moderate), Phase 3 (aspirational). The user can stop at any phase.

---

## Step 4 — Output shape

Write recommendations into `character_analyses/{League}-{CharacterName}.md` if it exists; otherwise propose creating one. Structure:

- **Current State** section (refreshed)
- **Gap Analysis** vs guide / vs target
- **Upgrade Path** with phases, each phase listing items with prices and impact
- **Open Questions / Follow-ups** for things needing user input
- **Decisions & Notes Log** dated entries appended chronologically

Surface key trade-offs that need user judgment rather than deciding silently (e.g., "Marylene's Fallacy boosts crit multi but breaks gem attribute requirements unless +50 Str is sourced elsewhere first").

---

## Step 5 — Pitfalls (lessons from past sessions)

These are concrete wrong-turns Claude has made before. Check these before promising specific mechanics.

### Conversion math
- **Phys → ele conversion kills "Gain X% of Physical as Extra Y" effects.** Winds of Fate (100% phys conversion) makes Divine Fury / Divine Wrath / Winter Spirit "gain extra" portions do nothing. Only the penetration portion survives, scaled by element-roll-uptime.
- **Phys-based leech is dead under full phys conversion.** Lust for Carnage's "1.5% Phys Attack Leeched as Life" stops working. Only the 12% attack speed remains.
- **Crit Chance is wasted under forced-100% mechanics.** Diamond Shrine (from Screams of the Desiccated) forces 100% crit. Crit chance notables become half-value (only crit multi portion alive). BUT only during mapping (flask-free); bossing with flasks turns Diamond Shrine off, so crit chance returns to relevance.

### Item mod misconceptions
- **Diamond Shrine does NOT grant elemental ailment immunity.** Freeze/chill/shock/ignite/bleed/poison come from OTHER shrines (Greater Freezing, Greater Shocking, etc.) or from flasks. See `reference_data/shrines.md`.
- **Body armour Eldritch implicits have NO `reduced mana cost of skills` mod** — that's helmet-only. Always check `reference_data/eldritch_implicits/` before promising a specific Eldritch mod.
- **Lapis Amulet natural implicit is +Intelligence ONLY** (no Strength). Build guides that recommend Marylene's Fallacy implicitly assume Strength is sourced elsewhere.
- **Screams of the Desiccated rolls exactly ONE shrine buff**, not all of them. Diamond + Greater Freezing on the same belt is impossible.
- **Double-corrupted uniques may have BOTH implicit slots overwritten**, losing the natural base implicit (e.g., losing Lapis Amulet's +Int when Marylene's gets double-corrupted).

### PoB / API quirks
- **`lua_set_tree` drops cluster jewel internal passives** on builds with Large Cluster Jewels (8 nodes consistently dropped in our test). Workaround: edit tree in PoB GUI or via in-game respec, then `lua_import_character` to sync.
- **`lua_set_tree` wipes all mastery effect selections.** `lua_import_character` preserves them.
- **`lua_set_tree` connectivity check is stricter than the actual game.** Nodes that PoE accepts as connected may fail in the API.
- **`add_item` to Flask 4 may also populate Flask 5** — verify after each flask add.
- **No API to clear/empty an equipped slot** as of 2026-05-21.
- **`lua_get_stats` slim output may lack CombinedDPS for some builds.** Use `get_build_stats` against the saved disk file, or read the right-side stat panel in PoB GUI.
- **Main skill matters for DPS calc.** If main skill is a warcry like General's Cry, CombinedDPS reads 0. Use `set_main_skill` to point at Cyclone (or whatever the actual damage skill is) before reading DPS.
- **`lua_reload_build` discards unsaved PoB GUI changes.** Confirm save state before reloading.

### PoB Notes tab
- The Notes tab in PoB is reserved for the user's own playstyle reminders. Detailed Claude analyses live in `character_analyses/`, NOT the Notes tab. After `lua_import_character`, the API auto-writes a brief import summary to Notes — that's fine; it's a 5-line marker, not an analysis.

---

## Trust hierarchy

See [`README.md`](README.md) section 5 for the standard ordering.
