# Playbooks — Meta-Analysis Framework & Index

Read this file **before** loading any specific playbook. It defines the execution protocol shared by all playbooks: how to classify a request, how to manage context, when to load league-specific data, and how to narrate the work. Individual playbooks focus on task-specific data loads, analysis patterns, and pitfalls — they do not repeat this framework.

---

## 1. Cursory vs detailed — the gate

Before loading any data, classify the request:

**Cursory** — proceed immediately, no playbook needed:
- Uses only: training data, already-cached character files (`meta.json`, `inventory.json`, `journal.md`), a single pobb.in/poedb.tw XML diff, or a ninja price lookup
- Expected new tokens: <5K; no heavy data fetches; no wiki pages, transcripts, or tree node lookups
- Examples: "what does this item do?", quick price check, which mastery should I pick?

**Detailed** — load this file + matching specific playbook, then wait for user approval before pulling data:
- Will touch: passive tree node descriptions, wiki pages, YouTube transcripts, multiple builds, or multiple data sources in sequence
- Involves: multiple distinct analysis stages, or >10K expected new tokens
- Trigger phrases: "comprehensive analysis", "optimize my build", "compare these guides", "full review", or any request where you can enumerate 4+ distinct data sources needed

When a request is **detailed**, respond before touching any data:
> "This looks like a detailed analysis. Here's what I'd cover and in what order: [stage list with expected data sources]. Want me to proceed, or should we narrow the scope first?"

Only load data once the user confirms. This prevents spending 20K tokens on an analysis the user wanted as a 2-sentence summary.

---

## 2. Pre-flight protocol (every detailed task)

Run these before loading task-specific data. Individual playbooks list the tools to call; this section explains when and why.

### 2a — Context headroom
Call `mcp__pob__get_context_usage` before loading heavy data. The tool reads the last 8KB of the session JSONL — it's fast.

| Usage | Action |
|---|---|
| < 60% | Proceed normally |
| 60–79% | Prefer cached summaries; use compact tool outputs (category-specific stats, not `category='all'`); skip transcripts unless essential |
| 80%+ | Write key findings to `character_data/` before continuing; ask the user to `/compact` before the next heavy stage |

Rough token costs (calibrated from real sessions — see `character_data/analysis_log.md`):

| Source | Approx tokens |
|---|---|
| `meta.json` | ~500 |
| `inventory.json` | ~2–3K |
| `build.md` + `journal.md` combined | ~8–12K |
| YouTube transcript (38K chars) | ~10–12K |
| `reference_data/leagues/{league}.md` | ~4–5K |
| `lua_get_stats` result | ~500–1K |
| `get_tree_node` single-node lookup | ~300–500 tokens — **prefer this over Python BFS** for single-node "what does this give me?" questions |
| `find_jewel_affected_nodes` (full build scan) | ~1–2K — call before assuming any tooltip discrepancy is stale data |
| `list_cluster_jewel_nodes` | ~1–2K — fast structured view of all socketed clusters |
| `evaluate_threshold_jewels` | ~500 tokens — empty result for builds without threshold jewels |
| Python-processed output (tree diff, XML parse) | **only the output** — key efficiency win for bulk topology analysis |

For analyses that won't fit in one session, use the staged checkpoint pattern from [`multi-stage-analysis.md`](multi-stage-analysis.md).

After any multi-stage or context-heavy analysis, append an entry to `character_data/analysis_log.md` with actual vs. estimated token costs. That log is how the table above gets calibrated.

### 2b — League reference
Load `reference_data/leagues/{current-league}.md` at the start of any session involving current-league content. Per-league summaries cover drop tables, unique items, scarab/atlas-node availability, and strategic implications — things that change every 3 months and aren't in Claude's training. The current league name is set in `.mcp.json` as `POE_LEAGUE`.

If the file doesn't exist for the current league, generate it via a sub-agent (see section 6) so the raw wiki page never enters main context. The agent fetches `https://www.poewiki.net/wiki/{LeagueName}_league`, summarizes, writes the cache file, and returns only a brief confirmation. For per-mechanic deep dives during the same session, additional sub-agents per mechanic also work well.

### 2c — Character snapshot
If the task involves a specific character, read `character_data/{Account}/{Character}/meta.json` and `journal.md` before loading any live data. The journal records hard-won decisions (crafting results, build pivots, known pitfalls) that directly affect what to recommend — skipping it leads to re-solving problems already solved.

