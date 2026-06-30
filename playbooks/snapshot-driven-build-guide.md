# Playbook: Snapshot-Driven Build Guide

For a character that has **no external guide** (friend-built, theorycrafted, or a heavy adaptation) — or whose
guide you want to *author as it levels*. You periodically **import the live character from PoE, save a dated
PoB snapshot, diff it against the previous snapshot, and accrete a living guide** in the character's
`build.md` Progression Log. Over time the accumulated snapshots + narrative become a real build guide, and the
workflow itself is a **reusable template** for future characters.

**Triggers:** "snapshot my character", "let's build a guide as we go", "track this build as I level", "make a
template from this character", importing a character that has no `guides/` entry.

This is the *authoring* counterpart to `build-comparison.md` (which diffs two builds you already have) and
`character-leveling.md` (which plans milestones forward). Here you record what actually happened, snapshot by
snapshot.

---

## Step 0 — Frame the work for the user

One sentence: *"Using the Snapshot-Driven Build Guide playbook — I'll import your character from PoE, save a
dated PoB snapshot, diff it against the last one, and add a Progression Log entry to the living build.md."*

Narration notes specific to this playbook:
- Announce the **import** ("Importing <char> from the PoE API — this replaces whatever build is open in PoB").
- Announce the **snapshot save + copy** ("Saved via PoB to POB_DIRECTORY, copying into `snapshots/`").
- When diffing, state **what you're diffing against** ("vs snapshot #N from <date>, lvl <L>").
- If the build can't be fully modelled (minion DPS, unmodelled ascendancy), say so rather than reporting a
  misleading number.

