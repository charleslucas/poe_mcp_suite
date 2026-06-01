# poe_mcp_suite — Notes for Claude

**Setup / post-pull:** If this is a fresh clone or you just ran `git pull`, read [`CLAUDE_INSTALL.md`](CLAUDE_INSTALL.md) to check for new installation steps or tools that need running.

**Cursory-vs-detailed gate (cross-cutting — applies to EVERY task):** Before doing anything, decide whether the request is *cursory* (a quick lookup/answer — proceed directly, no playbook) or *detailed* (multi-source, multi-stage, or >10K expected tokens — engage the matching playbook and pause for approval before pulling data). This triage is domain-independent and lives here on purpose; the per-domain skills assume it has already happened. Full criteria in [`playbooks/README.md`](playbooks/README.md) section 1.

**Freshness check (a SEPARATE axis from cursory/detailed):** The cursory gate measures *effort*; freshness measures whether the answer depends on patch-specific game data. They're independent — a question can be cheap (one lookup) yet still be exactly what stale knowledge gets wrong. Classify the *content*:
- **Timeless / conceptual** — how a mechanic works, general tactics, the math — safe to answer from your own knowledge.
- **Patch-specific factual lookup** — what mods can roll on an item, what a passive node grants, a unique's current stats, prices, league specifics — your built-in PoE knowledge (~mid-2024) is unreliable and the game changes constantly. **Err on the side of freshness: fetch authoritative data by default.** On factual data you can never go wrong by being current; the only cost is time, context, and a few API calls. Almost every such lookup has a cheap authoritative path — `get_tree_node`, `search_crafting_mods` / `list_craftable_mods_for_base`, `get_essence_detail`, `calculate_mod_odds`, `fetch_wiki_page`, or live PoB. Prefer fetching over answering from memory; only ask "quick take from memory, or pull current data?" when the fetch would be genuinely expensive or multi-step. This is a problem for everyone — PoE has too much data, changing too often, to keep current from memory; the tools exist precisely so you don't have to.

**Playbooks & skills:** Detailed analysis procedures live in `playbooks/` (the single source of truth). Thin wrapper **skills** in `.claude/skills/` auto-trigger on matching detailed-scope requests and tell you to read `playbooks/README.md` (shared meta-framework: context management, league pre-flight, narration norms, trust hierarchy) plus the relevant specific playbook. If a skill fires for what is actually a cursory task, honor the gate above and answer directly instead. If no playbook exists for a recurring detailed task shape, note that and write one (then add a wrapper skill).

**Before extracting, modifying, or redistributing any Path of Exile game data — including writing to the `reference_data/skilltree/` or `reference_data/atlastree/` forks, or building any tooling that reads from a local PoE install — read [`legal_considerations.md`](legal_considerations.md).** It documents what the project deliberately does and does not redistribute, and why. Stay inside those boundaries:

- **Safe to publish to the forks:** node IDs, positions, connections, group/orbit data, node names, integer stat values and stat-table references — i.e., the same kinds of fields GGG already publishes in their own `data.json`.
- **Extract at runtime only — never commit to the forks or any public repo:** stat description templates (`passive_skill_stat_descriptions.txt`), Timeless Jewel transformation tables (`AlternatePassiveSkills`, `AlternatePassiveAdditions`), mod pools, item bases, gem descriptions, lore text, and any other creative/expressive content from the game.
- **Never extract:** art, icons, sounds, or anything else from `Bundles2/Art/`, `Bundles2/Audio/`, etc.

If you're unsure whether a particular extraction or redistribution falls inside the conservative boundary, **stop and ask the user before proceeding**. Don't infer; check.

**GGG trade API — warn + get explicit permission before first use each session:** The following tools hit `https://www.pathofexile.com/api/trade` directly, which GGG's ToS (section 7c) restricts and which a GGG developer has confirmed they don't want automated. Account bans are a real consequence. **The first time in any session you would call one of these tools, stop, warn the user clearly (ToS section 7c, account ban risk, which tool you're about to use and why it's risky), and require their explicit "yes, proceed" before continuing.** After the user confirms once in a session, you may call trade API tools freely for the rest of that session without re-prompting.

