# Playbook: Build Comparison

For sessions where the user wants to compare two builds — e.g. their current character vs a guide build, or two theory-craft variants. Builds can come from pobb.in/poedb.tw URLs, locally saved PoB files, or the currently loaded PoB build.

This playbook is **sub-agent-first**: each build is parsed and digested in its own sub-agent context, so main context only sees compact summaries (~1.5K tokens per build) instead of raw XML (~50-100K per build). See [`README.md`](README.md) section 6 for the meta-criteria on when sub-agents earn their cost.

**Triggers:** "compare my build to this guide", "how does my tree differ from X", "what would I need to change to match this build", two pobb.in URLs in the same message.

---

## Step 0 — Frame the work for the user

One sentence: *"Using the Build Comparison playbook — I'll dispatch a sub-agent per build to fetch and digest each one in parallel, then diff the summaries here. This keeps main context light."*

**Before touching any build data:** run the standard pre-flight from [`README.md`](README.md) section 2 — context check, league reference, character snapshot if comparing against the user's current character.

**Gem and mechanic verification:** Your training data has a cutoff. New league gems, reworked skills, and changed interactions need verification from live sources before being used in analysis. Default: verify any gem that sounds new or that a guide creator describes as "new this league" via `mcp__poemcp__get_gem_detail` or `mcp__poemcp__fetch_wiki_page` before reporting its mechanics. Don't trust transcript descriptions alone — a past session learned that a creator described Void Shockwave Support as "drops from Uber Elder" when it's actually an Exceptional Support Gem (levels 1-3) socketed normally; the price and effectiveness claims were accurate, the drop source was not.

**Key principle:** sub-agents do the parsing, main context does the diffing. The agents are bounded I/O (fetch + parse + summarize); the insight work — what differs and why it matters — happens in main context where I can see both digests at once.

---

## Step 1 — Triage

Establish what the two builds ARE before dispatching agents. Skip `AskUserQuestion` if context is already clear.

**Q1 — What's the comparison goal?**
- "Would build B's tree work better for my character?" → tree-focused digest + stat simulation
- "Should I swap to build B's item in slot X?" → item diff + PoB slot simulation
- "How far is my build from this guide?" → full diff, then prioritize upgrades by impact
- "Academic curiosity / understanding a mechanic" → digest-only, no PoB simulation needed

**Q2 — Source of each build?**
- pobb.in or poedb.tw URL → sub-agent fetches XML directly
- Currently loaded PoB build → sub-agent uses live `lua_get_*` calls
- Local build file → sub-agent uses `lua_load_build` then reads state

**Q3 — Guide tier (if applicable)**
Many guides ship multiple pobb.in links (cheap/standard/aspirational/league-starter/endgame). Comparing tiers misleadingly inflates the diff. If the user gave one URL from a multi-tier guide, ask which tier — or have the build sub-agent fetch the Mobalytics/written-guide page for the tier label.

---

## Step 2 — Data loads (sub-agent first)

Dispatch one sub-agent per build in a **single message with parallel tool calls**. Total wall time is one agent's runtime, not N.

### Pre-flight
See [`README.md`](README.md) section 2. Two-build comparison via sub-agents typically costs 4-6K tokens in main context (two digests + diff work), down from 30-40K if you loaded raw XMLs and any transcripts inline.

### Sub-agent prompt template (use one per build)

Adapt and dispatch:

> Fetch and digest the Path of Exile build at `{source}`. `{source}` is one of:
> - A pobb.in URL (`https://pobb.in/{id}` — append `/xml` to get the XML, also fetch `/json` in parallel for metadata)
> - A poedb.tw URL (`https://poedb.tw/pob/{id}/xml` — no `/json` endpoint, use the build XML's `<Build className=...>` attribute for class info)
> - A local `.xml` path (read directly)
> - The literal string `CURRENT` (use `lua_get_tree(include_node_ids=true)`, `get_equipped_items`, `lua_get_stats(category='all')` on the currently loaded PoB build)
>
> Both pobb.in and poedb.tw require `User-Agent: pob-mcp/1.0`.
>
> Look up node names from `reference_data/skilltree/data.json`. If `reference_data/skilltree/data_patches.json` exists, apply it as an overlay before reading stats (see `reference_data/skilltree/PATCHES.md`).
>
> **Return a compact digest (under 1.5K tokens) in this exact format:**
>
> ```markdown
> ## Build: {name from pobb.in /json title, or filename}
> Source: {URL or path}
> Tier: {if multi-tier guide and tier is identifiable, otherwise omit}
> Class: {class} / {ascendancy}
> Level: {level from <Build level=...>}
>
> ### Tree — signal nodes only (no travel smalls)
> - Notables: {comma-separated list of names}
> - Keystones: {comma-separated list of names}
> - Jewel sockets allocated: {count, with large/medium/basic breakdown}
> - Masteries: {list, each as "Mastery Group: selected effect"}
> - Total allocated: {N}
>
> ### Main skill
> {skill name} — {N}-link in {slot}
> Supports: {comma-separated}
>
> ### Other socket groups (one line each)
> - {slot}: {gem list}
>
> ### Aura / reservation setup
> {list of skills with mana/life reservation, mark which is reserved}
>
> ### Equipped items by slot
> - Helmet: {unique name OR "rare: key mods: X, Y, Z"}
> - Body: ...
> - (one line per slot, including flasks and jewels)
>
> ### Stored stats (from <PlayerStat> elements — last PoB calc)
> Life: X | ES: Y | Mana: Z | Armour: A | Evasion: E
> Resists: Fire/Cold/Lightning/Chaos = F/C/L/Ch
> DPS: {CombinedDPS or whatever the build's main DPS stat is}
> Block: {attack/spell}
>
> ### Notes
> {anything unusual: tattoos in <Override>, hashOverrides, timeless jewels socketed, league-specific tech, items with cluster jewel internal passives, etc.}
> ```
>
> Do NOT load the full transcript, individual wiki pages for each unique, or any analysis beyond what fits the digest. The parent will request deeper dives on specific items if needed.

### Special case: if the guide source is a YouTube URL

Spawn a SEPARATE sub-agent (not the build digest agent) to extract author intent from the transcript. The build digest agent only needs the pobb.in link from the description; the transcript agent reads the prose.

> Fetch the YouTube transcript at `{URL}` via `mcp__poemcp__fetch_youtube_transcript`. The build is `{archetype}` ({class}/{ascendancy}). Extract and return, in under 800 tokens: (1) why specific notables were chosen, (2) mandatory vs optional items, (3) known build weaknesses or gotchas the author flagged, (4) playstyle notes (mapping vs bossing). Skip filler, sponsor reads, and gameplay commentary that doesn't inform build choices. If a Mobalytics or written guide URL is in the description, mention which tier(s) it documents.

### What you DON'T need in main context
- Raw XML strings of either build
- Full YouTube transcripts (delegated above)
- Wiki pages for each unique item — load only if a specific item becomes a decision point, via a single targeted `fetch_wiki_page`

---

## Step 3 — Analysis pattern

By the time Step 3 starts, you have two compact digests in main context. Diff happens here, where insight needs both readable at once.

### 3a — Structural diff
1. **Notables and keystones:** compute `only_in_A`, `only_in_B`, `shared`. Each digest already filtered to signal-only, so this is straightforward.
2. **Items per slot:** simple line-by-line comparison from the digests.
3. **Stored stats:** identify the largest deltas (DPS, life, EHP, resist caps).
4. **Aura/reservation:** different aura sets usually drive item differences (e.g., one build runs Determination, the other doesn't — that explains different armour values and different resist requirements).
5. **Masteries:** different mastery effects can be a hidden source of stat differences. The Reservation Mastery `+1% to all max ele res while life+mana reserved` is a common "secret defensive notable" worth flagging.

### 3b — Triage: what actually matters
Rank differences by likely impact:
- **Different main skill or support gem priority** → may invalidate the whole comparison. Flag and re-scope before continuing.
- **Keystone differences** → always high impact (binary mechanic switches).
- **Notable differences in the core damage/defense cluster** → high impact.
- **Unique item swaps with mechanic-changing effects** (conversion, +max res, charge generation, forced crit, etc.) → high impact.
- **Cluster Jewel differences** → usually high impact (whole-build-shape changes — different added notables, different jewel sockets, different small-passive bonuses). Use `mcp__pob__list_cluster_jewel_nodes` on each build (loaded one at a time) to get a clean per-cluster summary.
- **Timeless Jewel differences** → check both builds for Timeless Jewels via `mcp__pob__find_jewel_affected_nodes`. Different seeds → different transformations on the same allocated nodes. Different jewels socketed → entirely different transformed-node sets. Use `mcp__pob__get_tree_node_with_timeless_jewels` on key affected nodes to compare what the actual transformed stats look like in each build.
- **Radius-effect-unique differences** (Energy From Within, Healthy Mind, Might of the Meek, etc.) → run `mcp__pob__list_radius_effect_jewels` on each build. A swap from "no Energy From Within" to "Energy From Within with N Life passives in radius" is a meaningful effective-stat change that PoB applies internally but isn't visible in a node diff.
- **Stat delta >10%** for any major stat → worth simulating.
- **Mastery effect differences** → can be load-bearing (e.g., +1% max ele res); don't dismiss.
- **Threshold Jewel state differences** → if one build has a Brawn/Lethal Assault/etc. triggered and the other doesn't, that's a real effective-stat divergence. Use `mcp__pob__evaluate_threshold_jewels` to check.
- **Jewel socket count differences** → moderate (cluster jewel budget changes).
- **Travel node count differences alone** → usually low impact (pathing artifact unless it reveals a cluster jewel access point).

### 3b.5 — Budget reality check (when goal = "should I switch builds")
If the target build uses 2-3 expensive uniques (Mageblood, Headhunter, Forbidden Flame/Flesh, multi-divine rares), price-check them against current stash value before recommending the switch:
1. `mcp__poe__ninja_lookup` each expensive unique from the target digest
2. `mcp__poe__price_tab` or `mcp__poe__scan_stash_tabs` to estimate current stash value
3. Report the gap concretely: *"Mageblood costs ~40 div; your stash is ~8 div — aspirational tier is ~5× away."*

This prevents recommending Mageblood-tier builds to someone who just league-started.

### 3c — Targeted PoB simulation (only for high-impact differences)
Operate on the currently loaded PoB build. Do NOT load both full builds into PoB sequentially — loading build B replaces build A in the GUI and loses simulation state.

For each high-impact difference identified in 3b, simulate one at a time on the current build:
- **Tree differences:** `update_tree_delta` to add/remove specific notables → read stat delta. Use `update_tree_delta` (incremental, safer) over `lua_set_tree` for any build with Large Cluster Jewels.
- **Item differences:** `add_item` in the target slot → read stat delta → revert.
- **Gem differences:** swap individual gems with `add_gem`/`remove_gem` → read DPS delta.

**Revert pattern:** before each simulation, snapshot the slot/tree state. After reading the delta, restore. For tree deltas this means tracking what was added/removed and applying the reverse. `lua_reload_build` works as a nuclear revert if state gets tangled, but it discards any unsaved PoB GUI changes.

---

## Step 4 — Output shape

For quick comparisons (one specific question), a chat response is enough:
- What differs, ranked by impact
- Stat delta for the 2-3 most important differences (if simulated)
- Bottom line: *"Build B's tree would give you X more life but costs Y DPS."*

For full "how far am I from this guide" comparisons, append to `character_data/{Account}/{Character}/journal.md` (the chronological log) rather than `build.md` (the narrative doc). Entry structure:

```markdown
## YYYY-MM-DD — Comparison vs [guide name/URL]

### Builds compared
- A: {short name} ({source})
- B: {short name} ({source})

### High-impact differences
{ranked list with simulated stat deltas where applicable}

### Recommendation
{what to change, in priority order, with cost estimates}

### Notes
{anything notable about the comparison itself — e.g., tier mismatch caveats, mechanics that need verification}
```

This keeps comparison records discoverable in the journal alongside other decisions, with a consistent date prefix.

---

## Step 5 — Pitfalls

### Comparison setup pitfalls
- **Tier mismatch inflates diffs.** Guides ship multiple pobb.in links labeled cheap/standard/aspirational. Comparing a league-starter spec against an endgame spec produces a misleading 100+ node delta driven by gear, not build concept. Always identify which tier each build represents; ask the user if unclear.
- **Travel nodes bury the signal.** Two builds in the same archetype can show 70+ node differences where 60 are `+10 Str` / `6% Life` smalls. The sub-agent digest format filters these out by design — if you find yourself looking at raw `nodes=` lists for diffs, something went wrong with the digest.
- **`masteryEffects` is separate from `nodes=`.** Two builds can share a mastery node but have different effects selected — this is often the source of "why is build A tankier" surprises. The digest's Masteries section captures this.
- **Tattoo / override nodes** appear in `<Override>` elements, not in `nodes=`. The digest's Notes section should mention any overrides present.

### XML fetch pitfalls
- pobb.in `/json` has metadata (title, class, main skill) — sub-agent should fetch alongside `/xml` for context.
- poedb.tw has `/xml` and `/raw` but no `/json` endpoint (returns 404). Use the build XML's `<Build className=...>` attribute or the HTML page title for context instead.
- Both platforms require a browser-like `User-Agent`; they return 403 without it.

### Unknown node IDs
- Node IDs not present in `reference_data/skilltree/data.json` are likely new nodes from a patch the GGG export hasn't been re-tagged for. The sub-agent should flag them as "unknown ID {N}" in the Notes section, not silently drop them. If the discrepancy becomes load-bearing for a recommendation, follow the protocol in `reference_data/skilltree/PATCHES.md` to log a patch entry once the in-game stats are confirmed.

### PoB simulation pitfalls
- **The two builds must NOT both be loaded into PoB.** Loading build B replaces build A. Always do the digest diff first; load only the build you'll simulate against.
- **`lua_set_tree` drops cluster jewel internal passives** on builds with Large Cluster Jewels. Use `update_tree_delta` for tree edits in any cluster-jewel build.
- **`lua_set_tree` wipes mastery effect selections.** `lua_import_character` preserves them.
- **Mastery nodes are terminal in the tree graph.** You can allocate them but cannot route through them — neighbors that only connect via a mastery will be silently dropped on tree edits. See `tree-analysis.md` pitfall #1 for the full pattern.
- **GGG export staleness.** When a notable's stats are load-bearing for a decision, cross-verify against in-game tooltip or `mcp__pob__search_tree_nodes`. See `tree-analysis.md`'s pitfall on this and `reference_data/skilltree/PATCHES.md` for the correction workflow.
- **`lua_reload_build` discards unsaved PoB GUI changes.** Confirm save state before reloading.

### Sub-agent pitfalls
- **Don't dispatch sub-agents for trivial parses.** A single short pobb.in build that's only being skimmed for an item name doesn't need an agent — just fetch the `/xml` inline.
- **Don't ask sub-agents to do the synthesis.** Each agent digests its own build; comparison and recommendation happen in main context where I can see both at once and apply user-specific constraints (locked items, budget, playstyle).
- **Dispatch in parallel.** Multiple sub-agent calls in a single message run concurrently. Sequential dispatch defeats half the benefit.

---

## Trust hierarchy

See [`README.md`](README.md) section 5 for the standard ordering.