---

## 3. Narration norms

When starting a recognized task: *"Using the [X] playbook — quick triage first, then I'll pull [data sources]."*

Throughout the session:
- **Before fetching live data:** state the source and why ("Pulling current Eldritch pool from poewiki — the cached version is stale")
- **When caching new data:** say so ("Writing this to `reference_data/X.md` so future sessions don't re-fetch")
- **When data is stale, missing, or suspect:** ask the user. Their in-game observations are always more current than any cache or wiki. Frame it as force multiplication: "Up-to-date local data lets me run faster, more accurate analyses next time."
- **When sources conflict:** name which source you're trusting and why

---

## 4. Model selection

`mcp__pob__get_context_usage` reports the active model ID alongside session state.

| Model | Best for |
|---|---|
| `claude-opus-4-7` | Complex multi-step reasoning, novel build synthesis, difficult cross-analysis |
| `claude-sonnet-4-6` | General analysis, code, most PoE tasks — good default |
| `claude-haiku-4-5` | Fast lookups, price checks, simple queries |

If on Sonnet/Haiku and the task clearly needs deeper reasoning (synthesizing 5+ guide builds into a novel build), mention: *"This would benefit from Opus — you can switch with `/model opus` if you'd like."* Don't switch automatically. Log the model in `analysis_log.md` entries so patterns emerge over time.

---

## 5. Trust hierarchy

When sources conflict:
1. Live in-game observation by the user (item pastes, character API data)
2. GGG official exports (`reference_data/skilltree/`, `reference_data/atlastree/`)
3. Live PoB TCP for the loaded build
4. Live wiki fetch via `mcp__poemcp__fetch_wiki_page`
5. Cached `reference_data/` — check the `fetched:` date in frontmatter before trusting
6. PoB's bundled tree data
7. Claude's training (last resort — often outdated on prices, mod availability, league mechanics)

---

## 6. Sub-agents

When a task can be decomposed into bounded, independent queries, prefer spawning sub-agents over running them in main context. Each sub-agent runs in its own context window — raw inputs and intermediate work never enter mine. I only see the final summary the agent returns.

**Sub-agents earn their cost when:**
- Input or output would be >5K tokens (raw transcripts, wiki pages, full build XMLs)
- Multiple independent queries can run in parallel
- The scope is self-contained: the agent has everything it needs in its prompt

**Sub-agents are wasted when:**
- The lookup is a single tool call (price check, fetch one wiki page for a single fact)
- The work requires back-and-forth iteration (live build tuning, interactive simulation, tree-delta cycles)
- The synthesis can't happen without seeing the raw data (rare — usually the agent can extract enough)

**Decision rule:** if I'd be loading >5K tokens of raw content to extract <1K tokens of insight, delegate. The sub-agent reads the raw; I receive the digest.

**Common patterns (specifics live in the relevant playbooks):**
- One sub-agent per build for `build-comparison.md` (parses XML, returns structured digest)
- One sub-agent per guide for multi-guide synthesis (reads transcript, returns build extraction)
- One sub-agent for league reference cache generation (fetches wiki, writes cache file)

When spawning multiple sub-agents whose queries don't depend on each other, dispatch them in **a single message with parallel tool calls** rather than sequentially. This is the right pattern when (for example) you want to fetch and digest three guides simultaneously — total wall time is one agent's runtime, not three.

---

## 7. Current playbooks

Each domain playbook below has a thin wrapper **skill** in `.claude/skills/<name>/` that auto-triggers on matching detailed-scope requests and points back here — the playbooks remain the single source of truth. `verify-install` is wrapped as a manual `/verify-install` skill (no auto-trigger). The cursory-vs-detailed gate (section 1) stays cross-cutting in `CLAUDE.md`, not in the skills.

