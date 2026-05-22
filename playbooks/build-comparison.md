# Playbook: Build Comparison

For Claude sessions where the user wants to compare two builds — e.g. their current character vs a guide build, or two theory-craft variants. Builds can come from pobb.in/poedb.tw URLs, locally saved PoB files, or the currently loaded PoB build.

**Status: STUB** — workflow and pitfalls are established but this playbook has not yet been validated against a full real-session comparison. Flesh out Step 3, Step 4 output shape, and Step 5 pitfalls after the first complete comparison session.

Triggers: "compare my build to this guide", "how does my tree differ from X", "what would I need to change to match this build", two pobb.in URLs in the same message.

---

## Step 0 — Frame the work for the user

One sentence: *"Using the Build Comparison playbook — I'll diff the two builds from their XML first to find what matters, then simulate the meaningful differences in PoB."*

Key principle: **XML-first, PoB second.** Parse both builds structurally before touching PoB. This gives you the triage map cheaply, so PoB analysis is targeted at the 5-10 differences that actually matter rather than a blind full-build swap.

---

## Step 1 — Triage

Establish what the two builds ARE before diffing. Skip `AskUserQuestion` if context is already clear.

**Q1 — What's the comparison goal?**
- "Would build B's tree work better for my character?" → tree diff + stat simulation
- "Should I swap to build B's item in slot X?" → item diff + PoB slot simulation
- "How far is my build from this guide?" → full diff, then prioritize upgrades by impact
- "Academic curiosity / understanding a mechanic" → XML-only, no PoB simulation needed

**Q2 — Source of each build?**
- pobb.in or poedb.tw URL → fetch XML directly
- Currently loaded PoB build → `lua_get_tree` + `get_equipped_items`
- Local build file → `lua_load_build` then read state

---

## Step 2 — Data loads

### Always load
- Both build XMLs (or XML + live PoB state for the current character)
- `reference_data/skilltree/data.json` — for node name lookups (already local, fast)
- `character_data/{account}/{char}/meta.json` if one build IS the current character

### If the guide is a YouTube URL
Use `mcp__poemcp__fetch_youtube_description` (or `yt-dlp --get-description` via Bash as fallback).
Returns the video title, full description, and any pobb.in/poedb.tw/pastebin links extracted —
no API key needed, no browser needed.

```bash
yt-dlp --get-description "https://www.youtube.com/watch?v=..." 2>/dev/null
```

Build guide channels typically put the pobb.in link in the description alongside a Mobalytics/
written guide URL. Extract the pobb.in link and proceed to the XML fetch step below.

### Fetch pobb.in/poedb.tw XMLs
```python
# pobb.in
GET https://pobb.in/{id}/xml        # also try /json for metadata
# poedb.tw
GET https://poedb.tw/pob/{id}/xml
```
Both require `User-Agent: pob-mcp/1.0 (contact: github.com/charleslucas/poe_mcp_suite)`.

### What the XML contains (no PoB needed)
- `<Spec nodes="1234,5678,...">` — comma-separated allocated node IDs
- `masteryEffects="{nodeId,effectId},..."` — mastery selections
- `<Sockets><Socket nodeId="..." itemId="..."/>` — jewel socket assignments
- `<Override>` elements — tattoo/node overrides (hashOverrides)
- `<Skill>` elements — gem groups with levels/quality
- `<Item>` text blocks — full item text per slot
- `<PlayerStat stat="..." value="..."/>` — stored stat values (last PoB calculation)

### Add if Q1 = stat simulation
Load the current build's live state via `lua_get_tree`, `get_equipped_items`, `lua_get_stats`.

---

## Step 3 — Analysis pattern (STUB — validate with first real session)

### 3a — Structural diff (Python, no PoB)
1. Parse `nodes=` from both XMLs → two sets of integers
2. Compute: `only_in_A`, `only_in_B`, `shared`
3. Look up node names/types from `reference_data/skilltree/data.json`
4. **Filter to signal nodes first** — notables, keystones, jewel sockets, masteries. Travel smalls (`+10 Str`, `5% Life`, etc.) tell you about pathing, not build intent. Show them separately or on request.
5. Repeat for items (per-slot diff), gems (per-socket-group diff), stored stats delta

