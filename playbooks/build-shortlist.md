# Playbook: Build Shortlist (N-way comparison / bake-off)

For choosing among **N candidate builds** (3+) — e.g. "import these six minion builds and
tell me which to build a character around." Produces a durable decision doc in
`character_data/guides/_comparisons/{topic}.md`, with every unit of per-candidate
understanding banked permanently in that candidate's `guides/{archetype}/` dir. Nothing
researched here is throwaway.

For exactly **two** builds, use [`build-comparison.md`](build-comparison.md) directly — this
playbook *invokes* it for its finals. For designing the winner into a character, hand off to
[`build-design.md`](build-design.md).

Read [`README.md`](README.md) first (cursory gate, pre-flight, context management, narration
norms). **Model routing:** cross-build judgement is meta-knowledge-heavy — Opus-class, like
guide synthesis (note it inline and proceed).

---

## Shape: a seeded tournament, not N² comparisons

A group comparison ultimately reduces to a series of pairwise calls ("best of these two, then
that one vs the next…"). But a full `build-comparison` per pair is expensive, so structure it:

1. **Group stage (cheap):** normalize all N candidates onto the same axes from digests —
   no PoB loads. Prune candidates that lose on a *hard constraint* or are dominated.
2. **Finals (expensive):** run the king-of-the-hill pairwise chain — with tier-matched PoB
   sims via `build-comparison` — only on the 2–3 survivors where the call is contested.

Elimination order matters less when the group stage prunes on hard constraints first;
document *why* each candidate was eliminated (that rationale is reusable knowledge).

---

## Stage 0 — Value-function triage (before ANY data is pulled)

"Best" is undefined until the user defines it. A DPS-best list, a playability-best list, and
a defence-best list are **different rankings of the same candidates**. Ask pointed questions:

1. **What does "best" mean here — in priority order?** Offer the axis menu and get a ranked
   pick (typically 2–3 primary axes + a tiebreaker):
   - DPS at matched gear tiers (league-start / mid / aspirational)
   - Clear speed / mapping feel
   - Defence / tankiness (EHP, layers, recovery)
   - Leveling smoothness & when the build "comes online"
   - Budget curve (cost to start, cost to scale, gearing/socket difficulty)
   - Playstyle fit (buttons per pack, one-button vs piano, minion babysitting, projected fun)
   - League/patch robustness (nerf exposure, mechanic dependence)
2. **Hard constraints** (instant elimination, no scoring): budget ceiling, HC/SC, league-start
   day-1 viability required?, skills/archetypes the user refuses to play.
3. **The standing lean + overturn test:** does the user already favour one? If so, frame the
   comparison as *"what evidence would change that lean?"* — it sharpens which axes actually
   need numbers. (The 3.29 league-start comparison was exactly this: clear speed and
   DPS-at-level were the potential lean-changers; playstyle was the standing tiebreaker.)
4. **Topic name** for the decision doc: `_comparisons/{topic}.md` (e.g. `minion-builds-3.30.md`).

**Pause and state the plan** (roster, ranked axes, elimination criteria, expected depth per
stage). Wait for approval.

---

## Stage 1 — Roster normalization (bank the per-candidate effort)

For each candidate, in the guide library — creating `guides/{archetype}/` dirs as needed:

- **Minimum depth: quick entry** (per [`guide-analysis.md`](guide-analysis.md)): the JSON
  entry (author/league/tier/links/key uniques/stored stats) + archetype README skeleton.
- **Digest without loading PoB:** `mcp__poe-data-mcp__parse_pob` (stats, items, tree
  summary) and `mcp__poe-data-mcp__parse_pob_skill_groups` (link groups, socket/colour
  requirements — feeds the "gearing difficulty" axis; full method:
  [`gem-socket-analysis.md`](gem-socket-analysis.md) shared-build variant).
- **Deepen only where an axis demands it** — if "leveling smoothness" is a ranked axis, the
  guide's leveling section needs reading; if not, skip it. Every deepening lands in the
  archetype dir (README notes, synthesis.md), never only in the comparison doc.

Freshness pre-flight per candidate (guide's league vs current patch; `freshness-check` on
core mechanics) — a candidate built on a nerfed mechanic is a Stage-2 elimination with cause.

---

## Stage 2 — Group stage: matrix + prune

Build the matrix (candidates × ranked axes) from Stage-1 digests:

- Fill **numeric axes** from stored/parsed stats — clearly tagged with gear tier and config.
- Fill **mechanical axes** (clear feel, leveling timing, playstyle) from digest notes — these
  are judgement calls; say so.
- **Eliminate**: hard-constraint failures first, then dominated candidates (worse or equal on
  every ranked axis than some survivor). Record each elimination + one-line cause in the
  decision doc.

Target: 2–3 finalists. If one candidate dominates everything, you're done — write it up.

---

## Stage 3 — Finals: pairwise king-of-the-hill (tier-matched sims)

Run the user's tree-search: champion vs challenger, winner stays, next challenger. Each
pairing uses [`build-comparison.md`](build-comparison.md) scoped to the **contested axes
only** (the ranked axes where the group stage couldn't separate them). Sim rules learned
from the 3.29 comparison (all real failure modes):

- **Tier-match configs** — league-start cfg vs league-start cfg, aspirational vs
  aspirational. Never cross tiers.
- **Character level barely moves DPS** — gear/gem tier is the lever; matching level without
  matching gear tier is a false control.
- **FullDPS vs CombinedDPS isn't perfectly 1:1** across archetypes (DoT-ramp vs
  front-loaded hit); note the damage-delivery caveat next to any close call.
- **PoB under-reports some archetypes** (e.g. trigger/breakpoint minions) — carry the
  candidate's known under/over-reporting flags from its build-profile into the verdict.
- **Equalize what you can't fill** (e.g. leave jewels empty on BOTH) so the axis is fair.
- **Never load two builds into PoB at once** — digest-diff first; load only the one being
  simmed (build-comparison's rule).
- **Ceiling vs timing:** ~par DPS at matched tiers can hide a big difference in *when* the
  build works (leveling dead zones, swap points). Report both.

---

## Stage 4 — Decision doc + banking

Write `character_data/guides/_comparisons/{topic}.md` (format:
`character_data/guides/README.md` → "Cross-archetype comparisons"): candidates (links to
archetype dirs), ranked axes + hard constraints (the Stage-0 value function, verbatim),
matrix, eliminations with cause, finals verdicts with sim numbers, **decision + rationale +
what would overturn it**, and **re-verify triggers** (patch risks per candidate).

Then: one-line pointer in each involved archetype README; add the comparison to the root
guides README index; per-candidate learnings discovered during finals go in the candidate's
own dir (synthesis.md / README), not just the comparison doc.

---

## Stage 5 — Handoff

- **Winner** → [`build-design.md`](build-design.md) (adopt/adapt decision, build-profile +
  build-plan in its archetype dir) when the user is ready to commit.
- **Runners-up keep their banked analyses** — a future comparison (new league, new topic)
  starts from their existing dirs at near-zero cost. That accretion is the point.
- The comparison doc is **living**: a new candidate joins by running Stages 1–3 against the
  standing champion; a patch triggers the re-verify list.

---

## Pitfalls

| Pitfall | Reality |
|---|---|
| Comparing before defining "best" | The ranking is undefined without the user's prioritized axes — Stage 0 is mandatory |
| Full build-comparison for every pair | N² deep dives; prune on cheap digests first, sim only contested finals |
| Comparison findings living only in the decision doc | Per-candidate insight belongs in that candidate's archetype dir — the doc holds only cross-candidate material |
| Cross-tier sims ("their endgame vs our starter") | Tier-match configs or the numbers are meaningless |
| Trusting DPS-at-par as "equivalent builds" | Timing (when it comes online) and clear feel are separate, often decisive axes |
| Treating eliminations as waste | Documented eliminations + banked quick entries are the durable output for future picks |
