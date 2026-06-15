# poe_mcp_suite — Installation Guide

This repo is a git submodule container for four MCP servers used together with Claude for Path of Exile. There is no runnable code here — everything lives in the submodules.

## Servers at a glance

| Submodule | Language | What it does |
|-----------|----------|--------------|
| `pob-mcp/` | TypeScript / Node.js | Connects Claude to Path of Building — build analysis, passive tree simulation, gem/item management, trade |
| `poe-mcp-server/` | Python | Trade site search (returns URLs), item pricing, loot filter editing; stash scanning ⚠️ blocked (see [`playbooks/stash-scanning.md`](playbooks/stash-scanning.md)) |
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

### Enable the submodule-pointer guard (recommended, one-time per clone)

This repo ships a tracked `pre-push` hook (`.githooks/pre-push`) that blocks a
suite push if any submodule pointer recorded in HEAD isn't reachable on that
submodule's own remote. It prevents the failure mode where the suite's
`origin/main` references submodule commits that were committed locally but never
pushed to the forks — which makes `git submodule update` fail on every other
clone. Git doesn't track hook *activation*, so enable it once per machine:

```bash
git config core.hooksPath .githooks
```

If a push is ever blocked, push the named submodule first (`git -C <submodule>
push origin <branch>`), then retry. Emergency bypass: `git push --no-verify`.

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
- Sets `POB_API_TCP=1` and `POB_API_TCP_PORT=59166` in the environment
- Checks whether `Modules\Main.lua` still has the TCP patch; if PoB updated and overwrote it, automatically re-runs `InstallTcpApi.ps1` before launching
- Starts `Path of Building.exe`

```
pob-mcp\LaunchPoBWithAPI.bat
```

On startup, PoB's in-game console (press `~`) shows:
```
[PoB API] TCP server started on port 59166
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

**Auto-updates are suppressed while the TCP API is active.** The "Update Ready" button is hidden and the "Update Available" toast notification is muted — both would, if triggered, replace `Modules\Main.lua` mid-session and break Claude's connection. PoB's startup console banner (`~` key) re-states this every launch.

**To check for updates manually**, do it occasionally (say every couple of weeks):

1. Close PoB.
2. Relaunch PoB via the **normal shortcut** (not `LaunchPoBWithAPI.bat`).
3. Click *Check for Update* — apply if one's available.
4. Close PoB again.
5. Relaunch via `LaunchPoBWithAPI.bat`. It detects that the update wiped the patch and re-applies it (you may see an integrity check warning during launch — dismiss it; the patch is already back in memory).

**If you accidentally update mid-session via some other path**, you'll see an integrity check warning and the API will stop working. Same fix: close PoB and relaunch via the batch file; it self-heals.

**Detailed docs:** [`PathOfBuilding/README.md`](PathOfBuilding/README.md) — [`PathOfBuilding/src/API/TOOLS.md`](PathOfBuilding/src/API/TOOLS.md)

### Headless mode (alternative, requires LuaJIT)

The PathOfBuilding submodule is already on the `api-stdio` branch. Point `POB_FORK_PATH` at `PathOfBuilding/src/` and set `POB_CMD` to your LuaJIT binary — no separate clone needed.

---

## Step 6 (optional) — Use with Claude.ai web instead of Claude Code

Claude Code connects to MCP servers via **stdio** (subprocess). Claude.ai web uses **HTTP/SSE** (network). The three servers in this suite currently support stdio only, so using them from Claude.ai web requires two things:

1. **HTTP transport mode** — each server needs to serve over HTTP/SSE instead of stdin/stdout
2. **Public URL** — Claude.ai's servers can't reach `localhost`; a tunnel makes your local servers accessible

> ⚠️ **HTTP transport is not yet implemented.** This section documents the intended path. See `ISSUES.md` → "HTTP/SSE transport for Claude.ai integration" for the remaining work. Once that's done, the tunnel setup below is how you'd connect.

### Why bother? The git/PR model is preserved

Each user runs their own instance locally and connects their own credentials. Nobody shares a server. The playbooks, skills, and CLAUDE.md stay in the repo — improving them via PR works exactly the same as with Claude Code.

### The intended setup (once HTTP transport is implemented)

**1. Run servers in HTTP mode**

Each server will need to be started with an HTTP/SSE flag instead of (or alongside) stdio mode:

```bash
# poe-mcp-server — once HTTP mode is added
python poe-mcp-server/poe_all.py --http --port 8481

# POEMCP — FastMCP already supports this, likely just:
python POEMCP/server.py --transport sse --port 8484

# pob-mcp — once SSEServerTransport is wired in
node pob-mcp/build/index.js --http --port 8480
```

The exact flags will be documented here once implemented.

**2. Expose servers via Cloudflare Tunnel (free, no account needed)**

```bash
# Install cloudflared
# Windows: winget install Cloudflare.cloudflared
# macOS:   brew install cloudflare/cloudflare/cloudflared

