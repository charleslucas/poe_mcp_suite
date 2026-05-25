# poe_mcp_suite — Notes for Claude

**Setup / post-pull:** If this is a fresh clone or you just ran `git pull`, read [`CLAUDE_INSTALL.md`](CLAUDE_INSTALL.md) to check for new installation steps or tools that need running.

**Before any analysis task:** Load [`playbooks/README.md`](playbooks/README.md) (meta-framework: cursory/detailed gate, context management, league pre-flight, narration norms, trust hierarchy) plus the matching specific playbook — **before** pulling any data. If no playbook exists for the task shape, note that and proceed; if the task recurs, write one.

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
