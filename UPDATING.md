# UPDATING.md — Data-dependency & refresh map

The suite's data comes from several **independent upstreams** that update on different cadences and gate
each other in specific ways. This maps each **update trigger → what to refresh, how, and what it does (and
does not) cascade into.** The `SessionStart` hook *detects* most of these triggers; this doc says what to
*do* when one fires. Companion: [`INSTALL.md`](INSTALL.md) (first-time setup), `reference_data/README.md`
(per-dataset format/staleness), `playbooks/league-transition.md` (the league-roll checklist).

## The upstreams (who feeds what)

```
GGG client patch / league launch ─┬─> GGG skilltree-export ──> reference_data/skilltree   (terminal)
                                   ├─> GGG atlastree-export ──> reference_data/atlastree   (terminal)
                                   ├─> GGG patch notes ───────> patch_notes_index / mechanics_index / freshness_index
                                   ├─> poe.ninja/trade prices > _watchlist.md, character price snapshots  (never cached long)
                                   ├─> poewiki (lags days) ───> eldritch_implicits/, leagues/{league}.md, shrines.md
                                   └─> craftofexile ─────────> reference_data/craftofexile/

PoB Community release ─────────────> PathOfBuilding submodule ──> reference_data/text_lake/  (regen)
                                                              └──> PoB app install (TCP) + optional npm tools release
```

Key non-obvious fact: **the text lake is generated from the PoB submodule ONLY.** Nothing else regenerates it —
not the tree exports, not the client patch. Conversely, the tree exports feed nothing downstream.

---

## Trigger → action

### 1. New PoE league / game client patch (e.g. 3.28 → 3.29)
The big cascade. Roughly in availability order (they don't all land at once):

| Refresh | How | Gate / timing |
|---|---|---|
| **GGG tree exports** (`skilltree`, `atlastree`) | in each submodule: `git fetch upstream --tags && git merge <ver>` → **push fork** → advance suite pointer → commit/push suite | GGG tags usually available **~launch** (ahead of PoB). Clean merges of the `X.Y.0` tag. |
| **Patch notes / mechanics / freshness** | update `patch_notes_index.md` (thread links), `mechanics_index.md` (scope tags: core/league/removed/nerfed), `freshness_index.md` (per-model cutoffs, current-league callout) | GGG posts at launch; cross-check the official thread. |
| **Prices reset** | run the **`league-transition`** skill → flip `.mcp.json` `POE_LEAGUE`, invalidate ninja caches, re-baseline `_watchlist.md`, fix character `meta.json` league fields | at launch, once `get_active_leagues` shows the new league live |
| **Wiki caches** | re-fetch `eldritch_implicits/`, generate `leagues/{league}.md`, refresh `shrines.md` | **poewiki lags days** — don't expect it at launch |
| **craftofexile cache** | refresh `reference_data/craftofexile/` | on craftofexile's own patch timeline |

### 2. PoB Community release (new PoB version, e.g. v2.66 / 3.29)
| Refresh | How | Note |
|---|---|---|
| **PoB submodule** | in `PathOfBuilding/`: merge `upstream` tag/dev → **push fork FIRST** → advance suite pointer | branch is `api-stdio`; push-order guarded by `.githooks/pre-push` |
| **Text lake** | `python scripts/generate_text_lake.py` → re-stamp `MANIFEST.md` patch (~90s) | **its ONLY trigger.** Local-only output — never commit (`legal_considerations.md`) |
| **PoB app install** | relaunch via `pob-mcp/LaunchPoBWithAPI.bat` (re-patches `Main.lua` for TCP); dismiss the integrity warning | separate from the submodule; needed for live TCP |
| **npm / tools release** (optional) | publish the `pob-mcp` / `poe-*` packages | the "full tools release" — do once PoB 3.29 support is in |

### 3. GGG tree export update, standalone (no league — a mid-patch export tweak)
- Refresh the affected submodule(s) as in #1. **Terminal — nothing downstream regenerates** (the text lake is
  from PoB; `get_tree_node` reads live PoB). These exports are offline/authoritative reference + insurance.

### 4. Hotfix / point release (e.g. 3.29.0b, PoB 2.66.1)
- **GGG tree hotfix:** re-check the export upstream for a new `X.Y.Zx` tag; merge if present.
- **PoB hotfix:** re-sync the PoB submodule → **regenerate the text lake**.
- **Balance in the hotfix:** bump `mechanics_index.md` / `freshness_index.md` stamps for what changed.

---

## What does NOT cascade (common confusion)
- **Refreshing `skilltree`/`atlastree` does NOT require a text-lake regen** — different source (the text lake is
  PoB-derived). *(This question came up 2026-07-24; hence this doc.)*
- **A game client patch does NOT let us regenerate anything ourselves** — there is **no `Bundles2` extractor** in
  the suite. We wait on the upstreams (GGG exports, PoB, poewiki) to publish; having the client only confirms
  they're about to.
- **Prices are never a "cache to refresh" on a schedule** — they reset at the league roll and drift hourly; treat
  poe.ninja/trade as live-only (`league-transition` invalidates, doesn't archive).

## Push-ordering rule (submodules)
Always **push the sub-repo first, then advance the suite pointer** (`git -C <submodule> push` → `git add <path>
&& commit && push` in the suite). Pushing the suite pointer before the submodule commit exists on its fork
leaves `origin/main` referencing an unfetchable commit. The tracked `.githooks/pre-push` hook guards this
(enable once per clone: `git config core.hooksPath .githooks`). Submodule branches differ: `PathOfBuilding` =
`api-stdio`, `poe-data-mcp` = `main`, `poe-trade-mcp` = `master`, tree exports = `master`.
