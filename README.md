# poe_mcp_suite

A collection of MCP (Model Context Protocol) servers for Path of Exile, designed to work together with Claude.

## Repositories

| Submodule | Description |
|-----------|-------------|
| [pob-mcp](pob-mcp/) | MCP server for Path of Building — build analysis, simulation, trade integration (~96 tools) |
| [poe-mcp-server](poe-mcp-server/) | MCP server for trade, stash, pricing, and loot filter editing (~30 tools) |
| [POEMCP](POEMCP/) | MCP server for wiki lookups, game data, and economy queries (13 tools) |
| [PathOfBuilding](PathOfBuilding/) | Fork of Path of Building with a TCP/stdio JSON-RPC API layer (branch: `api-stdio`) |

## Quick Start

```bash
git clone --recurse-submodules https://github.com/charleslucas/poe_mcp_suite.git
```

Or if you already cloned without `--recurse-submodules`:

```bash
git submodule update --init --recursive
```

## Configuration

Each server is configured independently. See the individual submodule READMEs for setup details.

The `pob-mcp` server connects to `PathOfBuilding` in TCP mode — launch PoB via `pob-mcp/LaunchPoBWithAPI.bat` to enable the live GUI connection.

## Tool Reference

Each submodule has a `TOOLS.md` listing all available tools:

- [pob-mcp/docs/TOOLS.md](pob-mcp/docs/TOOLS.md)
- [poe-mcp-server/TOOLS.md](poe-mcp-server/TOOLS.md)
- [POEMCP/TOOLS.md](POEMCP/TOOLS.md)
- [PathOfBuilding/src/API/TOOLS.md](PathOfBuilding/src/API/TOOLS.md)
