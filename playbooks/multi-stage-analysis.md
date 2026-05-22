# Playbook: Multi-Stage Analysis

For analyses too large to fit in a single context window. Instead of trying to hold all data at once, work in stages: each stage loads a specific slice of data, extracts the findings that matter, writes them to a checkpoint file, then releases the raw data before the next stage.

The checkpoint file is the thread that connects stages across context resets. Raw data is temporary; distilled findings are permanent.

**Triggers:** "comprehensive analysis", "full character review", "optimize everything", or any task where you can enumerate more than 4-5 distinct data sources needed. Check context before starting — if already at 40%+, start with a fresh `/compact` first.

---

## The Core Pattern

```
for each stage:
  1. read checkpoint (know where we are + what we've found so far)
  2. call get_context_usage (know how much headroom we have)
  3. load only the data for THIS stage
  4. analyze
  5. write findings to checkpoint
  6. report stage result to user
  7. if approaching 70%: flush and recommend /compact before next stage
  8. proceed to next stage (or stop if context too full)
```

Key insight: **only the findings survive between stages, not the raw data.** A 60-page passive tree node list collapses to "these 8 nodes look suboptimal, here's why." The next stage reads those 8 lines, not the 60 pages.

---

## Checkpoint File Format

Write to `character_data/{account}/{char}/buffer/analysis_{YYYY-MM-DD}_{type}.json`. The buffer/ dir is for temporary session files — safe to delete after the analysis is complete and findings are in journal.md.

```json
{
  "analysis_type": "character_improvement",
  "character": "Memophage_4428/MirageSixFingeredMan",
  "started": "YYYY-MM-DD",
  "stages": [
    {
      "name": "tree_validation",
      "status": "complete",
      "findings": "Nodes X, Y, Z look suboptimal: X because [...], Y because [...]. Nodes A-F are well-chosen and should not be changed."
    },
    {
      "name": "item_mod_analysis",
      "status": "in_progress",
      "findings": ""
    },
    {
      "name": "nearby_nodes",
      "status": "pending"
    },
    {
      "name": "synthesis",
      "status": "pending"
    }
  ],
  "context_snapshots": [
    {"after_stage": "tree_validation", "tokens": 145000, "pct": 72}
  ],
  "final_recommendations": ""
}
```

**Status values:** `pending` · `in_progress` · `complete` · `skipped` (if context ran out)

---

## Stage Protocol

### At the start of every stage

```
1. Read checkpoint file (cheap — JSON, a few KB)
2. Call mcp__pob__get_context_usage
3. If pct >= 80%:
   - Write findings so far to checkpoint
   - Tell the user: "Context is at X%. I'll stop here and recommend /compact.
     When you restart, I'll read the checkpoint and continue from stage N."
   - STOP. Do not load more data.
4. If pct >= 60%:
   - Load minimal version of stage data (summaries not raw, cached not live)
   - Note in checkpoint that this stage was done with reduced data
5. If pct < 60%: proceed normally
```

### After each stage completes

```
1. Distill findings to 3-10 bullet points (not raw data, not full analysis — just conclusions)
2. Write findings to checkpoint["stages"][N]["findings"]
3. Update checkpoint["stages"][N]["status"] = "complete"
4. Record token snapshot in checkpoint["context_snapshots"]
5. Report to user: what was found, what's next, current context level
6. Ask if they want to continue or compact first
```

### Resume after /compact

At the start of the resumed session:
```
1. User says "continue the analysis" (or similar)
2. Read the checkpoint file from buffer/
3. Find the first stage with status != "complete"
4. Summarize completed stages to user: "Last session completed: tree_validation, item_mod_analysis. Findings: [...]"
5. Continue from the in_progress or first pending stage
```

---

## Canonical Example: Character Improvement Analysis

### Stage definitions

