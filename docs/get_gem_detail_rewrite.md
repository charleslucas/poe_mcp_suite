# Spec: rewrite `get_gem_detail` to source from PoB game data (not poedb scraping)

**Status:** design / spec (2026-07-02). **Owner:** poe_mcp_suite. **Supersedes:** the poedb-scraping
implementation in `POEMCP/sources/player/gems.py` (interim guard already shipped — POEMCP `2df9223`).

## 1. Problem
`get_gem_detail` scrapes poedb HTML and mis-targets: the `div.gemPopup` elements it reads are the
**summoned-monster** tooltips (inside `col-monster` tab-panes), not the gem's own tooltip. Result: spells
returned as wand attacks, minion gems returned as their minion's default attack, and 0 popups for many
non-summon gems. poedb's data is correct — it's human-facing HTML that's ambiguous and inconsistent to
scrape (see investigation, POEMCP commit `2df9223`). An interim guard now suppresses the wrong tooltip and
returns the (correct) Level Effect table + a caveat. This spec replaces the scraping with the game's own data.

## 2. Goal
For any gem (active / support / Vaal / transfigured "of X"), return correct, structured data: name, tags,
active-skill-type, requirements, mana/cast/attack info, per-level stat scaling, quality bonus — sourced from
the game's own data, patch-current, unambiguous. Preserve the current markdown output shape so callers are
unaffected.

## 3. Data source decision (from the freshness check, 2026-07-02)

Ranked by freshness (freshest first):

| Source | Freshness | Notes |
|---|---|---|
| Raw game bundles (`Bundles2/`) via `pathofexile-dat` / PyPoE | freshest (the running game) | needs PoE install + extraction tooling; **runtime-only, never commit** (legal_considerations.md) |
| **Installed PoB `Data/*.lua`** (`%APPDATA%/Path of Building Community/Data/`) | **current** — 2.65.0, files dated 2026-04-23; updates when the user updates PoB | **PRIMARY.** `Gems.lua` + `Skills/*.lua` + `StatDescriptions/*.lua`. Parseable locally, no PoB running required |
| Live PoB via TCP (pob-mcp) | current (= installed PoB) | needs PoB running; pob-mcp already owns the connection |
| **Our fork `PathOfBuilding/src/Data`** (`POB_FORK_PATH`) | **~2 leagues STALE** (2.57.0 / 3.27 Keepers; `Gems.lua` untouched since Jun 2025) | **DO NOT USE** until the fork is synced (see the fork-sync task) |

**Decision:**
- **Primary source = the INSTALLED PoB's `Data/` Lua files** (current, local, no TCP dependency). Path
  configurable (env, default the PoB Community install dir). NOT the stale `POB_FORK_PATH` copy.
- **Fallback = raw game-file extraction** (`pathofexile-dat`/PyPoE against the local install) for content
  newer than the installed PoB — the post-patch window and un-modelled event content (e.g. this is exactly
  why PoB 2.65.0 lacks the June Phrecian ascendancies). Runtime-only; never commit extracted data.
- **Version guard:** at query time read the installed PoB version (`changelog.txt` → `VERSION[x.y.z]`) and
  compare to the latest PoB release + current game patch (reuse the session-start freshness check). If PoB
  lags, emit a freshness note and optionally trigger the raw fallback.

## 4. Parsing approach (PoB Lua data)
1. **`Gems.lua`** — keyed by `Metadata/Items/Gems/SkillGem<Name>`; each entry has `name`, `baseTypeName`,
   `grantedEffectId`, `variantId`, and variants (base / `Vaal…` / `…AltX` transfigured). Resolve the query
   name → entry(ies); handle variants explicitly (base vs Vaal vs "of X").