# Run a tunnel for each server (each gets a random HTTPS URL)
cloudflared tunnel --url http://localhost:8480   # pob-mcp
cloudflared tunnel --url http://localhost:8481   # poe-mcp-server
cloudflared tunnel --url http://localhost:8484   # POEMCP
```

Each tunnel prints something like `https://random-name.trycloudflare.com`. Save those URLs.

**3. Add to Claude.ai**

1. Open Claude.ai → Settings → Integrations → Add custom integration
2. Paste each tunnel URL as an MCP server endpoint
3. Claude.ai connects and the tools are available in web sessions

### Limitations to be aware of

- **PoB must run locally.** The pob-mcp tools talk to a running Path of Building GUI via TCP. Even with a tunnel, PoB has to be on your local machine — the tunnel just makes Claude.ai's requests reach your local pob-mcp server, which then talks to local PoB. This works fine as long as you're at your computer.
- **Credentials stay local.** `POE_SESSION_ID` and `POE_ACCOUNT_NAME` live in your environment; they never leave your machine. The tunnel only forwards MCP protocol messages.
- **Tunnels are ephemeral.** Free Cloudflare tunnels get a new random URL on each restart. For persistent URLs, use a named tunnel (requires a free Cloudflare account) or ngrok.
- **No stash scanning yet.** Stash tools are blocked regardless of transport (GGG API issue, not a transport issue).

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
        "POB_API_TCP_PORT": "59166",
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
| `POB_API_TCP_PORT` | No | Port PoB listens on (default `59166`) |
| `POB_FORK_PATH` | Headless only | Path to `PathOfBuilding/src/` |
| `POB_CMD` | Headless only | Path to LuaJIT binary |
| `POB_TIMEOUT_MS` | No | Per-request timeout ms (default `10000`) |
| `POB_RECONNECT_TIMEOUT_MS` | No | TCP reconnect window ms (default `300000` = 5 min) |
| `POE_TRADE_ENABLED` | Trade tools | `"true"` to enable trade/price tools |
| `POE_SESSION_ID` | Private profiles | Your `POESESSID` cookie — **treat like a password, never commit** |
| `POE_ACCOUNT_NAME` | No | Default PoE account name with discriminator (e.g. `Account#1234`) |

---

## Verifying the installation

For a thorough, repeatable check after any fresh clone, `git pull`, submodule bump, or `.mcp.json` change, load [`playbooks/verify-install.md`](playbooks/verify-install.md) and run the four-tier suite. It exercises the filesystem layout, then each MCP server in turn, and ends with a single green/red summary table. Includes a regression test for the MapStash crash fix.

Quick smoke test (less thorough):
- With PoB running via `pob-mcp/LaunchPoBWithAPI.bat` and a build open, ask Claude: *"Use lua_start and tell me the current build's DPS and life."* Console should show `>> get_stats` / `<< get_stats ok`.
- For POEMCP: *"What does Headhunter do?"* → Claude calls `get_item_detail`.
- For poe-mcp-server: *"What's the current price of a Mirror of Kalandra?"* → Claude calls `ninja_lookup`.

---

## Backing up your data

The git-tracked code is recoverable by re-cloning, but your `character_data`
(journals, snapshots, build analysis) and Claude `memory` live outside git. Back
them up to a timestamped zip with:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\backup-data.ps1
```

and restore on any machine with `scripts\restore-data.ps1 -Zip <file>`. Full
details, options, and cross-machine caveats: [`BACKUP.md`](BACKUP.md).

---

## Documentation map

| Topic | File |
|-------|------|
| Backing up / restoring non-git user & character data | [`BACKUP.md`](BACKUP.md) |
| pob-mcp full setup, all env vars, troubleshooting | [`pob-mcp/README.md`](pob-mcp/README.md) |
| pob-mcp tool list (~123 tools) | [`pob-mcp/docs/TOOLS.md`](pob-mcp/docs/TOOLS.md) |
| poe-mcp-server setup and module architecture | [`poe-mcp-server/README.md`](poe-mcp-server/README.md) |
| poe-mcp-server tool list (~30 tools) | [`poe-mcp-server/TOOLS.md`](poe-mcp-server/TOOLS.md) |
| POEMCP setup | [`POEMCP/README.md`](POEMCP/README.md) |
| POEMCP tool list (13 tools) | [`POEMCP/TOOLS.md`](POEMCP/TOOLS.md) |
| PathOfBuilding API fork overview | [`PathOfBuilding/README.md`](PathOfBuilding/README.md) |
| PathOfBuilding Lua TCP action reference | [`PathOfBuilding/src/API/TOOLS.md`](PathOfBuilding/src/API/TOOLS.md) |
| Engineering decisions and bug history | [`pob-mcp/docs/DEVELOPMENT_HISTORY.md`](pob-mcp/docs/DEVELOPMENT_HISTORY.md) |
| Task playbooks (workflow definitions) | [`playbooks/`](playbooks/) |