**Before importing:** run the standard pre-flight (`README.md` §2) — context check, **character snapshot
(§2c: establish league/realm and whether it's an event character — this drives the scope filter)**, and the
freshness/mechanics scope (§2e). Event characters carry modelling caveats (see Pitfalls).

---

## Step 1 — Triage

Auto-derive before asking: read the character's `snapshots/` dir to get the snapshot number; run
`lua_list_characters` to get level/class/league. Then ask only what changes the work:

**Q1 — First snapshot or continuing?**
- *Snapshot #1 (new living guide)* → scaffold `meta.json` / `build.md` (living-guide skeleton) / `journal.md`
  / `snapshots/`; no prior to diff against.
- *Continuing (#N≥2)* → load the previous snapshot to produce a true snapshot-to-snapshot diff.

**Q2 — What triggered this snapshot?** (changes diff emphasis)
- *Level milestone* → emphasise tree growth + defensive scaling (life/res/EHP vs level).
- *Gear pass* → emphasise item diff + resover/under-cap + suppression.
- *Respec / rework* → emphasise the tree + gem-group diff (big deltas expected).
- *Just checking / ad-hoc* → light diff, focus on current priorities.

**Q3 — Original build or adapting an external guide?**
- *Original (no guide)* → the `build.md` Progression Log IS the guide; no `guides/` entry yet.
- *Adapting a guide* → also keep the `guides/<archetype>/` entry in sync (link it from `build.md`).

Skip questions whose answers are already obvious from context (e.g., a respec the user just described).

---

## Step 2 — Data loads

### Pre-flight
`README.md` §2 — context (`get_context_usage`), character snapshot (§2c, **establish event/league scope**),
freshness + mechanic-scope (§2e). A single import + snapshot + diff is typically 4–8K tokens in main context.

### Always load
- `mcp__pob__lua_list_characters(account_name)` — confirm the exact character name, level, class, **league**
  (the league sets the scope; e.g. `Ancestors` = event).
- `mcp__pob__lua_import_character(account_name, character_name)` — pulls tree/items/gems into PoB. **In TCP
  mode this replaces the build open in PoB.** The import response already reports level/node/item/gem/stat
  deltas **vs whatever was loaded** (see Pitfalls — that's not necessarily the last snapshot).
- `mcp__pob__lua_save_build("<League>-<Character>")` then **copy the XML from `POB_DIRECTORY` into
  `character_data/<Account>/<League>/<Character>/snapshots/<YYYY-MM-DD>_lvl<N>_<tag>.xml`**. `POB_DIRECTORY`
  is set in `.mcp.json` (NOT the default `%APPDATA%\...\Builds` — see Pitfalls).
- Read current state: `lua_get_build_info`, `get_skill_setup(main_only=false)`, `get_equipped_items`,
  `lua_get_stats(category='all')`.

### Add if Q1 = continuing (#N≥2)
- The previous snapshot's Progression Log entry in `build.md`.
- For a precise diff, load the previous snapshot XML first (`lua_load_build`/`lua_import_pobb` of the file),
  read its stats, THEN import the live character — so the import delta is genuinely snapshot-to-snapshot.
  (Cheaper alternative: read both XMLs' `<PlayerStat>` lines and diff in a small Python pass.)

### Add if Q2 = respec / rework
- Confirm the tree/gem-group deltas from the import summary; if load-bearing, `compare_trees` or a node diff.

### Add if Q3 = adapting a guide
- The `guides/<archetype>/README.md` + entry, to keep it in sync.

---

## Step 3 — Analysis pattern

1. **Establish the baseline you're diffing against.** Snapshot #1 has none. For #N, diff against snapshot
   #N-1 (its stats + tree/gem/gear), NOT against whatever build happened to be open in PoB.
2. **Compute the deltas that matter:** level, passive nodes (added/removed), skill groups/gems (added/levelled),
   items per slot, and the **defensive layer** (Life, ES, EHP, resists incl. over/under-cap, spell suppression,
   block) plus **DPS if it's modellable** (see caveats).
3. **Surface priorities** — the falsifiable, actionable findings: undercapped resists, low life-for-level,
   missing suppression, unlevelled gems, a reservation unique eating life (e.g. Midnight Bargain), a dead/empty
   link. These are the guide's "what to fix next."
4. **Apply modelling caveats** (don't report misleading numbers):
   - **Minion / trigger builds:** DPS does not show in `CombinedDPS`; select the minion/trigger as the main
     skill and read **`FullDPS`** (cf. `dps-analysis.md` / the Holy Relic case). If still unconfigured, say
     "DPS not modelled yet" rather than quoting the player's near-zero direct hit.
   - **Event characters with alternate ascendancies (Phrecia/Ancestor):** mainline PoB does NOT model the
     Phrecian ascendancy — its bonuses are dropped, so DPS/defence that depends on it is a **floor**. Flag it;
     use a Phrecia PoB fork if accuracy matters.
   - **Levelling characters:** bandit is not in the PoE API (**ask the user**); quest passive points may be
     incomplete (PoB assumes all → its point count runs slightly high).
5. **Write the next Progression Log entry** (Step 4) and update the live sections.

---

## Step 4 — Output shape

Everything lands in `character_data/<Account>/<League>/<Character>/`:

- **`snapshots/<YYYY-MM-DD>_lvl<N>_<tag>.xml`** — the dated PoB export (ISO date prefix so they sort).
- **`build.md`** — the **living guide**. Keep three things current:
  - *Current build* — concept, skill groups, key gear, defensive state.
  - *Priorities / watchlist* — the ranked "fix next" list.
  - *Progression Log* — append one entry per snapshot:
    ```markdown
    ### Snapshot #N — <YYYY-MM-DD>, lvl <L> (<trigger tag>)
    - File: snapshots/<file>.xml
    - State: <nodes>, skills/gear/stats summary (or "see Current build").
    - Changes vs #N-1: <tree / gems / gear / defensive + DPS deltas>.
    - Advice logged: <ranked priorities>.
    - Next snapshot target: <level / event>.
    ```
- **`meta.json`** — update `level`, `latest_snapshot`, `current_stats_snapshot`, `status`, `open_items`.
- **`journal.md`** — a dated line noting the snapshot + headline finding.
- **When the build matures**, a cleaned synthesis of the Progression Log can be promoted into
  `character_data/guides/<archetype>/` as a first-party guide entry (the snapshots are the evidence).

**Cadence:** snapshot every ~5–10 levels or on any major gear/respec change; record the trigger in the
filename `<tag>` and the Progression Log entry. Don't over-snapshot trivial changes.

---

## Step 5 — Pitfalls

- **The import diff is vs the LOADED build, not the last snapshot.** `lua_import_character`'s before/after
  columns compare against whatever was open in PoB (which may be an unrelated build). For a true
  snapshot-to-snapshot diff, load snapshot #N-1 first, or diff the two snapshot XMLs' `<PlayerStat>` lines.
- **`lua_save_build` writes to `POB_DIRECTORY`, not `%APPDATA%\Path of Building Community\Builds`.** In this
  install `POB_DIRECTORY` = `…\OneDrive\Documents\Path of Building\Builds` (see `.mcp.json`). Copy the snapshot
  from there. (Session 2026-06-30 lost a minute hunting the wrong dir.)
- **Minion/trigger DPS hides in `FullDPS`, not `CombinedDPS`.** A minion build can read ~0 CombinedDPS while
  doing fine — select the minion as main skill and read FullDPS, or state it's unmodelled.
- **Phrecian/alternate ascendancies aren't in mainline PoB** — class imports as Unknown/None and the
  ascendancy nodes are absent, so any number depending on them is a floor. Verify with `search_tree_nodes`
  (the notable won't be found) and flag it.
- **Bandit & quest points** aren't in the PoE API — ask for bandit; expect PoB's passive-point count to run
  slightly high for a mid-campaign character.
- **TCP mode replaces the open build on import.** Tell the user; don't `new_build`/`load_build_xml` (rejected
  in TCP). Confirm the user doesn't have unsaved PoB work open first.
- **Don't let `build.md` rot into the *old* build after a respec.** Move the abandoned plan to history (or its
  `guides/` archetype) and repurpose `build.md` for the current build — but keep the Progression Log's history.
- **Snapshot filenames:** ISO date + level + short trigger tag, e.g. `2026-06-30_lvl34_absolution-respec.xml`.
  Stable, sortable, self-describing.

---

## Trust hierarchy

See [`README.md`](README.md) §5. Note: the **live PoE API import is the ground truth** for what the character
*actually* is (tree/items/gems) — above any cached `build.md` description, which may lag the last snapshot.
