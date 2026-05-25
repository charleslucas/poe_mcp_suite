# poe_mcp_suite — Notes for Claude

**Setup / post-pull:** If this is a fresh clone or you just ran `git pull`, read [`CLAUDE_INSTALL.md`](CLAUDE_INSTALL.md) to check for new installation steps or tools that need running.

---

- **Distinguish cursory from detailed analyses, and ask before starting a detailed one.**

  **Cursory** — proceed immediately, no user approval needed:
  - Uses only: training data, already-cached character files (`meta.json`, `inventory.json`, `journal.md`), a single pobb.in/poedb.tw XML diff, or a ninja price lookup
  - Produces: a quick answer, a one-question comparison, a price check, a brief mechanic explanation
  - Expected new tokens: <5K; no heavy data fetches; no wiki pages, transcripts, or tree node lookups

  **Detailed** — present a plan and wait for approval before loading data:
  - Will touch: passive tree node descriptions, wiki pages, YouTube transcripts, multiple builds, multiple data sources in sequence
  - Involves: multiple distinct analysis stages (tree → items → gems → Ascendancy → synthesis), or iterating across those dimensions more than once
  - Expected new tokens: >10K; likely needs context management
  - Trigger phrases: "comprehensive analysis", "optimize my build", "compare these guides", "full review", or any request where you can enumerate 4+ distinct data sources needed

  When a request is **detailed**, respond with a brief plan before touching any data:
  > "This looks like a detailed analysis. Here's what I'd cover and in what order: [stage list with expected data sources]. Want me to proceed, or should we narrow the scope first?"

  The user can then confirm, trim the scope, or ask for a cursory take instead. Never start loading tree nodes, transcripts, or wiki pages without this gate for detailed work.

- **Check context headroom before loading heavy data.** Call `mcp__pob__get_context_usage` at the start of any session that will load multiple large sources (transcripts, full character data, tree diffs, league reference + gem lookups together). The tool reads only the last 8KB of the session JSONL — it's fast. Rough token costs to keep in mind:

  | Source | Approx tokens |
  |---|---|
  | `meta.json` | ~500 |
  | `inventory.json` | ~2-3K |
  | `build.md` + `journal.md` | ~8-12K combined |
  | YouTube transcript (38K chars) | ~10-12K |
  | `reference_data/leagues/{league}.md` | ~4-5K |
  | `mcp__pob__lua_get_stats` result | ~500-1K |
  | Python-processed output (tree diff, XML parse) | **only the output**, not the raw file — this is a key efficiency win |

  **At 60%+:** prefer cached summaries over raw data; use compact tool outputs (category-specific stats, not `category='all'`); read `meta.json` + `journal.md` rather than every character file.
  **At 80%+:** write key findings to `character_data/` before continuing; consider asking the user to `/compact`.
  A PreToolUse hook in `.claude/settings.json` warns automatically at 70%+ (CLI sessions only; VS Code extension reads the hook config but env vars may not be available). The MCP tool works in both environments.
  **For analyses that won't fit in one session:** use the staged checkpoint pattern from [`playbooks/multi-stage-analysis.md`](playbooks/multi-stage-analysis.md). Each stage loads one data slice, distills findings to a JSON checkpoint in `buffer/`, then releases the raw data before the next stage. Synthesis stages (cross-referencing checkpoint findings) cost almost no context and can always run after a `/compact`.
  **After any multi-stage or context-heavy analysis:** append an entry to `character_data/analysis_log.md`. This accumulates empirical token costs for each data source (actual vs. estimated) and records whether compaction caused data loss. The calibration table in that file is how the rough estimates in this documentation get refined over time.

- **Know which model you're running and suggest switches when appropriate.** Call `mcp__pob__get_context_usage` — it now reports the model ID alongside session state. Current models and their trade-offs:

  | Model | Context window | Best for |
  |---|---|---|
  | `claude-opus-4-7` | 200K | Complex multi-step reasoning, novel build synthesis, difficult cross-analysis |
  | `claude-sonnet-4-6` | 200K | General analysis, code, most PoE tasks — good default |
  | `claude-haiku-4-5` | 200K | Fast lookups, price checks, simple queries — use when speed matters more than depth |

  If the user is on Sonnet/Haiku and asks for something that clearly needs deeper reasoning (e.g. synthesizing 5 guide builds into a novel build), mention: *"This would benefit from Opus — you can switch with `/model opus` if you'd like."* Don't switch automatically; just inform. Conversely, if on Opus for a simple price lookup, Haiku would be faster. Log the model in `analysis_log.md` entries so we can identify over time whether certain tasks genuinely benefit from specific models.