### 3b — Triage: what actually matters
Rank differences by likely impact:
- Keystone differences → always high impact (binary mechanic switches)
- Notable differences in the core damage/defense cluster → high impact
- Jewel socket count differences → moderate (cluster jewel budget)
- Item slot differences → check stored stat delta first; simulate if >10% stat change
- Travel node differences → usually just path routing, low impact unless they reveal a cluster jewel access point

### 3c — Targeted PoB simulation
Only for the high-impact differences identified in 3b. Do NOT load both full builds into PoB sequentially — that replaces the current build and loses context.

Instead, operate on the currently loaded build:
- **Tree differences**: `update_tree_delta` to add/remove specific notables → read stat delta
- **Item differences**: `add_item` in the target slot → read stat delta → revert with `clear_item_slot`
- **Gem differences**: swap individual gems with `add_gem`/`remove_gem` → read DPS delta

⚠️ **STUB**: the revert-after-simulation pattern (`clear_item_slot` + reload original) has not been validated end-to-end. First real session should establish whether it works cleanly or if `lua_reload_build` is needed to restore state.

---

## Step 4 — Output shape (STUB)

For quick comparisons (one specific question), a chat response is enough:
- What differs, ranked by impact
- Stat delta for the 2-3 most important differences (if simulated)
- Bottom line: "Build B's tree would give you X more life but costs Y DPS"

For full "how far am I from this guide" comparisons, append to `character_data/{account}/{char}/build.md` under a new section:

```markdown
## Comparison vs [guide name/URL] — YYYY-MM-DD
[summary of key differences and what they'd cost/gain]
```

⚠️ **STUB**: output format not yet validated. First session should establish whether appending to build.md is the right place or whether a separate comparison log is cleaner.

---

## Step 5 — Pitfalls (known so far — add more after first real session)

**Passive tree pitfalls**
- **Travel nodes bury the signal.** A diff of two Slayer builds can show 70+ node differences, but 60 of them are `+10 Str`, `6% Life` smalls. Always filter to notables/keystones/jewel sockets first; show smalls only on request.
- **Unknown node IDs** (e.g. 65568, 65570, 65578 in 3.28 builds) are new nodes not yet in the `reference_data/skilltree` preview export. Flag them as unknown, don't silently drop them — they could be significant new 3.28 nodes. Check back when GGG publishes the full release export.
- **`masteryEffects` is separate from `nodes=`** — both must be diffed. A build can have the same mastery node allocated but different effect selected.
- **Tattoo/override nodes** appear in `<Override>` elements, not in `nodes=`. A build with tattoos will show matching node IDs in `nodes=` but different stats when you look up those IDs. Compare `<Override>` sections separately.
- **The two builds must NOT both be loaded into PoB** — loading build B replaces build A in the GUI. Do the XML diff first, then load only what you need to simulate.

**XML fetch pitfalls**
- pobb.in `/json` has metadata (title, class, main skill) — fetch it alongside `/xml` in parallel for context.
- poedb.tw has `/xml` and `/raw` but no `/json` metadata endpoint (404). Use the HTML page title or the build XML's `<Build className=...>` attribute for context instead.
- Both platforms require a browser-like `User-Agent` — 403 without it.

**PoB simulation pitfalls**
- ⚠️ STUB: `clear_item_slot` + re-add original item as a revert mechanism has not been tested end-to-end. Validate this before relying on it.
- `update_tree_delta` with cluster jewel builds can drop cluster jewel internal passives (known bug, workaround: use PoB GUI for tree edits then `lua_import_character` to sync). Avoid `lua_set_tree` for builds with Large Cluster Jewels.

---

## When to extend this playbook

After the first full real-world comparison session, fill in:
- Step 3c: confirm the revert-after-simulation pattern works (or document the correct workaround)
- Step 4: validate the output shape — does appending to build.md make sense or is a separate file better?
- Step 5: add any new pitfalls discovered
- Remove all **STUB** markers from validated sections