Tools that require this warning:
- `mcp__pob__search_trade_items`, `mcp__pob__find_weighted_trade_items` (⚠️ highest risk — multiple automated searches), `mcp__pob__compare_trade_items`, `mcp__pob__get_item_price`
- `mcp__poe__search_trade`, `mcp__poe__search_by_item_mods`, `mcp__poe__fetch_listing`

Tools that do NOT require this warning (they do not hit GGG's trade API):
- `price_item`, `price_items`, `price_tab`, `scan_stash_tabs` — local algo + poe.ninja only
- All other `mcp__pob__` tools — talk to local PoB only
- `ninja_lookup`, `currency_overview` — poe.ninja only
- `list_tabs`, `get_tab`, `get_character` — GGG's official OAuth gateway (approved path)

Full reasoning in [`legal_considerations.md`](legal_considerations.md) → "GGG Terms of Service" section.

---

- **Your built-in PoE knowledge is roughly current as of mid-2024.** Content, balance changes, and mechanics introduced after that point may be missing or wrong in your training data. Proactively use MCP tools to pull current data: `fetch_wiki_page` for item/passive descriptions, `ninja_lookup`/`currency_overview` for prices, live PoB TCP for calc results. Always defer to live tool results over training intuition when they conflict.

- **Check `reference_data/` first for cached game knowledge.** Eldritch implicit pools, crafting mods, shrine details, GGG official tree exports, and other slowly-changing game data live there. Read the `fetched:` date and `league:` frontmatter to check staleness. The directory is gitignored (data is regenerable), but `reference_data/README.md` IS committed — read it on first contact with a fresh clone. New clones need to follow the setup steps there (clone GGG repos for `skilltree/` and `atlastree/`, fetch Eldritch wiki pages, etc.).

- **At the start of any session involving current-league content, load `reference_data/leagues/{current-league}.md` if it exists.** The current league name is in `.mcp.json` as `POE_LEAGUE`. If the file doesn't exist, generate it from the poewiki page and cache it. Full guidance in [`playbooks/README.md`](playbooks/README.md) section 2b.

- **Check `character_data/guides/` for accumulated build guide research before analyzing a build archetype.** The global guide library lives at `character_data/guides/{archetype}/`. Each archetype has a `README.md` (consensus notes, current best guide by tier), JSON entries per guide, `synthesis.md`, and a `buffer/` for raw transcripts. Read the archetype README first; add a new entry when a new guide is analyzed.

- **Check `character_data/<Account>/<Character>/` before starting work on a character.** Per-character data lives in an external cache (`%APPDATA%/poe_claude_data/` on Windows) exposed via a directory junction at `character_data/`. Layout:
  - `meta.json` — identity + current stats snapshot. Read this first.
  - `inventory.json` — equipped items, flasks, jewels, eldritch implicits. Update via Edit, not full rewrite.
  - `build.md` — narrative: concept, gap analysis vs guide, upgrade plans, open questions.
  - `journal.md` — append-only chronological log. New entries at the bottom under `## YYYY-MM-DD`.
  - `snapshots/` — dated raw PoB XML exports.
  - `buffer/` — regenerable files (transcripts, raw API responses, build guide XMLs). Safe to delete.

  Account dirs are named `<Name>_<Discriminator>` (e.g. `Memophage_4428` for `Memophage#4428`). If the junction is missing: `mklink /J "<repo>/character_data" "%APPDATA%/poe_claude_data"`. See `character_data/README.md`.

- **TCP mode is strongly preferred** over headless — shows every change in the PoB GUI in real time, requires no LuaJIT install, auto-reconnects when PoB is restarted.
- **`POE_SESSION_ID` is sensitive** — treat it like a password. It enables importing private characters and running weighted trade queries. Never log or commit it.
- **PoB must be launched via `pob-mcp/LaunchPoBWithAPI.bat`**, not the normal shortcut, for TCP mode to work.
- **After a PoB update**, the batch file self-heals by re-patching `Modules/Main.lua`. Tell the user to dismiss the integrity check warning and relaunch via the batch file.
- **Submodule pointer updates**: when a sub-repo is updated, run `git submodule update --remote && git add -A && git commit && git push` in the suite repo to advance the pointers.
