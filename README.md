# poe_mcp_suite

A suite of [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) servers that give Claude deep, live integration with Path of Exile — from build theory-crafting and passive tree simulation to trade, stash management, loot filters, and wiki lookups.

Each server runs independently and exposes a set of tools that Claude can call during conversation. Together they allow Claude to act as an informed PoE assistant: loading your actual build in Path of Building, simulating node choices, checking prices on poe.ninja, searching trade, scoring stash tab items, and more — all without leaving the chat.

poe_mcp_suite is a master git repo that acts a wrapper for four independently developed MCP tools and some other useful utilities.

Point your Claude instance, or other AI at the CLAUDE.md file, and it should find everything it needs to install, connect to Path of Exile and Path of Building, and use all the various API calls for the tools.

If you have any issues or suggestions feel free to e-mail at zerosquaredio@gmail.com, or make changes in your own repos and create pull requests back to this one. 

---

## Tool Reference

Each submodule includes a `TOOLS.md` with a full list of available tools:

- [pob-mcp/docs/TOOLS.md](pob-mcp/docs/TOOLS.md)
- [poe-mcp-server/TOOLS.md](poe-mcp-server/TOOLS.md)
- [POEMCP/TOOLS.md](POEMCP/TOOLS.md)
- [PathOfBuilding/src/API/TOOLS.md](PathOfBuilding/src/API/TOOLS.md)

---

## Credits