- **Your built-in PoE knowledge is roughly current as of mid-2024.** Content, balance changes, and mechanics introduced after that point may be missing or wrong in your training data. When answering questions about game mechanics, items, or skills, proactively use the MCP tools to pull current data rather than relying solely on training: `fetch_wiki_page` for item/passive descriptions, `ninja_lookup`/`currency_overview` for prices, and the live PoB TCP connection for calc results. Tell the user when you're uncertain whether your training reflects the current patch, and always defer to live tool results over training intuition when they conflict.
- **Load the matching playbook from `playbooks/` at the start of recognizable task types.** Playbooks are workflow definitions for recurring task shapes (DPS analysis, atlas planning, etc.). Each playbook has a structured triage step to scope the work, a data-load matrix that gates which sources to fetch, an analysis pattern, an output shape, and a pitfalls section with concrete lessons from prior sessions. Loading the playbook BEFORE pulling data prevents context-wasteful broad sweeps. Playbooks are committed (workflow definitions, not personal data); start a new one whenever a task shape repeats enough to warrant the structure. See [`playbooks/README.md`](playbooks/README.md) for the required format.
- **When you draft a new playbook (or significantly extend an existing one with pitfalls), tell the user it would be valuable to PR back to the main repo.** A playbook that helped one session likely helps everyone else running similar work. Frame it as community contribution, not chore: *"This playbook captured some hard-won lessons from our session today — if you'd like to PR it back to [poe_mcp_suite](https://github.com/charleslucas/poe_mcp_suite), other users (and their Claudes) would benefit from the same shortcuts."* See `playbooks/README.md` for submission guidelines.
- **Narrate the process so the user becomes a co-pilot on data hygiene.** When you start a recognized task, say which playbook you're loading and why ("Using the DPS Analysis playbook — quick triage first, then I'll pull these data sources..."). When you fetch live data, say so ("Pulling current Eldritch pool from poewiki — the cached version is 14 days old"). When you cache new data, say so ("Writing this to `reference_data/X.md` so we don't refetch next time"). When data is stale, missing, or you suspect a league rule changed, **ask the user for help**: "I don't have current data for X. Quickest path is for you to check in-game and paste what you see — that's more authoritative than the wiki anyway." Frame their participation as a force multiplier ("Up-to-date local data lets me run faster, more accurate analyses next time"), not a chore. Game knowledge has a half-life; the user's in-game observations are always more current than any cache or wiki.
- **Check `reference_data/` first for cached game knowledge.** Eldritch implicit pools, crafting mods, shrine details, GGG official tree exports, and other slowly-changing game data live there. Read the frontmatter (`fetched:` date and `league:`) to check staleness. If outdated or missing, fetch from source and update the cache. The directory itself is gitignored (data is regenerable), but `reference_data/README.md` IS committed — read it on first contact with a fresh clone to see what should be set up. New clones need to follow the setup steps in that README (clone GGG repos for `skilltree/` and `atlastree/`, fetch Eldritch wiki pages, etc.).
- **At the start of any session involving current-league content, load `reference_data/leagues/{current-league}.md` if it exists.** Per-league mechanic summaries cover the league-specific drop tables, unique items, scarab/atlas-node availability, and strategic implications — things that change every 3 months and aren't in Claude's training. The current league name is set in `.mcp.json` as `POE_LEAGUE`. If the file doesn't exist for the current league, generate it from the poewiki page (`fetch_wiki_page` on `https://www.poewiki.net/wiki/{LeagueName}_league`) on first use and write it back as a cache.
- **Check `character_data/guides/` for accumulated build guide research before analyzing a build archetype.** The global guide library lives at `character_data/guides/{archetype}/` (e.g. `cyclone-slayer/`). Each archetype has a `README.md` (consensus notes, current best guide by tier), JSON entries per guide (author, pobb.in, YouTube, key stats, notes), `synthesis.md` for best-of analysis, and a `buffer/` for raw transcripts. The library is account-agnostic — same guides are relevant across characters and leagues. When starting a build comparison or analysis session, read the archetype README first to see what's already known; add a new JSON entry and update the README when a new guide is analyzed.

- **Check `character_data/<Account>/<Character>/` before starting work on a character.** Per-character data lives in an external cache (real path: `%APPDATA%/poe_claude_data/` on Windows) exposed inside the repo via a directory junction at `character_data/`. The junction is gitignored; the data outlives the repo and can be backed up independently. Layout per character:
  - `meta.json` — identity + current stats snapshot (class, level, league, life/ES/DPS, masteries, bandit). Read this first to scope any task.
  - `inventory.json` — equipped items, flasks, jewels, eldritch implicits. Update structurally via Edit, not full rewrite.
  - `build.md` — narrative: concept, gap analysis vs guide, upgrade plans, open questions.
  - `journal.md` — append-only chronological decisions/crafting log. New entries go to the bottom under a `## YYYY-MM-DD` heading.
  - `snapshots/` — dated raw PoB XML exports for diffing over time.
  - `buffer/` — regenerable files kept for convenience (YouTube transcripts, raw API responses, build guide XMLs). Safe to delete if space is needed; filename convention is `{description}_{video_id_or_source}.txt`.

  Account dirs are named `<Name>_<Discriminator>` (e.g. `Memophage_4428` for `Memophage#4428`). If the junction is missing on a fresh machine, recreate it: `mklink /J "<repo>/character_data" "%APPDATA%/poe_claude_data"`. See `character_data/README.md` for full conventions and backup guidance.
- **TCP mode is strongly preferred** over headless — it shows every change in the PoB GUI in real time, requires no LuaJIT install, and auto-reconnects when PoB is restarted.
- **`POE_SESSION_ID` is sensitive** — treat it like a password. It enables importing private characters and running weighted trade queries. Never log or commit it.
- **PoB must be launched via `pob-mcp/LaunchPoBWithAPI.bat`**, not the normal shortcut, for TCP mode to work.
- **After a PoB update**, the batch file self-heals by re-patching `Modules/Main.lua`. Tell the user to dismiss the integrity check warning and relaunch via the batch file.
- **Submodule pointer updates**: when a sub-repo is updated, run `git submodule update --remote && git add -A && git commit && git push` in the suite repo to advance the pointers.
