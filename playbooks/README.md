# Playbooks

Task workflow definitions for recurring Claude-driven work in `poe_mcp_suite`. Each playbook is a self-contained markdown file that scopes a task, lists the data sources to load, defines the analysis pattern, and captures lessons learned from prior sessions.

Claude loads the matching playbook at the start of a recognizable task. This prevents context-wasteful broad sweeps, surfaces past mistakes before they get repeated, and keeps task outputs in a consistent shape.

---

## Format conventions

Every playbook should have these sections, in this order:

1. **Step 0 — Frame the work for the user**
   One sentence telling the user which playbook is loaded and why. Then narration norms specific to this task type. Reference `CLAUDE.md` → "Notes for Claude" → narration bullet for the general norm.

2. **Step 1 — Triage (structured)**
   3-5 questions delivered via `AskUserQuestion`, used to scope the analysis. Each question must explicitly gate data loads or analysis paths in later steps — if a question doesn't change what gets loaded, drop it. Note any answers that can be auto-derived (e.g., budget from stash) so Claude reads first and only asks if the read fails.

3. **Step 2 — Data loads**
   Matrix of data sources, organized as:
   - **Always load** (regardless of triage answers)
   - **Add if Q1 = X** / **Add if Q2 = Y** (conditional loads)

   Use precise tool names (`mcp__pob__lua_get_tree`, `mcp__poemcp__fetch_wiki_page`, etc.) and `reference_data/` paths. Saying "use the wiki" without naming the tool is too vague.

4. **Step 3 — Analysis pattern**
   The actual work, in order. Usually: identify bottlenecks → generate candidate fixes → estimate cost and impact → prioritize → phase-order.

5. **Step 4 — Output shape**
   Where the result goes (typically appended to `character_analyses/{League}-{Character}.md`) and what structure it takes. Reference existing examples when possible.

6. **Step 5 — Pitfalls**
   Concrete lessons from prior sessions. Group by category. Each entry should be a specific assertion ("Diamond Shrine does NOT grant ailment immunity," not "be careful with shrines"). This section is the highest-value part of the playbook over time — it preserves expensive lessons that future Claudes would otherwise re-learn.

7. **Trust hierarchy** (optional, at the end)
   When the playbook relies on multiple sources, restate the ordering. Mirror `reference_data/README.md` to keep it consistent.

---

## Contributing a playbook

If a recurring task in your own Claude sessions doesn't have a playbook yet — or an existing one is missing a pitfall you discovered — please consider opening a pull request:

1. **Fork** [poe_mcp_suite](https://github.com/charleslucas/poe_mcp_suite) on GitHub
2. **Draft the playbook** in `playbooks/your-task-name.md`. Use [`dps-analysis.md`](dps-analysis.md) as the reference example
3. **Test it** in at least one real session — playbooks that haven't been used tend to have wrong assumptions about what data is actually needed
4. **Open a PR** with a brief description: what task shape it covers, what triage questions it asks, and the most important pitfall it captures

Maintainer notes when reviewing PRs:
- Playbooks should solve a *recurring* task shape, not a one-off question
- Triage questions must visibly affect Step 2 data loads — otherwise they're noise
- Pitfalls must be specific and falsifiable (a future Claude can verify or refute them against the current league)
- Avoid duplicating content from `reference_data/`; link to it instead

---

## Current playbooks

| Playbook | Covers | Status |
|---|---|---|
| [`dps-analysis.md`](dps-analysis.md) | Damage upgrade analysis: gear, tree, gems | Stable |
| [`verify-install.md`](verify-install.md) | Post-install / post-pull health check across all four MCP servers | Stable |
| [`atlas-planning.md`](atlas-planning.md) | Atlas node allocation, map mod blacklist, mechanic × build synergy, best map layouts | Stable |
| [`build-comparison.md`](build-comparison.md) | Compare two builds from pobb.in/poedb.tw URLs or local files — tree diff, item diff, targeted PoB simulation | Stub |
| [`gear-shopping.md`](gear-shopping.md) | Trade site workflows, resistance/attribute math, stash scanning, price-check pitfalls | Stable |

---

## Wishlist (playbooks worth writing)

- **crafting-decisions.md** — Eldritch implicit choices, bench crafting, corruption gambling expected value.
- **defense-audit.md** — EHP analysis, recovery sources, ailment immunity coverage, layered defenses.
- **league-start-character-pick.md** — Annual workflow leaning on guides + class meta + early-league economy.

If you write one of these (or anything else useful), please PR it back.