**Grinding Gear Games**
This project would not exist without [Path of Exile](https://www.pathofexile.com) — the game itself, the ongoing development, and GGG's decision to publish official passive tree and atlas tree data as open repositories that the community can fork and build on.
- Game: [pathofexile.com](https://www.pathofexile.com)
- Official skill tree data: [grindinggear/skilltree-export](https://github.com/grindinggear/skilltree-export) (upstream of our [poe-skilltree-export](https://github.com/charleslucas/poe-skilltree-export) fork)
- Official atlas tree data: [grindinggear/atlastree-export](https://github.com/grindinggear/atlastree-export) (upstream of our [poe-atlastree-export](https://github.com/charleslucas/poe-atlastree-export) fork)

**Path of Building Community**
The PathOfBuilding submodule is a fork of Path of Building Community, originally created by David Gowor and maintained by the PoB Community team.
- Upstream repo: [PathOfBuildingCommunity/PathOfBuilding](https://github.com/PathOfBuildingCommunity/PathOfBuilding)

**ianderse/pob-mcp**
The pob-mcp server started as a fork of ianderse's pob-mcp project.
- Original repo: [ianderse/pob-mcp](https://github.com/ianderse/pob-mcp)

**boschzilla / poe-mcp-server**
The poe-mcp-server started as a fork of boschzilla's poe-mcp-server project.
- Original repo: [boschzilla on GitHub](https://github.com/boschzilla) · [@boschzilla on X](https://x.com/boschzilla)

**shalayiding / POEMCP**
The POEMCP server started as a fork of shalayiding's POEMCP project.
- Original repo: [shalayiding/POEMCP](https://github.com/shalayiding/POEMCP)

---

## A note on Claude's Path of Exile knowledge

Claude's built-in PoE knowledge is roughly current as of mid-2024 — content, balance changes, and mechanics introduced after that point may be missing or wrong. **Before relying on Claude's game-mechanics advice, confirm it against current sources.**

The MCP servers exist partly to bridge this gap: use `fetch_wiki_page` (POEMCP) for up-to-date item and passive descriptions, `ninja_lookup` / `currency_overview` for current prices, and `parse_pob` or the live PoB TCP connection for accurate calc results. When Claude's training intuition conflicts with a live tool result, trust the tool.

---

## How Claude organizes the work (and how you help)

Path of Exile is a *huge* game — thousands of items, modifiers, passive nodes, atlas mechanics, league-specific systems, all interacting in ways that change every patch. No single source — not Claude's training, not the wiki, not poe.ninja, not Path of Building — is correct about all of it all the time. To make this manageable, the suite uses a small workflow framework that you'll see Claude reference during sessions.

### Playbooks

When you start a recognizable task — "help me improve my DPS," "what map mods should I run," "is this rare worth keeping?" — Claude loads a matching **playbook** from [`playbooks/`](playbooks/). Each playbook contains:

- A short **triage questionnaire** to scope the work (goal, budget, locked items, etc.) — answering 3-4 questions up front saves a lot of back-and-forth later
- A **data-load matrix** that determines which sources Claude needs (skip the atlas tree if we're doing a gear-only analysis, etc.)
- The **analysis pattern** to follow, in order
- A **pitfalls section** with concrete lessons from previous sessions ("Diamond Shrine does NOT grant ailment immunity" / "Body armour Eldritch has no mana cost mod") — so prior mistakes don't get repeated

Playbooks are committed to this repo; if a task shape recurs and a playbook doesn't exist yet, Claude can draft one mid-session.

> **Sharing playbooks back:** if you or Claude draft a new playbook that works well for you, or you have improved an existing one with new data sources, or you've added MCPs or tools, please consider opening a pull request to this repo so others can gain from your insights. See [`playbooks/README.md`](playbooks/README.md) for format conventions and submission guidelines. Pitfalls discovered in one session can save hours for the next person who hits the same wall.

### Reference data cache

Slowly-changing game data — the official GGG passive tree exports, atlas tree, Eldritch implicit pools, shrine mechanics — gets cached locally in [`reference_data/`](reference_data/) so Claude doesn't re-fetch it every session. The directory itself is gitignored (the data is regenerable and large), but `reference_data/README.md` is committed and tells a fresh clone how to populate it. Each cached file has a `fetched:` date and `league:` in its frontmatter so staleness is easy to spot.

### Per-character analyses

Detailed build analyses for each character live in [`character_analyses/<League>-<CharName>.md`](character_analyses/) — also gitignored, since they include playstyle notes and personal info. Claude reads the doc at the start of a session and appends new findings, decisions, and crafting outcomes as you work.

### Your role as co-pilot on data hygiene

Claude will narrate what it's doing so you can follow along — *"Pulling current Eldritch pool from poewiki — cached version is 14 days old," "Writing this to `reference_data/X.md` so we don't refetch next time."* When data is stale, missing, or possibly out of date for the current league, **Claude will ask you for help**:

- *"Can you paste an Eldritch boots mod list from your stash so I have current data?"*
- *"Has GGG changed how rage decay works recently? My training says X but I want to verify."*
- *"What does your current Atlas tree look like? — I don't have an authoritative source for the current league."*

Your in-game observations are the single most authoritative source for your specific situation, and your help refreshing the local cache compounds — better data this session means faster, more accurate analyses in every future session. The game is constantly changing; you're the freshest data source we have.

*Also* - Claude (or any AI) is forgetful after a context compression.  I have tried to create a playbook and context-management framework to encourage Claude to always cache the most up-to-date data before doing analyses, and have given it awareness of it's own context so it can intelligently load data and write out any analysis results before compression happens.  But Claude still will forget and fall-back to using it's trained-in game data, which is a couple years out of date.  Diligence on asking it if it has read the playbooks, loaded recent data sources, and written it's results to the character cache will help keep it on track and provide much better analyses.

---

## Servers

### pob-mcp
**Repo:** [charleslucas/pob-mcp](https://github.com/charleslucas/pob-mcp) · **~96 tools**

The core build-analysis server. Connects Claude to [Path of Building](https://github.com/PathOfBuildingCommunity/PathOfBuilding) — either headless (for batch work) or live via a TCP socket to the running PoB GUI. When connected live, every change Claude makes (adding a gem, allocating a passive, swapping an item) appears in the PoB window in real time.

Key capabilities:
- Load, save, and compare build files
- Read and write the passive tree, gems, items, config, and notes
- Simulate passive node upgrades and mastery effect choices by actually running PoB's calc engine — no guessing
- Validate builds against endgame boss thresholds, check resistances, identify flask immunity gaps
- Find best anointments, suggest Watcher's Eye mods, rank cluster jewel notables
- Import characters directly from the PoE API
- Search trade for upgrades, generate weighted trade queries, check poe.ninja prices

### poe-mcp-server
**Repo:** [charleslucas/poe-mcp-server](https://github.com/charleslucas/poe-mcp-server) · **~30 tools**

A multi-server bundle covering the player-facing side of the economy and account data.

Key capabilities:
- **Market**: local price-history database with risers/fallers/movers tracking
- **Stash**: read stash tabs via the PoE API, search across tabs, score and price rare items
- **Trade**: search the official PoE trade site with full filter support, look up stat IDs, fetch listing details
- **Character**: fetch live gear including all flask slots, ring slots (Ring1–3), and weapon swap slots from the PoE API; export as PoB XML. All required modules (`poe_lib`, `stash_cache`, `rare_scorer`, `poe_oauth`) are bundled — no external sibling repositories needed.
- **Pricer**: price individual or batch items using poe.ninja and a rare-item scorer
- **Filter**: read and edit loot filter files in place — find blocks, add/remove/replace rules, set BaseType priorities

### POEMCP
**Repo:** [charleslucas/POEMCP](https://github.com/charleslucas/POEMCP) · **13 tools**

A knowledge and economy lookup server backed by the PoE wiki and poe.ninja.

Key capabilities:
- Search and retrieve detailed data for gems, unique items, and passive nodes (keystones, notables, masteries, ascendancy)
- Look up item modifiers (prefix/suffix) by item type
- Search maps and scarabs with category filtering
- Current poe.ninja prices and currency exchange rates
- Fetch cleaned content from any poewiki.net page
- Parse a Path of Building export code or share URL into a readable build summary

### PathOfBuilding *(api-stdio branch)*
**Repo:** [charleslucas/PathOfBuilding](https://github.com/charleslucas/PathOfBuilding/tree/api-stdio)

A fork of Path of Building Community with a JSON-RPC API layer added (`src/API/`). This is the calculation backend that `pob-mcp` connects to. It exposes PoB's full calc engine — passive tree simulation, item stat computation, full DPS/EHP calculations — over a TCP socket (live GUI mode) or stdio (headless mode).

The API additions live on the `api-stdio` branch and are designed to be non-destructive: the PoB GUI remains fully usable while Claude works with the same build through the API.

---

## Data Submodules

In addition to the four MCP server submodules above, two data repositories live under [`reference_data/`](reference_data/) as submodules. These are community forks of GGG's official tree exports, augmented with patches overlay files for corrections that GGG hasn't yet published.

### poe-skilltree-export *(community fork)*
**Repo:** [charleslucas/poe-skilltree-export](https://github.com/charleslucas/poe-skilltree-export) · **Path:** `reference_data/skilltree/`

Fork of GGG's official passive skill tree export. The upstream `data.json` is preserved verbatim; a sibling `data_patches.json` carries verified corrections with provenance metadata (who verified, when, against what source). Tools merge the two files at load time; on-disk, the GGG export stays pristine so `git merge upstream/master` works cleanly. See the fork's `PATCHES.md` for the protocol.

### poe-atlastree-export *(community fork)*
**Repo:** [charleslucas/poe-atlastree-export](https://github.com/charleslucas/poe-atlastree-export) · **Path:** `reference_data/atlastree/`

Same convention applied to GGG's atlas tree export. Identical patch format and merge policy so a single tool can serve both.

Both forks are real submodules and travel with the suite — `git clone --recurse-submodules` gets you everything. Each fork has `origin` pointing at the community fork and `upstream` pointing at GGG's repo, so pulling new GGG releases is a standard `git fetch upstream && git merge upstream/master` inside the submodule.

---

## Prerequisites

Before cloning, make sure the following are installed and on your system PATH:

| Requirement | Version | Used by | Download |
|-------------|---------|---------|----------|
| **Node.js** | 18 LTS+ | pob-mcp | [nodejs.org](https://nodejs.org) |
| **Python** | 3.10+ | poe-mcp-server, POEMCP | [python.org](https://python.org) |
| **Git** | 2.x+ | submodule checkout | [git-scm.com](https://git-scm.com) |
| **Path of Building Community** | latest | TCP live mode | [GitHub releases](https://github.com/PathOfBuildingCommunity/PathOfBuilding/releases) |

> **Windows users:** after installing Node.js, restart any open terminals (and VS Code / Claude Code) so the updated PATH takes effect. If Claude Code can't start the `pob` MCP server, this is almost always the cause.

---

## Quick Start

```bash
git clone --recurse-submodules https://github.com/charleslucas/poe_mcp_suite.git
cd poe_mcp_suite
```

Or if you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

**Install Python dependencies** (covers poe-mcp-server, POEMCP, and RePoE):

```bash
pip install -r requirements.txt
pip install -e POEMCP/
```

**Install pob-mcp** (Node.js):

```bash
cd pob-mcp && npm install && npm run build && cd ..
```

To use `pob-mcp` in live mode, launch Path of Building via `pob-mcp/LaunchPoBWithAPI.bat` rather than the normal shortcut. This sets the environment variables that activate the TCP API server inside PoB.

---

## MCP Client Configuration

### 1. Copy the template

A `.mcp.json.example` is included at the repo root. Copy it to `.mcp.json` and fill in the four `CHANGE_ME` values:

```bash
cp .mcp.json.example .mcp.json
# then open .mcp.json and edit it
```

The four things to change:

| Placeholder | What to put |
|-------------|-------------|
| `/CHANGE_ME/poe_mcp_suite` (×3) | Absolute path to your clone, e.g. `C:/Users/you/tools/poe_mcp_suite` |
| `C:/Users/CHANGE_ME/AppData/...` | Your PoB builds folder — the Windows default is shown; adjust username or path if needed |
| `CHANGE_ME_your_POESESSID_cookie` | Your `POESESSID` session cookie (see below) |
| `CHANGE_ME_YourAccount#1234` | Your PoE account name including the `#` discriminator |

> **Security:** `.mcp.json` contains your session cookie — treat it like a password. It is listed in `.gitignore` and must never be committed.

### 2. Get your POESESSID cookie

`POE_SESSION_ID` is required for importing private characters and running weighted trade queries. To find it:

1. Log in to [pathofexile.com](https://www.pathofexile.com)
2. Open browser DevTools → Application (Chrome) or Storage (Firefox) → Cookies → `pathofexile.com`
3. Copy the value of the `POESESSID` cookie

### 3. Claude Desktop vs Claude Code

- **Claude Code** — `.mcp.json` goes in the workspace root (already where you put it above)
- **Claude Desktop** — paste the same `mcpServers` block into:
  - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
  - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
