# poe_mcp_suite — Claude Setup Guide

This repo is a git submodule container for four MCP servers used together with Claude for Path of Exile. There is no runnable code here — everything lives in the submodules.

## Servers at a glance

| Submodule | Language | What it does |
|-----------|----------|--------------|
| `pob-mcp/` | TypeScript / Node.js | Connects Claude to Path of Building — build analysis, passive tree simulation, gem/item management, trade |
| `poe-mcp-server/` | Python | Trade site search, stash tab management, item pricing, loot filter editing |
| `POEMCP/` | Python | Wiki lookups, game data (gems, items, passives, maps), poe.ninja economy |
| `PathOfBuilding/` | Lua | Fork of PoB with a TCP/stdio JSON-RPC API — the calc backend for pob-mcp |

---

## Step 0 — Clone with submodules

```bash
git clone --recurse-submodules https://github.com/charleslucas/poe_mcp_suite.git
cd poe_mcp_suite
```

If you cloned without `--recurse-submodules`:
```bash
git submodule update --init --recursive
```

---

## Step 1 — Prerequisites

### All platforms
- **Git** 2.x+
- **Node.js** 18+ and **npm** (for pob-mcp)
- **Python** 3.10+ (for poe-mcp-server and POEMCP)
- **Path of Building Community** installed (for TCP mode — standard install, no special version)

### Headless mode only (optional — TCP mode is simpler)
- **LuaJIT** in PATH

```bash
# macOS
brew install luajit

# Ubuntu/Debian
sudo apt-get install luajit

# Windows: download from https://luajit.org/ and add to PATH
```

---

## Step 2 — Install pob-mcp

```bash
cd pob-mcp
npm install
npm run build
cd ..
```

Verify: `node pob-mcp/build/index.js` should start without crashing.

**Detailed docs:** [`pob-mcp/README.md`](pob-mcp/README.md)

---

## Step 3 — Install POEMCP

```bash
cd POEMCP
pip install -e .
cd ..
```

Installs `mcp[cli]`, `httpx`, and `beautifulsoup4`. No API keys required — data is fetched at runtime from poedb.tw, poe.ninja, and poewiki.net.

**Detailed docs:** [`POEMCP/README.md`](POEMCP/README.md)

---

## Step 4 — Install poe-mcp-server

```bash
pip install -r poe-mcp-server/requirements.txt
```

This installs `mcp`, `anyio`, and the GitHub-sourced PyPoE + RePoE packages. All required modules (`poe_lib`, `stash_cache`, `rare_scorer`) are included directly in the `poe-mcp-server/` directory — no external sibling repositories needed.

Credentials are supplied via env vars in `.mcp.json` (`POE_SESSION_ID`, `POE_ACCOUNT_NAME`). A `poe-mcp-server/config.json` can be used as a fallback but is not required.

**Detailed docs:** [`poe-mcp-server/README.md`](poe-mcp-server/README.md)

---

## Step 5 — Set up PathOfBuilding for TCP mode (recommended)

TCP mode connects Claude to a **running PoB GUI** — no LuaJIT installation needed, and changes appear live in the PoB window.

### 5a — Install Path of Building Community

