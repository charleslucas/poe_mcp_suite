# poe_mcp_suite

A suite of [Model Context Protocol](https://modelcontextprotocol.io/) (MCP) servers that give Claude deep, live integration with Path of Exile — from build theory-crafting and passive tree simulation to trade, stash management, loot filters, and wiki lookups.

Each server runs independently and exposes a set of tools that Claude can call during conversation. Together they allow Claude to act as an informed PoE assistant: loading your actual build in Path of Building, simulating node choices, checking prices on poe.ninja, searching trade, scoring stash tab items, and more — all without leaving the chat.

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

## Quick Start

```bash
git clone --recurse-submodules https://github.com/charleslucas/poe_mcp_suite.git
```

Or if you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

Each server is configured independently — see the individual submodule READMEs for setup details, environment variables, and MCP client configuration.

To use `pob-mcp` in live mode, launch Path of Building via `pob-mcp/LaunchPoBWithAPI.bat` rather than the normal shortcut. This sets the environment variables that activate the TCP API server inside PoB.

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
