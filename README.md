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

**Path of Building Community**
The PathOfBuilding submodule is a fork of Path of Building Community, originally created by David Gowor and maintained by the PoB Community team.
- Upstream repo: [PathOfBuildingCommunity/PathOfBuilding](https://github.com/PathOfBuildingCommunity/PathOfBuilding)

**ianderse/pob-mcp**
The pob-mcp server started as a fork of ianderse's pob-mcp project.
- Original repo: [ianderse/pob-mcp](https://github.com/ianderse/pob-mcp)


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
- **Character**: fetch live gear and passive tree from the PoE API, export as PoB XML
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

## A note on Claude's Path of Exile knowledge

Claude's built-in PoE knowledge is roughly current as of mid-2024 — content, balance changes, and mechanics introduced after that point may be missing or wrong. **Before relying on Claude's game-mechanics advice, confirm it against current sources.**

The MCP servers exist partly to bridge this gap: use `fetch_wiki_page` (POEMCP) for up-to-date item and passive descriptions, `ninja_lookup` / `currency_overview` for current prices, and `parse_pob` or the live PoB TCP connection for accurate calc results. When Claude's training intuition conflicts with a live tool result, trust the tool.

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