| Playbook | Covers | Status |
|---|---|---|
| [`dps-analysis.md`](dps-analysis.md) | Damage upgrade analysis: gear, tree, gems | Stable |
| [`verify-install.md`](verify-install.md) | Post-install / post-pull health check across all four MCP servers | Stable |
| [`atlas-planning.md`](atlas-planning.md) | Atlas node allocation, map mod blacklist, mechanic × build synergy, best map layouts | Stable |
| [`build-comparison.md`](build-comparison.md) | Compare two builds from pobb.in/poedb.tw URLs or local files — sub-agent-first digest, then tree/item/gem diff and targeted PoB simulation | Stable (sub-agent-first; not yet session-validated) |
| [`multi-stage-analysis.md`](multi-stage-analysis.md) | Framework for analyses too large for a single context window — checkpoint files, stage protocol, resume-after-compact | Stable |
| [`gear-shopping.md`](gear-shopping.md) | Trade site workflows, resistance/attribute math, stash scanning, price-check pitfalls | Stable |
| [`character-leveling.md`](character-leveling.md) | Milestone PoB builds (every 20 levels), gear schedule from stash, passive tree planning, Notes tab, progression.md | Stable |
| [`tree-analysis.md`](tree-analysis.md) | Passive tree audit and reallocation: intent triage, node classification, connectivity/chain analysis, jewel socket safety, mastery node topology | Stable |
| [`league-transition.md`](league-transition.md) | End-of-league migration checklist: env var, character `meta.json` updates, new-league cache bootstrap; trigger when `get_active_leagues` shows ⚠ | Stable |
| [`build-optimization-sim.md`](build-optimization-sim.md) | Systematic gem/link/jewel optimization via live PoB sim — snapshot, sim each candidate, restore, rank by DPS-per-div. Full audit surface: support gem choice, gem quality, jewel dead-mod re-rolls, stat layer (reservation, HitChance, overcapped resists) | Stable (session-validated 2026-05-31) |

| [`stash-scanning.md`](stash-scanning.md) | Stash tab pricing and item evaluation. **Currently blocked** — GGG disabled the legacy stash endpoint; OAuth developer registration required for bulk access. Documents `score_rare` (individual items, works today), WealthyExile (recommended for bulk), and OAuth as a last resort. Skill auto-triggers and immediately explains the block. | Stable (blocked) |

**Wishlist** (playbooks worth writing):
- `crafting-decisions.md` — Eldritch implicit choices, bench crafting, corruption gambling expected value
- `defense-audit.md` — EHP analysis, recovery sources, ailment immunity coverage, layered defenses
- `league-start-character-pick.md` — Annual workflow: guides + class meta + early-league economy

---

## 8. Playbook format

Every playbook must have these sections in this order:

1. **Step 0 — Frame the work for the user**
   One sentence naming the playbook and the approach. Add task-specific narration notes (tool calls to announce, what to say when results come back). Do not re-state the general narration norms from section 3 above.

2. **Step 1 — Triage**
   3–5 questions via `AskUserQuestion` that gate data loads in Step 2. Every question must visibly change what gets loaded — if it doesn't, drop it. Auto-derive answers from available context before asking (e.g., read stash for budget before asking for budget).

3. **Step 2 — Data loads**
   Matrix organized as **Always load** / **Add if Q1 = X** / **Add if Q2 = Y**. Use exact tool names and `reference_data/` paths. "Pre-flight" entries (`get_context_usage`, league reference, character snapshot) can be listed here with a short note; the execution rules live in section 2 of this file.

4. **Step 3 — Analysis pattern**
   The actual work in order: identify bottlenecks → candidate fixes → cost/impact estimates → prioritized phases.

5. **Step 4 — Output shape**
   Where results go (typically `character_data/{Account}/{Character}/journal.md` or `build.md`) and what structure they take.

6. **Step 5 — Pitfalls**
   Concrete lessons from real sessions. Each entry must be a specific, falsifiable assertion — "Diamond Shrine does NOT grant ailment immunity" not "be careful with shrines." This section is the highest-value part of the playbook over time.

7. **Trust hierarchy** (omit — link here instead, or restate only if the task's source ordering differs meaningfully from the default in section 5)

---

## 9. Contributing a playbook

Playbooks that helped one session likely help everyone running similar work. If a recurring task in your sessions doesn't have a playbook, or an existing one is missing a pitfall you discovered, please PR it back:

1. **Fork** [poe_mcp_suite](https://github.com/charleslucas/poe_mcp_suite)
2. **Draft** in `playbooks/your-task-name.md` — use [`dps-analysis.md`](dps-analysis.md) as the reference example
3. **Test** in at least one real session — untested playbooks tend to have wrong data-load assumptions
4. **Open a PR** with: what task shape it covers, the triage questions, and the most important pitfall captured

Reviewing PRs: playbooks must solve a *recurring* shape, not a one-off; triage questions must affect Step 2; pitfalls must be specific and falsifiable; avoid duplicating content from `reference_data/` (link instead).