| # | Stage | Data loaded | Output |
|---|---|---|---|
| 1 | **Tree validation** | `meta.json` + `lua_get_tree` (node IDs) + `atlastree/league.json` (node descriptions) | Which nodes look suboptimal and why |
| 2 | **Item + mod review** | `inventory.json` + `lua_get_stats` (defense) + poedb wiki for each unique | Which item mods are load-bearing, which are replaceable |
| 3 | **Tree–item cross-reference** | Findings from stages 1–2 (from checkpoint, ~1-2K tokens) | Interactions between current nodes and items; which node choices are forced by gear |
| 4 | **Nearby node alternatives** | `search_tree_nodes` or atlastree lookup for nodes adjacent to "suboptimal" ones from stage 1 | Better alternatives within ~3 nodes of current path |
| 5 | **Category-node comparison** | `search_tree_nodes` by stat type for each "category" identified (e.g., "mana nodes", "block nodes") | Whether the character is on the best nodes of that type available |
| 6 | **Synthesis** | Findings from all stages (checkpoint, ~5-10K tokens total) | Ranked upgrade list: quick wins, medium effort, expensive/aspirational |

### What collapses at each stage

- Stage 1: 200-node tree → 5-10 flagged suboptimal nodes + 3-line justification each
- Stage 2: 10 equipped items × many mods → "load-bearing mods: X, Y, Z; replaceable: A, B"
- Stage 3: no new raw data — just cross-referencing 2 checkpoint entries
- Stage 4: 50-node neighbourhood → 3-5 better alternatives with node IDs and stat lines
- Stage 5: same — cross-referencing
- Stage 6: combines all 5 checkpoint entries into a ranked list (~1-2 pages)

Stages 3, 5, and 6 are **synthesis-only** — they load no raw data, only checkpoint findings. This means they can run even when context is tight.

---

## Context Management During Stages

### Token cost estimates per stage

| Stage | Raw data loaded | Approx tokens consumed |
|---|---|---|
| 1 (tree) | node IDs + atlastree descriptions | 5-8K |
| 2 (items) | inventory.json + 3-4 wiki pages | 6-10K |
| 3 (cross-ref) | checkpoint only | <1K |
| 4 (nearby) | search_tree_nodes results | 3-5K |
| 5 (categories) | search_tree_nodes results | 3-5K |
| 6 (synthesis) | checkpoint only | <2K |

**Total if all stages run in one session:** 18-31K tokens of new data. Feasible if starting below 40%.
**If starting at 50%+:** plan for a context reset after stage 2 (before the heaviest cross-referencing). Stages 3, 5, 6 can always run fresh after /compact since they load no raw data.

### Recommended breakpoints

- **After stage 2** if context > 65% — stages 3-6 are synthesis-heavy and work fine in a fresh context
- **After stage 4** if context > 75% — stage 6 synthesis runs well on a clean slate

---

## Writing to journal.md at completion

When all stages are done (or when explicitly stopping), append to `character_data/{account}/{char}/journal.md`:

```markdown
## YYYY-MM-DD — Comprehensive Character Analysis ({analysis_type})

Stages completed: [list]
Context snapshots: [list — useful to know if analysis was done in degraded mode]

### Key findings
[distilled from checkpoint, organized by priority]

### Recommended changes
[ranked: quick wins → medium effort → aspirational]
```

Then delete the checkpoint file from buffer/ — the journal is the permanent record.

---

## Pitfalls

- **Don't skip the checkpoint write.** If you load 8KB of tree data, analyze it, and then the user asks a follow-up question that pushes context over 90% before you write the findings — those findings are gone. Write immediately after analysis, before any user interaction that might trigger more data loads.
- **Keep findings distilled, not quoted.** A stage finding should be 3-10 lines, not a copy of the raw data. If you're tempted to write "here's the full list of 50 nearby nodes," write "the 3 best alternatives are X (node 1234), Y (node 5678), Z (node 9012)" instead.
- **Synthesis stages are cheap — do them last.** Stages that only read checkpoint findings cost almost nothing in context. Always run them after a /compact if the analysis ran long, rather than trying to squeeze them in when full.
- **The checkpoint file itself costs tokens.** Keep the JSON lean. Findings should be prose, not nested JSON objects. The whole checkpoint should stay under ~3K tokens for a 6-stage analysis.
- **Label checkpoint files by date.** If an analysis spans multiple days, the date in the filename makes it obvious which checkpoint is active. Always read the latest one.
