# Guide Source Index — external build-guide aggregators & discovery resources

**Purpose:** A bookmark index of *external* sites that list/aggregate many PoE build guides — for
**discovery** ("what builds exist around skill/mechanic X", "what's the current meta"). This is distinct
from the per-archetype folders in `character_data/guides/{archetype}/`, which hold guides that have actually
been **digested** for a specific build.

**Committed (not cached):** this file travels with the suite (gitignore exception, like `freshness_index.md`)
because a curated source list is useful to every clone — unlike the per-character digested guides, which live
in the gitignored `character_data/` cache.

**Workflow:** Use these to *find* a candidate guide → then digest it into a
`character_data/guides/{archetype}/` folder via the build-design / build-comparison sub-agent pattern (one
sub-agent reads the guide, returns a compact digest; see `playbooks/build-comparison.md` §Step 2). Don't
paste a whole aggregator page into main context.

**Trust / freshness reminder** (full hierarchy in `playbooks/README.md` §5): these are secondary sources.
For *empirical* "what's actually played and how it's geared," **poe.ninja/builds** beats any authored list.
For *mechanics/values*, the **wiki + live tools** beat any guide. Authored guides (Maxroll/Mobalytics/
poe-vault) are quality but patch-dated. Currency-seller aggregators (odealo) are broad but lowest-trust —
verify specifics before relying on them. Always check each resource's stated patch/league before trusting it.

---

## Aggregators / index resources

| Resource | URL | Organized by | Best for | Freshness / trust notes |
|---|---|---|---|---|
| **poe.ninja — Builds** | https://poe.ninja/builds | Empirical ladder data; filter by skill, ascendancy, unique, keystone, item | **Meta discovery from real characters** — what's actually played this league, real gear/tree/links, popularity & level distribution | **Highest-value discovery source** — live ladder data, not opinion. Per-league; pick the current league. First stop for "is archetype X popular / how do people gear it." |
| **Maxroll — PoE Build Guides** | https://maxroll.gg/poe/build-guides | Filterable: skill, class, tags (league-start, boss, mapping, budget) | High-quality authored guides with **native planners** + tiered progression (e.g. "2/4 Stone → Endgame") | Well-maintained, current-patch. **No pobb.in code** — planners export to PoB via their button (note when digesting). Strong tag filters → good for mechanic/role discovery. |
| **Mobalytics — PoE Builds** | https://mobalytics.gg/poe/builds | Filterable by skill/class/role; multi-tab variant PoBs | Authored guides with **single shared pobb.in** + many variant tabs (starter→uber), creator-driven (e.g. Fubgun) | Current-patch. One PoB code per guide (loadable directly — convenient for sims). Variant tabs = milestone ladder. |
| **PoE Vault — Guides** | https://www.poe-vault.com/guides | Class/skill; author-driven | Single-author deep dives (often niche/off-meta archetypes the big sites skip) | Variable update cadence per author; **single-author = low corroboration** (cross-check before committing — see `character_data/guides/holy-relic-necromancer/` as an example). |
| **Odealo — Complete Build List** | https://odealo.com/articles/path-of-exile-build-guides-complete-list | Class → skill gem; star badges (Budget / Boss DPS / AoE / Defense) | Broad **breadth** scan: ~70 active + ~150 archival builds in one place; quick budget/clear/boss read via badges | "Last Update **Apr 20 2026, Patch 3.28**" (current as of bookmark 2026-06-27). All guides **self-hosted** (no Maxroll/Mobalytics links). Currency-seller → **lowest trust**; class-first layout, **no mechanic filter**. Good for "what exists," not ground truth. |
| **r/PathOfExileBuilds** | https://www.reddit.com/r/PathOfExileBuilds | Discussion / search by skill | **League-start lists, cutting-edge tech, "is X viable" sanity checks**, post-patch reactions | Most current (community reacts to patch notes fast) but unstructured & unvetted. Best for sentiment + finding the *author* whose guide to then digest. |
| **Official PoE Forum — class build subforums** | https://www.pathofexile.com/forum | Class subforums | Long-form author threads, theorycraft, league-start guide megathreads | Cadence varies; older threads linger. Search by skill + sort by date. |

---

## How this maps to the workflow

1. **Discover** here (start with poe.ninja/builds for meta truth; odealo/Maxroll/Mobalytics for authored options).
2. **Pick** a candidate guide (URL with a pobb.in code or planner).
3. **Digest** it into `character_data/guides/{archetype}/` — `README.md` + `{author}_{league}_{id}.json` +
   (if comparing) `synthesis.md`, via the sub-agent pattern. Register the archetype in
   `character_data/guides/README.md`.
4. **Verify** mechanics/values against live tools + `reference_data/freshness_index.md` (model-aware) before
   asserting how anything works — guides are patch-dated secondary sources.

> Add a row when a new aggregator/index resource proves useful. Keep per-build guide entries in their
> `character_data/guides/{archetype}/` folders, not here — this file indexes *where to find* guides, not the
> guides themselves.
