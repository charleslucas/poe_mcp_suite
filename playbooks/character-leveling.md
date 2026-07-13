# Playbook: Character Leveling Plan

For sessions where the user wants a structured leveling plan — gear schedule, passive tree progression, gem setup, and PoB milestone builds — for a character that isn't yet at endgame. Covers both "I have endgame gear pre-farmed and need a plan to use it" and "plan me a path from scratch."

**Triggers:** "what gear should I use while leveling", "when do I equip X", "make a passive tree plan", "create milestone builds", "leveling guide for my character", or any session that involves a sub-100 character with a clear endgame build target.

---

## Step 0 — Frame the work for the user

*"Using the Character Leveling playbook — I'll import the character, scan the stash for pre-farmed gear, check the build concept, then create milestone PoB builds (every 20 levels) with gear schedule, passive tree, and gem setup at each checkpoint."*

This is always a **detailed analysis** — apply the cursory/detailed gate from [`README.md`](README.md) section 1: present the stage list and wait for approval before loading data.

---

## Step 1 — Triage

Establish the shape of the work before loading anything. Several of these can be auto-derived.

**Auto-derive (read before asking):**
- Character class and level: `mcp__pob__lua_list_characters` (or `mcp__poe-trade-mcp__get_character`)
- Pre-farmed gear: ask which stash tab(s) hold the leveling/endgame gear, then `mcp__poe-trade-mcp__get_tab`

**Ask the user:**
1. **Build concept** — what's the endgame goal? Class, main skill, ascendancy target. Without this, gear and passive recommendations can't be prioritized correctly.
2. **Milestone granularity** — every 20 levels (default), or at specific gear checkpoints?
3. **Existing guide?** — pobb.in URL, YouTube link, or "build from scratch"? Guides collapse the build-design phase to a parse call; from-scratch needs more triage.

---

## Step 2 — Data loads

### Always load
| Source | Tool | Notes |
|--------|------|-------|
| Character current state | `mcp__pob__lua_import_character` or `mcp__poe-trade-mcp__get_character` | Level, class, equipped items, allocated nodes |
| Pre-farmed gear stash | `mcp__poe-trade-mcp__get_tab` | Gets item list with level requirements — forms the gear schedule |
| Context usage | `mcp__pob__get_context_usage` | Check headroom before loading guide builds or transcripts |

### Add if a guide build is provided
| Source | Tool | Notes |
|--------|------|-------|
| Guide build XML | `mcp__poe-data-mcp__parse_pob` | Use for triage only — don't load into PoB until you know the class matches |
| Mechanic verification | `mcp__poe-data-mcp__fetch_wiki_page` | Any mechanic that sounds like a bug exploit, "infinite", or "immortal" — verify current state before building around it |
| YouTube transcript | `mcp__poe-data-mcp__fetch_youtube_transcript` | Only if gems/interactions need verbal explanation not in XML |

### Add if building from scratch (no guide)
- `mcp__pob__search_tree_nodes` for key archetype notables
- `mcp__poe-data-mcp__fetch_wiki_page` for the main skill gem

---

## Step 3 — Analysis pattern

### 3a — Build concept triage
Establish the endgame identity before planning the path to it:
- **Damage type** (determines which passive clusters matter, which gear mods are load-bearing)
- **Defense profile** (life? ES? hybrid? — determines tree direction from the class start)
- **Key mechanics** (auras that need free reservation, spectres/minions, curse interactions)
- **Ascendancy order** (which lab unlock matters most for the build to function)

If adapting a guide from a different class (e.g. Guardian guide → Witch/Necromancer), explicitly map out what the original ascendancy provided and what the adapted ascendancy replaces. Don't assume the tree paths will be similar.

### 3b — Gear schedule
From the stash scan, sort items by `LevelReq` ascending. For each item:
- Note what slot it replaces and what it unlocks (resistance fix, key aura, spectre corpse, etc.)
- Identify gaps (slots not covered by pre-farmed gear — needs placeholder rares)
- Flag items whose utility changed due to hotfixes or patches (verify before building around them)

### 3c — Passive tree planning (milestone by milestone)
Work through each 20-level checkpoint. For each milestone:

