# Template: Build Guide + Progression Checklist

**What this is:** the section registry and copy-paste skeletons for a character's two core docs —
**`build.md`** (the living build guide: read once per league, updated as the build evolves) and
**`progression.md`** (the campaign checklist: followed *while playing*). Produced by
[`character-leveling.md`](character-leveling.md) §3e; the living-guide variant for guideless builds is
[`snapshot-driven-build-guide.md`](snapshot-driven-build-guide.md).

**Why two docs, not one:** they're read at different times, in different postures. `build.md` answers
*"what am I building and why"*; `progression.md` answers *"what do I do next, and am I on track?"*
Merging them forces you to bounce between an act block and the table that judges it — the exact
failure mode the pre-2026-07-29 single-doc format had.

---

## 1. The no-filler rule

**A section exists only when it carries real, non-obvious, character-specific information.** An empty
or restated-from-elsewhere section is worse than no section: it costs scan time and rots.

Before writing any section, ask: *would omitting this lose information the reader can't get faster
elsewhere?* If no → omit. Specifically:

- **Don't restate the source guide** — link it. Our docs carry the *delta* and the *decisions*.
- **State each fact once.** Ascendancy order lives in `build.md` only; `progression.md` references it
  at the act where it's taken (`★ Asc #1 → build.md#ascendancy`). Same for the fork, tree phases,
  pantheon.
- **No placeholder rows.** `_(add when known)_` is acceptable **only** in a table that already has
  real rows and a live reason to expect more (e.g. a partly-verified quest-reward table).
- **Omit whole sections freely.** Most builds have no fork, no variant gear tables, no patch delta.

## 2. Section registry