Install [Path of Building Community](https://github.com/PathOfBuildingCommunity/PathOfBuilding/releases) normally. It installs to `%APPDATA%\Path of Building Community\` on Windows.

### 5b — Run the API installer (first time only)

`InstallTcpApi.ps1` does three things:
1. Creates `%APPDATA%\Path of Building Community\API\`
2. Copies `TcpServer.lua`, `Handlers.lua`, and `BuildOps.lua` from `PathOfBuilding/src/API/` (the submodule)
3. Patches `Modules\Main.lua` to start the TCP server when PoB launches with `POB_API_TCP=1`

```powershell
# Run from the pob-mcp directory
cd pob-mcp
.\InstallTcpApi.ps1
```

**Directory layout the script expects:**
```
poe_mcp_suite/
  pob-mcp/
    InstallTcpApi.ps1   ← run this
    LaunchPoBWithAPI.bat
  PathOfBuilding/
    src/
      API/
        TcpServer.lua   ← copied to PoB's AppData
        Handlers.lua
        BuildOps.lua
```

The script finds `PathOfBuilding/src/API/` by looking one level up from `pob-mcp/` — so the suite's submodule layout works automatically.

You do **not** need to re-run this manually after PoB updates — the next step handles that.

### 5c — Launch PoB via the batch file (every time)

**Always** use `pob-mcp/LaunchPoBWithAPI.bat` to start PoB, not the normal shortcut. It:
- Sets `POB_API_TCP=1` and `POB_API_TCP_PORT=31337` in the environment
- Checks whether `Modules\Main.lua` still has the TCP patch; if PoB updated and overwrote it, automatically re-runs `InstallTcpApi.ps1` before launching
- Starts `Path of Building.exe`

```
pob-mcp\LaunchPoBWithAPI.bat
```

On startup, PoB's in-game console (press `~`) shows:
```
[PoB API] TCP server started on port 31337
[PoB API] Background keepalive active (~60 fps)
```

And on Claude connecting:
```
[PoB API] Claude connected (1 client(s) active)
[PoB API] >> get_stats
[PoB API] << get_stats ok
```

PoB can be minimised — a background keepalive posts `WM_NULL` every 16 ms to keep its frame loop running at ~60 fps even when it has lost focus.

### PoB update behaviour

PoB's built-in updater overwrites `Modules\Main.lua` and shows an integrity check warning. This is expected. Just close PoB and relaunch via `LaunchPoBWithAPI.bat` — it detects the missing patch and re-applies it automatically. The TCP server is already running in memory for that session, so the warning during the session is harmless.

**Detailed docs:** [`PathOfBuilding/README.md`](PathOfBuilding/README.md) — [`PathOfBuilding/src/API/TOOLS.md`](PathOfBuilding/src/API/TOOLS.md)

### Headless mode (alternative, requires LuaJIT)

The PathOfBuilding submodule is already on the `api-stdio` branch. Point `POB_FORK_PATH` at `PathOfBuilding/src/` and set `POB_CMD` to your LuaJIT binary — no separate clone needed.

---

## Step 6 — Configure your MCP client

A ready-to-edit template is included at the repo root: copy `.mcp.json.example` to `.mcp.json` and replace the four `CHANGE_ME` placeholders (clone path ×3, PoB builds path, `POE_SESSION_ID`, `POE_ACCOUNT_NAME`). Do **not** commit `.mcp.json` — it contains your session cookie.

```bash
cp .mcp.json.example .mcp.json
# then edit .mcp.json
```

### Claude Code (`.mcp.json` in workspace root)

```json
{
  "mcpServers": {
    "pob": {
      "command": "node",
      "args": ["/absolute/path/to/poe_mcp_suite/pob-mcp/build/index.js"],
      "env": {
        "POB_DIRECTORY": "/path/to/Path of Building/Builds",
        "POB_LUA_ENABLED": "true",
        "POB_API_TCP": "true",
        "POB_API_TCP_PORT": "31337",
        "POB_RECONNECT_TIMEOUT_MS": "300000",
        "POE_TRADE_ENABLED": "true",
        "POE_SESSION_ID": "your-poesessid-cookie-here",
        "POE_ACCOUNT_NAME": "YourAccount#1234"
      }
    },
    "poe": {
      "command": "python",
      "args": ["/absolute/path/to/poe_mcp_suite/poe-mcp-server/poe_all.py"],
      "env": {
        "POE_SESSION_ID": "your-poesessid-cookie-here",
        "POE_ACCOUNT_NAME": "YourAccount#1234",
        "POE_LEAGUE": "Mirage",
        "POE_CONTACT_EMAIL": "your@email.com"
        // Optional — add POE_CLIENT_ID once you have a developer account:
        // "POE_CLIENT_ID": "your-client-id-here"
      }
    },
    "poemcp": {
      "command": "python",
      "args": ["/absolute/path/to/poe_mcp_suite/POEMCP/server.py"]
    }
  }
}
```

### Claude Desktop

Same JSON block in:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

---

## Key environment variables (pob-mcp)

| Variable | Required | Description |
|----------|----------|-------------|
| `POB_DIRECTORY` | Yes | Path to your PoB builds folder |
| `POB_LUA_ENABLED` | Yes | `"true"` to enable any Lua bridge features |
| `POB_API_TCP` | TCP mode | `"true"` to connect to running PoB GUI |
| `POB_API_TCP_PORT` | No | Port PoB listens on (default `31337`) |
| `POB_FORK_PATH` | Headless only | Path to `PathOfBuilding/src/` |
| `POB_CMD` | Headless only | Path to LuaJIT binary |
| `POB_TIMEOUT_MS` | No | Per-request timeout ms (default `10000`) |
| `POB_RECONNECT_TIMEOUT_MS` | No | TCP reconnect window ms (default `300000` = 5 min) |
| `POE_TRADE_ENABLED` | Trade tools | `"true"` to enable trade/price tools |
| `POE_SESSION_ID` | Private profiles | Your `POESESSID` cookie — **treat like a password, never commit** |
| `POE_ACCOUNT_NAME` | No | Default PoE account name with discriminator (e.g. `Account#1234`) |

---

## Verifying the installation

With PoB running via `pob-mcp/LaunchPoBWithAPI.bat` and a build open, ask Claude:
> "Use lua_start and tell me the current build's DPS and life."

Claude connects to PoB, loads stats, and responds with numbers matching what PoB shows. In PoB's console you should see `>> get_stats` / `<< get_stats ok`.

For POEMCP: *"What does Headhunter do?"* → Claude calls `get_item_detail`.
For poe-mcp-server: *"What's the current price of a Mirror of Kalandra?"* → Claude calls `ninja_lookup`.

---

## Documentation map

| Topic | File |
|-------|------|
| pob-mcp full setup, all env vars, troubleshooting | [`pob-mcp/README.md`](pob-mcp/README.md) |
| pob-mcp tool list (96 tools, 11 categories) | [`pob-mcp/docs/TOOLS.md`](pob-mcp/docs/TOOLS.md) |
| poe-mcp-server setup and module architecture | [`poe-mcp-server/README.md`](poe-mcp-server/README.md) |
| poe-mcp-server tool list (~30 tools) | [`poe-mcp-server/TOOLS.md`](poe-mcp-server/TOOLS.md) |
| POEMCP setup | [`POEMCP/README.md`](POEMCP/README.md) |
| POEMCP tool list (13 tools) | [`POEMCP/TOOLS.md`](POEMCP/TOOLS.md) |
| PathOfBuilding API fork overview | [`PathOfBuilding/README.md`](PathOfBuilding/README.md) |
| PathOfBuilding Lua TCP action reference | [`PathOfBuilding/src/API/TOOLS.md`](PathOfBuilding/src/API/TOOLS.md) |
| Engineering decisions and bug history | [`pob-mcp/docs/DEVELOPMENT_HISTORY.md`](pob-mcp/docs/DEVELOPMENT_HISTORY.md) |
| Task playbooks (workflow definitions) | [`playbooks/`](playbooks/) |

---

## Notes for Claude

- **Your built-in PoE knowledge is roughly current as of mid-2024.** Content, balance changes, and mechanics introduced after that point may be missing or wrong in your training data. When answering questions about game mechanics, items, or skills, proactively use the MCP tools to pull current data rather than relying solely on training: `fetch_wiki_page` for item/passive descriptions, `ninja_lookup`/`currency_overview` for prices, and the live PoB TCP connection for calc results. Tell the user when you're uncertain whether your training reflects the current patch, and always defer to live tool results over training intuition when they conflict.
- **Load the matching playbook from `playbooks/` at the start of recognizable task types.** Playbooks are workflow definitions for recurring task shapes (DPS analysis, atlas planning, etc.). Each playbook has a structured triage step to scope the work, a data-load matrix that gates which sources to fetch, an analysis pattern, an output shape, and a pitfalls section with concrete lessons from prior sessions. Loading the playbook BEFORE pulling data prevents context-wasteful broad sweeps. Playbooks are committed (workflow definitions, not personal data); start a new one whenever a task shape repeats enough to warrant the structure. See [`playbooks/README.md`](playbooks/README.md) for the required format.
- **When you draft a new playbook (or significantly extend an existing one with pitfalls), tell the user it would be valuable to PR back to the main repo.** A playbook that helped one session likely helps everyone else running similar work. Frame it as community contribution, not chore: *"This playbook captured some hard-won lessons from our session today — if you'd like to PR it back to [poe_mcp_suite](https://github.com/charleslucas/poe_mcp_suite), other users (and their Claudes) would benefit from the same shortcuts."* See `playbooks/README.md` for submission guidelines.
- **Narrate the process so the user becomes a co-pilot on data hygiene.** When you start a recognized task, say which playbook you're loading and why ("Using the DPS Analysis playbook — quick triage first, then I'll pull these data sources..."). When you fetch live data, say so ("Pulling current Eldritch pool from poewiki — the cached version is 14 days old"). When you cache new data, say so ("Writing this to `reference_data/X.md` so we don't refetch next time"). When data is stale, missing, or you suspect a league rule changed, **ask the user for help**: "I don't have current data for X. Quickest path is for you to check in-game and paste what you see — that's more authoritative than the wiki anyway." Frame their participation as a force multiplier ("Up-to-date local data lets me run faster, more accurate analyses next time"), not a chore. Game knowledge has a half-life; the user's in-game observations are always more current than any cache or wiki.
- **Check `reference_data/` first for cached game knowledge.** Eldritch implicit pools, crafting mods, shrine details, GGG official tree exports, and other slowly-changing game data live there. Read the frontmatter (`fetched:` date and `league:`) to check staleness. If outdated or missing, fetch from source and update the cache. The directory itself is gitignored (data is regenerable), but `reference_data/README.md` IS committed — read it on first contact with a fresh clone to see what should be set up. New clones need to follow the setup steps in that README (clone GGG repos for `skilltree/` and `atlastree/`, fetch Eldritch wiki pages, etc.).
- **Check `character_analyses/<CharName>.md` before starting work on a character.** Per-character analyses (build concept, current state, upgrade plans, decisions log) live there. Gitignored. Update the doc with new findings as you go.
- **TCP mode is strongly preferred** over headless — it shows every change in the PoB GUI in real time, requires no LuaJIT install, and auto-reconnects when PoB is restarted.
- **`POE_SESSION_ID` is sensitive** — treat it like a password. It enables importing private characters and running weighted trade queries. Never log or commit it.
- **PoB must be launched via `pob-mcp/LaunchPoBWithAPI.bat`**, not the normal shortcut, for TCP mode to work.
- **After a PoB update**, the batch file self-heals by re-patching `Modules/Main.lua`. Tell the user to dismiss the integrity check warning and relaunch via the batch file.
- **Submodule pointer updates**: when a sub-repo is updated, run `git submodule update --remote && git add -A && git commit && git push` in the suite repo to advance the pointers.