1. **Calculate point budget:** level - 1 + estimated quest rewards (Acts 1–2 ≈ 4, Acts 1–4 ≈ 10, all acts ≈ 18–24) + bandit choice
2. **Identify target notables** for this milestone: prioritize by impact-per-point (notables adjacent to the current frontier are often 1–3 nodes; distant keystones may cost 8–10)
3. **Find exact paths** using `find_path_to_node` for each target notable — **do not rely on `update_tree_delta` auto-pathing for nodes more than 2–3 steps from the frontier** (it often fails to connect)
4. **Merge shared prefixes manually** before calling `lua_set_tree` — if two notables share a 4-node path prefix, count those 4 nodes once
5. **Set tree via `lua_set_tree`** with the complete node list (class start nodes + all path nodes + all notables + ascendancy nodes)

**Ascendancy timing:**
- Lab 1 (Normal, Act 3, ~level 33): First notable — usually the one that changes how the build functions most (resistances, damage, or key mechanic enabler)
- Lab 2 (Cruel, ~level 55): Second notable
- Lab 3 (Merciless, ~level 68): Third notable
- Lab 4 (Uber, ~level 75+): Fourth notable

### 3d — Build each milestone in PoB
For each milestone (levels 20, 40, 60, 80, 100):

1. `mcp__pob__set_character_level` to the milestone level
2. `mcp__pob__lua_set_tree` with complete node list
3. `mcp__pob__setup_skill_with_gems` for all skill groups
4. `mcp__pob__add_item` for all gear that becomes available at or before this level
5. `mcp__pob__lua_get_stats` to confirm stats are reasonable
6. `mcp__pob__lua_save_build` as `{CharacterName}-{level}.xml`
7. `mcp__pob__set_build_notes` with a self-contained summary (see output shape below)

**Gem group management:** When updating gem groups from milestone to milestone, remove obsolete groups before adding new ones. Indices shift on removal — remove from highest index to lowest to preserve lower indices.

### 3e — Create progression.md
Write `character_data/{account}/{char}/progression.md` with the full schedule:
- Phase headers with level ranges
- Gear unlock table (item | level req | slot | what it replaces | why it matters)
- Passive priorities per phase
- Gem setup at each phase
- **Checkpoint tolerances per phase** — the pass/fail floors a mid-leveling checkpoint
  (Step 6) tests against: res targets by act, rough life floor, main-link size, key gem
  levels. These make "am I on track?" answerable in seconds.
- Open questions / farming needs

This is the player-facing document; it should be readable without opening PoB.

---

## Step 4 — Output shape

### Files created
| File | Location | Purpose |
|------|----------|---------|
| `{Character}-20.xml` through `{Character}-100.xml` | PoB builds folder | Milestone PoB builds — open in PoB to simulate any stage |
| `progression.md` | `character_data/{account}/{char}/` | Human-readable leveling schedule |
| `meta.json` (update) | `character_data/{account}/{char}/` | Add `ascendancy_target`, `build_concept`, `ascendancy_plan` |
| `journal.md` (append) | `character_data/{account}/{char}/` | Session summary entry |

### PoB Notes tab content (per milestone build)
Each milestone build's Notes tab should be self-contained:
```
# {Character} — Level {N} Snapshot
{Class} → {Ascendancy} | {Main skill} | {League}

## This file represents: {brief description}

## Gear
[table of slot | item | note]

## Gems
[table of setup | gems | slot]

## Passive notables (new since previous milestone)
[bullet list]

## Next steps
[what to do before the next milestone]
```

### guides/ entry
If the build archetype is novel (not already in `character_data/guides/{archetype}/`), create:
- `guides/{archetype}/README.md` — consensus notes, best guide by tier, pitfalls
- `guides/{archetype}/{author}_{league}_{pobb_id}.json` — structured entry for the source guide

---

## Step 5 — Checkpoint & reconvergence (the drift loop)

**Plans are aspirational corridors, not scripts.** Real leveling drifts — found gear
replaces planned gear, passive picks get improvised, pace varies. The plan's job is to
make reconvergence *cheap*, and this loop is the recurring in-league procedure for:
*"I just levelled N times with gear I found and some nodes I picked — how close am I to
the plan, and how do I track back?"*

**Triggers:** every ~10–15 levels, after each lab, entering a new act tier, or on request
("am I on track?"). Cursory-to-light scope — minutes, not a full analysis.

1. **Import reality:** `lua_import_character` (league explicit). Read `progression.md`'s
   current-phase tolerances.
2. **Pick the reference = the nearest milestone AT OR BELOW current level** — never the
   endgame build (a lvl-34 char vs the lvl-100 aspiration measures nothing). Between
   milestones, pro-rate the point budget.
