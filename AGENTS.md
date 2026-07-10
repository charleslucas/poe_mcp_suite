# poe_mcp_suite — Guide for AI Agents

This file is the vendor-neutral entry point for any MCP-compatible AI agent
(Cursor, Windsurf, Cline, Codex, Zed, Gemini CLI, custom agents, …). It routes
you to the shared, plain-Markdown resources in this repo. If you are **Claude
Code**, read [`CLAUDE.md`](CLAUDE.md) instead/as well — it adds Claude-specific
mechanics (auto-triggering skills, a SessionStart hook, memory) layered on top of
everything below.

## What this is

A collection of MCP servers that give an agent deep, live integration with Path
of Exile — build theory-crafting and passive-tree simulation via Path of
Building, trade/economy lookups, wiki and crafting data, and loot filters. Each
server runs independently; the tools are agent-agnostic by construction (standard
MCP). See [`README.md`](README.md) for the server/tool overview and
[`INSTALL.md`](INSTALL.md) for setup (submodules, dependencies, `.mcp.json`).

The current league name is in `.mcp.json` as `POE_LEAGUE`; pass it explicitly on
tool calls rather than trusting auto-detection when leagues run concurrently.

## How to work in this repo

The suite uses a lightweight workflow framework. It is described once, in
[`playbooks/README.md`](playbooks/README.md) — the shared meta-framework
(context management, league pre-flight, trust hierarchy, narration norms). Read
it before a substantial task, then the specific playbook that matches. **The
playbooks are ordinary Markdown — any agent can read and follow them directly**,
even without skill/rule auto-loading. Key ideas:

- **Cursory-vs-detailed gate** — decide up front whether a request is a quick
  lookup (answer directly) or a multi-source/multi-stage analysis (engage the
  matching playbook and pause for approval before pulling data).
  [`playbooks/README.md`](playbooks/README.md) §1.
- **Freshness discipline** — the game changes every patch, and model training
  data lags. For any patch-specific fact (mods, node stats, unique stats,
  prices, league specifics), prefer fetching authoritative data via the tools
  over answering from memory. Model-aware staleness index:
  [`reference_data/freshness_index.md`](reference_data/freshness_index.md).
- **Cached game data** lives in [`reference_data/`](reference_data/) (gitignored
  but its `README.md` is committed — read it on a fresh clone). Check it before
  re-fetching; respect the `fetched:`/`patch:`/`league:` frontmatter.
- **Per-character analyses** live in [`character_data/`](character_data/) (see
  its `README.md`). Read a character's file before working on it; append
  findings as you go.

## Non-negotiables

- **Legal boundaries** — before extracting, modifying, or redistributing any
  Path of Exile game data, read
  [`legal_considerations.md`](legal_considerations.md). Stay inside the
  conservative redistribution boundary it documents; if unsure, ask the user.
- **GGG trade API** — the official trade API carries Terms-of-Service risk.
  Brief the user and get explicit consent before using trade tools (see
  `legal_considerations.md` → "GGG Terms of Service").
- **Secrets** — `.mcp.json` and `POE_SESSION_ID` are sensitive (session cookie /
  account access). Never log or commit them.

## Contributing back

New or improved playbooks, reference data, and pitfalls are valuable to everyone
— see [`playbooks/README.md`](playbooks/README.md) for format conventions and
submission guidelines.
