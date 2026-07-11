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
- Read live from stash via `mcp__poe-trade-mcp__list_tabs` + `mcp__poe-trade-mcp__price_tab` BEFORE asking. Only ask if the stash read fails or returns nothing useful. Present the computed budget back to the user for confirmation: "I see ~X chaos / Y div in your stash. Use this as the budget?"
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

> **Current-league free damage:** check whether the league offers a cheap damage add. **Mirage:** a **Djinn
> coin** (Coin of Power/Skill/Knowledge, matched to the skill's attribute) imbues a random support on a
> finished lvl-20, 6-linked gem ≈ a free 7th link — a real DPS lever on the main skill. See
> `reference_data/leagues/{league}.md` → Djinn Coins, and the model-aware `reference_data/freshness_index.md`.

### Always load
- Pre-flight: `mcp__pob__get_context_usage` + league reference + character snapshot (see [`README.md`](README.md) section 2)
- Build profile + constraint margins: see [`README.md`](README.md) §2d. Sections 3+4 define which stats are the actual DPS levers for this build — critical for identifying the right bottlenecks in Step 3 rather than chasing generically-good mods that don't move this build's damage.
- Character live state: `mcp__pob__lua_get_stats` (TCP) or `mcp__pob__get_build_stats` (disk)
- Equipped items: `mcp__pob__get_equipped_items`
- Main skill setup: `mcp__pob__get_skill_setup`
- Character journal if it exists: `character_data/{Account}/{League}/{Character}/journal.md`

### Add if Q1 = Gear or All
- League context (current league name affects ninja prices, mod pool, league mechanics): `mcp__poe-data-mcp__currency_overview`
- Trade API stat IDs for mods we're about to search: `mcp__poe-trade-mcp__get_stat_ids`
- Eldritch implicit pools from `reference_data/eldritch_implicits/` if any helmet/body/glove/boots are uniques or rares being recrafted
- Wiki page for each equipped unique if its mechanics are non-obvious: `mcp__poe-data-mcp__fetch_wiki_page`

### Add if Q1 = Tree or All
- Full passive tree allocation: `mcp__pob__lua_get_tree` with `include_node_ids: true`
- Build guide tree section if a guide is referenced in the character doc
- `mcp__pob__find_path_to_node` for any candidate new allocations
- `mcp__pob__get_tree_node` for "what does this node give me?" lookups (replaces ad-hoc Python BFS on `data.json` for single-node questions; always-current via PoB's `tree.lua`)
- **If any jewels are socketed:**
  - `mcp__pob__find_jewel_affected_nodes` — surfaces which allocated nodes are transformed by Timeless Jewels. Run this before assuming a node's tooltip stats; the in-game tooltip may differ.
  - `mcp__pob__get_tree_node_with_timeless_jewels` — returns the actual transformed stats for a specific affected node. Use this when a Karui-flavored Strength addition or a Vaal-flavored Crit Multi addition might be juicing a node beyond its base data.
  - `mcp__pob__list_cluster_jewel_nodes` — surfaces what each Cluster Jewel contributes (notables, sockets, small-passive bonuses). Cluster notables are often the highest-leverage DPS stats in the build.
  - `mcp__pob__evaluate_threshold_jewels` — checks "With at least N <Attr> in Radius" triggers. If a tree change moves the build above/below a threshold, the effective DPS shifts even though tooltip stats don't.
  - `mcp__pob__list_radius_effect_jewels` — catches the long tail of "in Radius" uniques (Energy From Within → Life-to-ES conversion in radius, Healthy Mind → Life-to-Mana in radius, Might of the Meek → multiplied notable effect in radius, etc.). Important because the numeric effect is rolled into `lua_get_stats` totals but isn't visible per-node; if a tree edit removes a node from radius, the total shifts.

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

### Delegate to sub-agents (see [`README.md`](README.md) section 6)

If the analysis pulls **3+ guide transcripts** (synthesizing recommendations from multiple build guides), or **3+ wiki pages for non-trivial mechanic verification**, delegate each to a sub-agent rather than loading inline. A single transcript is ~10-12K tokens; three of them in main context can blow the budget before analysis starts.

Sub-agent prompt template for transcript extraction:
> "Fetch the YouTube transcript at `{URL}` via `mcp__poe-data-mcp__fetch_youtube_transcript`. The build is `{archetype}` ({class}/{ascendancy}). Extract and return, in under 800 tokens: (1) skill links and support gem priority, (2) key passive notables and ascendancy choices, (3) gear: must-have uniques + key rare mods per slot, (4) playstyle notes (mapping vs bossing, defenses), (5) anything the author flagged as a known weakness or gotcha. Skip filler, jokes, sponsor reads, and gameplay commentary that doesn't inform the build."

Dispatch multiple transcripts in a **single message with parallel sub-agent calls** so they run concurrently — total wall time is one transcript's, not N.

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
   - **Craft vs. buy signal**: for any gear fix, run `search_craft_mods(target_mod)` to check if the target mod is in the craftable pool. If so, note whether crafting is likely cheaper or more accessible than the market at the user's budget. Crafting is worth flagging when the item needs only 1–2 mods (low expected cost) or when trade listings are thin/overpriced. Direct the user to the craftofexile Calculator for actual odds.
3. **Prioritize by ROI** — DPS delta per chaos spent, within the locked-item constraints from Q4.
4. **Identify phase ordering** — group into Phase 1 (immediate, cheap), Phase 2 (moderate), Phase 3 (aspirational). The user can stop at any phase.

---

## Step 3b — Minion builds (run whenever damage lives in minions)

The main-skill DPS readout **under-reports every minion build** — PoB computes one skill at a time, and swarm totals only exist through the Full DPS system. Before any bottleneck analysis on a minion build:

1. **Verify the Full DPS configuration in PoB** — this is where minion numbers silently go wrong:
   - Every damage-contributing socket group (each minion type, triggered novas, ballistas) needs **"Include in Full DPS"** checked in the Skills tab.
   - Each group's **"Count" field must be set manually** to the real active quantity (10 zombies, 4 relics…). PoB does **NOT** auto-multiply by the minion limit — an unset Count silently counts the group once. Cross-check against the build's actual limits.
   - Trigger-based minions (Holy Relic) scale with the **player's** trigger rate — verify attack rate/CDR config matches reality (the guide library has CDR breakpoint tables for Holy Relic).
   - Spectre selection, minion gem levels, and EE/curse ownership are all part of config, not just gear.
2. **Get the swarm table**: `mcp__pob__minion_dps_breakdown` — per-skill DPS × count, share of total, from PoB's cached calc (free). If it reports nothing flagged, fix step 1 first; recommendations made from main-skill DPS alone on a swarm build are wrong.
3. **Stat weights**: `mcp__pob__compute_stat_weights` auto-detects minion builds and switches to a minion probe battery (+1 minion gem levels, minion damage/speed/life, player trigger speed). With Full DPS configured, probe deltas measure the whole swarm; without it, they measure the main skill's minion only — the output says which.
4. **Apply uptime haircuts to PoB-perfect numbers.** PoB assumes every minion attacks continuously; real minions lose damage to AI, travel, and retargeting. Community rules of thumb (verify per archetype from guides): stationary/boss fights ~90–95% for ranged and triggered minions; melee minions on mobile targets ~60–80%; AG/support minions contribute buffs, not listed DPS. State the haircut used when reporting real-world estimates.
5. **Minion survivability is DPS.** Dead minions deal nothing — minion life/resist probes and AG gear checks belong in the defense half of the analysis for any build whose minions die in content.

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