3. **Cheap diff** (digest-style, per build-comparison's format; no sims yet):
   - *Tree:* planned notables present / missing / extra. Travel-small differences are
     noise — compare **notables + keystones + masteries**, not raw node lists.
   - *Gear:* judge each found item by the **slot's job in the plan** (res, life, minion
     levels, trigger craft), not item identity. A random rare that caps res IS the plan.
   - *Gems:* main-link size and **gem levels** (minion builds scale on levels — an
     underleveled main gem is real drift; also check weapon-swap gems are soaking XP).
   - *Tolerances:* pass/fail against the phase floors from progression.md.
4. **Classify every divergence — four kinds, two directions:**
   - **Benign** (equivalent path/rare): ignore, note nothing.
   - **Beneficial** (found gear/pick beats the plan): **converge the PLAN to the
     character** — amend progression.md and, if generalizable, the archetype trunk. Drift
     is not always error; sometimes reality wins.
   - **Drift-to-fix** (missing load-bearing notable, res under cap, wrong bridge
     support): goes in the track-back list.
   - **Blocked** (planned item/gem unavailable or unaffordable): plan a substitute now,
     don't leave a hole.
5. **Track-back plan, ordered by cost:** free fixes first (gem swaps, stash gear), then
   respec-point spends (count available quest refunds), then purchases. If a fix is
   load-bearing, verify it in the milestone PoB before recommending. Hand deep tree work
   to `tree-analysis`, purchases to `gear-shopping`.
6. **Record:** one journal entry (drift found → decisions), tick/annotate the
   progression.md checkpoint. Plan amendments from (4b) update the doc so the *next*
   checkpoint measures against amended reality.

---

## Step 6 — Pitfalls

### Passive tree planning
- **`update_tree_delta` is unreliable for nodes more than 2–3 steps from the tree frontier.** It often silently drops nodes with "total count lower than expected." Use `find_path_to_node` to get the exact intermediate node IDs, then set the entire tree at once with `lua_set_tree`.
- **1–2 nodes are frequently dropped by `lua_set_tree`** due to PoB's stricter connectivity validation vs. the game itself. This is usually harmless — check which node was dropped and manually allocate it in the PoB GUI tree view if it matters.
- **Point budget:** PoB level = passive points from levels only. Quest passive rewards are not automatically accounted for. Include them in the budget manually (Acts 1–2 ≈ 4, full playthrough ≈ 18–24). If a milestone has leftover points, note them as "unallocated — fill with X" in build notes.
- **Merging paths:** When multiple notables share a path prefix, only count those prefix nodes once. A 5-node path + a 6-node path sharing a 3-node prefix = 5+6-3 = 8 total nodes, not 11. Manually inspect `find_path_to_node` results before summing.

### Hotfix and mechanic verification
- **Any mechanic described as "immortal", "infinite", or known to be a bug exploit** — always verify current state via `mcp__poe-data-mcp__fetch_wiki_page` before building the character around it. The Rongokurai's Boon / Temporal Chains interaction was hotfixed within hours of the Reddit post going live; the wiki will show the current behavior.
- **Ghost Reaver conflicts with Wicked Ward.** Ghost Reaver says "Cannot Recharge Energy Shield" — taking both makes Wicked Ward useless. Don't combine them.
- **Zealot's Oath is 1 passive point and converts all life regen to ES regen.** For any ES build with significant life regeneration on gear, this is often the single highest-value passive in the build.

### Class adaptation
- **When adapting a guide from a different class**, explicitly map what the original ascendancy provided and what the new ascendancy replaces. Don't assume tree paths will be similar — Witch and Templar start at completely different tree positions. Spiritual Aid / Spiritual Command (minion bonuses apply to player) may be reachable from either, but the path cost differs significantly.
- **Garb of the Ephemeral** ("Nearby Allies' Action Speed cannot be modified to below Base Value") is often load-bearing in Guardian builds that use Temporal Chains self-curse. Witch builds using this mechanic need an alternative (Kaom's Roots, Juggernaut Unstoppable, or dropping the self-TC entirely).

### Item handling
- **`add_item` with PoB item text format** works reliably for unique items and rares. Use the stash API data to reconstruct the text: `LevelReq` from requirements, `Implicits: N` count before the implicit mods, then explicit mods one per line.
- **Sockets in `add_item` text** use dash notation: `Sockets: B-G-B-R` for a 4-link. Disconnected groups use spaces: `Sockets: B-B B`.
- **Gem group indices shift on removal.** Always remove from highest index to lowest to avoid off-by-one errors.

### Guides/ conventions
- Create a guides/ archetype when the build concept is reusable across characters or leagues (not character-specific). Character-specific progression lives in `character_data/{account}/{char}/progression.md`; archetype consensus lives in `guides/{archetype}/README.md`.