`[BUILD]` = build-guide concern · `[CAMPAIGN]` = checklist concern · `[OURS]` = our value-add
(external guides don't do it).

| Section | Doc | Tag | Include when | Omit when |
|---|---|---|---|---|
| Status header | both | `[OURS]` | **always** — the scan anchor | never |
| Concept / Overview | `build.md` | `[BUILD]` | always | never |
| Pros / Cons | `build.md` | `[BUILD]` | there are real tradeoffs to warn about | generic build with no notable downside |
| Playstyle / rotation | `build.md` | `[BUILD]` | the build has a real rotation, ramp, or button discipline | facetank-and-hold-left-click |
| Damage & defence layers | `build.md` | `[BUILD]` | scaling or defence is non-standard (poison ramp, block-not-leech, minion-carried) | conventional life+res+one damage stat |
| PoB links (per budget tier) | `build.md` | `[BUILD]` | tiers differ meaningfully | one link covers it → single line, no table |
| Gear | `build.md` | `[BUILD]` | always (table) | never |
| Gear progression (cheap→chase) | `build.md`/sub-doc | `[BUILD]` | acquisition order matters and isn't obvious from the gear table | short gear list, no chase items |
| Watchlist + buy-triggers | `build.md` | `[OURS]` | there are items to wait for at a price | nothing gated on the market |
| Ascendancy / Bandits / Pantheon | `build.md` | `[BUILD]` | always — **once**, here | never |
| Passive tree phases | `build.md` | `[BUILD]` | always | never |
| Tree caveats (cluster-jewel, skip-list) | `build.md` | `[OURS]` | the plan names notables that are cluster-only, or points people waste | nothing to warn about |
| Endgame fork + swap-insurance | `build.md` | `[OURS]` | the build genuinely branches on an external condition (usually price) | single-path build → **omit entirely** |
| Patch delta ("New in {patch}") | `build.md` | `[OURS]` | a patch actually changed something for *this* build | nothing changed → omit |
| Gap analysis vs source guide | `build.md` | `[OURS]` | a source guide exists | pure theorycraft (nothing to diff) |
| Open questions | `build.md` | `[OURS]` | non-empty | empty → delete the heading |
| Per-act blocks | `progression.md` | `[CAMPAIGN]` | always | never |
| Tagged essentials line | `progression.md` | `[CAMPAIGN]` | always — the #1 usability feature | never |
| Per-act checkpoint row | `progression.md` | `[OURS]` | always — inline, *with* the act | never (don't move it to a distant table) |
| Zone-by-zone walkthrough | sub-doc | `[CAMPAIGN]` | **no** good external walkthrough covers this build's route | the guide already links one → link it instead (§5) |
| Progression log | `progression.md` | `[OURS]` | always — the reality record | never |
| Quest-gem timing anchors | `progression.md` | `[OURS]` | acquisition timing is non-trivial (usually) | all gems trivially available |

## 3. Layout conventions

Borrowed **patterns** (not assets) from poe-vault/Maxroll: scannable tagged quest lines, callout
boxes, tier badges, hub-and-sub-page cross-linking.

**Fixed badge set — use only these, and only with these meanings:**

| Badge | Means |
|---|---|
| `★` | ascendancy point taken here |
| `◆` | a decision the player must make |
| `⏳` | gated — not available until this point |
| `⚠` | correctness warning / easy mistake |
| `✅` | verified in-game |
| `✓` | checkpoint / tolerance row |

Nothing else. Emoji density was a real complaint about the old format — a small fixed vocabulary
scans; free-form decoration doesn't.

**Quest reward tagging** (the single biggest usability win — Maxroll's idea). In each act's essentials
line, tag every reward-bearing quest inline so it can be *scanned*:

```
· Breaking Some Eggs (Gem: SRS, Frostblink)   · Deal with the Bandits (◆ Bandit)
· The Caged Brute (Gem: supports)             · Trial of Ascendancy ×N (⏳ Lab)
· Lost in Love (Passive Point)                · A Fixture of Fate (⏳ Siosa: most gems)
```

**Budget tiers:** `[LS]` league-start · `[MID]` mid-budget · `[MAX]` min-max. Use as row prefixes in
gear/PoB tables; don't create three separate tables.

**Callout box** for anything that silently ruins a run:

```
> ⚠ **Kitava (end of Act 5 and Act 10):** each applies **−30% to all resistances**. Re-cap after both.
```

## 4. Skeleton A — `build.md`

Hub doc. Sub-doc anything that outgrows ~1 screen or is pure reference (§5).

```markdown
# {Character} — {Build name}
**Class:** {class} / {ascendancy} · **Main skill:** {skill} · **League:** {league}
**Source guide:** [{author} — {title}]({url}) · **Archetype library:** `guides/{archetype}/`
**Status:** L{n} · {act/maps} · {life}/{ehp} EHP · res {f}/{c}/{l} · latest snapshot `{file}`

## Concept
{2-4 sentences: what carries damage, what keeps you alive, why this build.}

## Pros / Cons
**Pros:** {…}
**Cons:** {…}

## Playstyle
{The actual button discipline: what you press, what ramps, what re-summons, what to avoid.}

## Damage & defence layers
| Layer | How it works | Notes |
|---|---|---|

## PoB
| Tier | Link | Notes |
|---|---|---|
| [LS] | {pobb.in} | {…} |

## Gear
| Slot | Item / base | Key stats | Tier |
|---|---|---|---|

### Watchlist — buy when the price is right
| Priority | Item | Why / when | Buy-trigger |
|---|---|---|---|
{Cross-ref the shared `_watchlist.md` rather than duplicating cross-league entries.}

## Ascendancy · Bandits · Pantheon
**Ascendancy order:** {1 → 2 → 3 → 4} — {source}
**Bandit:** {choice} · **Pantheon:** major {…} / minor {…}
{State once. progression.md points here.}

## Passive tree
**Phase 1 (Acts 1-2):** {notables} · **Phase 2 (Acts 3-5):** {…} · **Phase 3 (6-10→maps):** {…}
⚠ {cluster-jewel-only notables; skip-list; masteries that matter}

## Endgame fork          ← omit unless the build really branches
**Decider:** {condition, usually a price} · **Swap insurance:** {how you avoid bricking}

## New in {patch}        ← omit unless something changed
## Gap analysis vs the source guide
## Open questions        ← omit when empty
```

## 5. Skeleton B — `progression.md`

Campaign checklist. **Act = the spine**, with judgment co-located per act.

```markdown
# {Character} — campaign progression
**Build detail:** [`build.md`](build.md) · **Log:** [`journal.md`](journal.md)
**Status:** L{n} · {act} · next: {the single next action}

> How to use: drift is expected and free. This is a corridor, not a script — when reality diverges,
> either track back or amend the plan (see the log for what actually happened).

## Always-on
{Only rules that apply in EVERY act — e.g. re-summon cadence, res-before-Kitava, snapshot cadence.
3-6 lines max. If it's act-specific it belongs in that act.}

## ACT {N} — lvl {a}-{b}
**Essentials:** · {Quest} ({tag}) · {Quest} ({tag}) …
**Links:** {gem setup at this point}
**Items:** {what to equip/craft/buy here} · {⏳ gated items}
**{★/◆}** {ascendancy taken here → build.md#ascendancy · decisions}
`✓` res {n}+ · life {n}+ · {main-link state}

{repeat per act — omit any line with nothing real in it}

## Progression log
| Date | Lvl · Act | Snapshot | Life / res | Notes vs plan |
|---|---|---|---|---|
```

**Zone-by-zone walkthrough — conditional.** Do **not** write one when the source guide already links a
good campaign walkthrough (e.g. BalorMage → poe-vault's quick-reference leveling guide): link it from
`progression.md`'s header and stop. Write `campaign-walkthrough.md` **only** when no external
walkthrough covers the route, using per-zone metadata blocks:

```markdown
### {Zone}
**Waypoint:** yes/no · **Boss:** {…} · **Quests:** {Quest} ({tag})
{layout/mechanic notes only if non-obvious}
```

## 6. Maintenance

- **Plan docs hold current state, not history.** Update in place; "was X, now Y" goes in
  `journal.md`. (Standing user preference.)
- **Stamp freshness** on anything patch-dependent (`patch:` / `league:` / `fetched:`); re-verify
  against [`reference_data/freshness_index.md`](../reference_data/freshness_index.md) before
  asserting a mechanic.
- **Quest-gem timing** comes from
  [`reference_data/quest_gem_rewards.md`](../reference_data/quest_gem_rewards.md) — quest-gated, not
  level-gated. Vendor recipes:
  [`reference_data/vendor_recipes.md`](../reference_data/vendor_recipes.md). Feed newly *verified*
  in-game timings back to those files.
- **At league end,** fold durable, reusable lessons into `guides/{archetype}/` so the next character
  inherits them; character-specific detail stays in `character_data/`.
- ⚠ **Relative-link depth.** From `character_data/{account}/{league}/{char}/`, repo-root targets
  (`reference_data/`, `playbooks/`) need **four** levels — `../../../../reference_data/x.md` — while
  `guides/` lives *inside* `character_data` and needs **three**: `../../../guides/x.md`. Getting this
  wrong is silent (VSCode just shows a dead link). Also note `character_data/` is a **directory
  junction**, so a shell that resolves paths physically (git-bash `cd`) will report repo-root links
  broken even when they render fine — verify lexically from the repo path, not from inside the junction.