2. **`Skills/*.lua`** (`act_str/int/dex`, `minion`, `spectre`, `sup_*`, `glove`, `other`) — look up the
   `grantedEffect` by id → tags, per-level stat arrays, base damage, mana/cost, requirements, quality stats.
   (Absolution's granted effect is in `act_str.lua`; its Sentinel minion skill is in `minion.lua`.)
3. **`StatDescriptions/*.lua`** — translate raw stat ids + values into readable lines ("Deals X to Y Physical
   Damage"). ⚠ These templates are the "runtime-only creative content" per `legal_considerations.md`: read
   the installed PoB's copy at runtime; **never commit** them.
4. **Lua-from-the-host:** parse via the existing **LuaJIT** dependency (`POB_CMD` = luajit) — load the PoB
   data with PoB's own loader and dump JSON — rather than a fragile Python Lua parser or regex. This reuses
   PoB's own data model and is what pob-mcp headless already does.

## 4b. VALIDATED implementation recipe (explored live 2026-07-09, PoB 2.65.0)

Rather than parse `Data/*.lua` files, **read PoB's already-parsed in-memory data via a new API action** and
reuse PoB's own renderer. Confirmed functions/fields in the fork (now synced to 2.65.0):

- **Gem lookup:** `data.gemForBaseName[name:lower()]` → gemId → `data.gems[gemId]` (call it `gem`).
  `gem.grantedEffect` = the resolved granted effect. Variants share `gem.gameId` via
  `data.gemsByGameId[gameId]` (base / `Vaal…` / transfigured `…AltX`). `gem.secondaryGrantedEffect` = Vaal
  half.
- **Tags:** `gem.tagString` (ready human string) + `gem.tags` (set). **Type:** `grantedEffect.support` (bool).
  **Flavor:** `grantedEffect.description`. **Cast:** `grantedEffect.castTime`.
- **Per-level fields:** `grantedEffect.levels[n]` → `.levelRequirement`, `.critChance`,
  `.damageEffectiveness` (×100 for %), cost/mana. Max level = `#grantedEffect.levels`.
- **Per-level stat lines (THE renderer):**
  `local inst = { level = n, quality = q, gemData = gem }`
  `local stats = calcLib.buildSkillInstanceStats(inst, grantedEffect)`  -- assembles {statName=value}
  `local descriptions = data.describeStats(stats, grantedEffect.statDescriptionScope)`  -- English lines
  (This is exactly `GemSelectControl.lua`:734-740 and `SkillsTab.lua`:777. `data.describeStats` =
  `Modules/StatDescriber`.)
- **Quality lines:** iterate `grantedEffect.qualityStats` as `{statName, valPerQual}`; render at +20% via
  `data.describeStats({[stat]=val*20}, scope)` (SkillsTab.lua:773-777).
- **Requirements:** `calcLib.getGemStatRequirement(reqLevel, grantedEffect.support, gem.reqStr/reqDex/reqInt)`.
- **Deps in the API scope:** `data` (global) + `calcLib` (`require("Modules/CalcTools")`) — both already
  available to the fork's `src/API/BuildOps.lua` (headless + TCP). No build needs to be loaded — this reads
  static game data, so it works even with no character open.

Suggested action shape: `get_gem_detail(gemName, levels?)` → `{ name, tags[], support, castTime, description,
variants[], requirements{level,str,dex,int}, perLevel: [{level, levelRequirement, critChance,
damageEffectiveness, cost, statLines[]}], qualityLines[], provenance: "PoB <version> data" }`. Handler formats
to the markdown shape in §6. Selected levels: 1, ~mid, max (mirror the current output).

**Test loop caveat:** changing `src/API/*.lua` requires re-running `InstallTcpApi.ps1` + **relaunching PoB**
(it loads the API Lua at startup) before a live `lua_*` test — or build a headless luajit harness. Plan for
that iteration cost; it's the main reason this is a focused multi-step build, not a one-shot.

## 5. Architecture decision (open — recommend option A)
The real gem data + a LuaJIT/PoB pipeline already live in **pob-mcp** (headless luajit against a PoB checkout,
plus live TCP). `POEMCP` is Python with no PoB connection. Options:

- **(A, recommended) Put gem-detail in pob-mcp.** Add a `get_gem_detail` (and structured `search_gem`) tool
  to pob-mcp that reads the **installed** PoB `Data/` via luajit (or live TCP when connected). Point POEMCP's
  `get_gem_detail` at it (delegate) or deprecate it. Keeps a single PoB-data pipeline; no duplication. Note:
  pob-mcp's headless path currently uses the **stale fork** (`POB_FORK_PATH`) — this tool must read the
  **installed** PoB data (or the fork must be synced first).
- **(B) Keep it in POEMCP**, shelling out to `luajit` to dump the installed PoB data → JSON → format. Keeps
  the tool where it is, but duplicates a mini PoB-data loader in Python-land.

`skillGemService.ts` in pob-mcp is a *hand-curated* database for support-gem suggestions (synergies, cost
tiers) — **not** a full gem-data source; the rewrite should not conflate the two, though it could enrich it.

## 6. Output shape (unchanged for callers)
Preserve the markdown: `# {name}`, `**Tags:** …`, property lines (skill type, cost, cast/attack time,
requirements), `**Stats:**` (description lines), `**Quality bonus:**`, `**Level Scaling (selected levels):**`
table (levels 1/10/20 + max), and a source link. Add a one-line provenance/version footer (e.g. "source: PoB
2.65.0 data").

## 7. Testing / acceptance
Validate against in-game tooltips for: **Absolution** (spell+minion), **Raise Zombie** / **Summon Skeletons**
(minion), **Fireball** (spell), a support (**Spell Echo**), a **transfigured** gem ("… of …"), and a **Vaal**
variant. Each must return the *gem's own* tags/skill-type (never a Default Attack), correct per-level stats,
and correct variant. Regression: the interim guard's caveat path should no longer trigger for known gems.

## 8. Rollout
1. Implement behind the current interim guard (guard stays as a safety net).
2. Wire the version guard + raw fallback (or at minimum the freshness warning).
3. Validate (§7); then make PoB-data the default path and demote poedb scraping to last-resort only.
4. Update `TOOLS.md` / tool description to note the data source.

## 9. Open questions
- Tool location: **A (pob-mcp)** vs B (POEMCP)? (Recommend A.)
- Do we implement the raw-extraction fallback now, or ship PoB-data + a freshness *warning* first and add raw
  extraction later? (Recommend: warning first, raw fallback as a follow-up.)
- Does reading the **installed** PoB dir (vs `POB_FORK_PATH`) need a new env var, or reuse an existing PoB
  path config?

## 10. Dependencies / related
- **Fork sync** (separate task): syncing `PathOfBuilding` (and other forks) with upstream would make
  `POB_FORK_PATH` current again — but the recommended primary source is the *installed* PoB regardless, so
  this rewrite is not blocked on it.
- `legal_considerations.md`: StatDescriptions + any raw-extracted mod/description data are runtime-only.
