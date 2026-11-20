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

- **Never add a mod or stat "just in case".** Gear advice and item templates
  carry exactly what the build demands and nothing else: attributes only when
  PoB's requirement panel shows the character is short, resistances only in the
  elements that are actually below cap, suffixes that answer a reported gap.
  An empty suffix stays empty. Every invented filler mod (unneeded attribute,
  redundant resistance, "nice to have" regen) makes the item worse and, when it
  later reaches the build, hides the real cost behind noise.
- **Read numbers from PoB, do not recompute them.** Attribute requirements
  (`Str/Dex/Int Required`), resistances (`Current output value`), and gaps
  (build issues) are already calculated by the tool. Quote them; do not sum
  sources by hand — hand arithmetic over breakdown output has produced wrong
  requirements (a gem level read out of context) and wrong resistance bases.
- **Legal boundaries** — before extracting, modifying, or redistributing any
  Path of Exile game data, read
  [`legal_considerations.md`](legal_considerations.md). Stay inside the
  conservative redistribution boundary it documents; if unsure, ask the user.
- **GGG trade API** — the official trade API carries Terms-of-Service risk.
  Brief the user and get explicit consent before using trade tools (see
  `legal_considerations.md` → "GGG Terms of Service").
- **Trade links cost nothing; trade searches do.** A trade search URL is just
  `gzip(query)` → base64url of the bare query object (Path of Building does this
  locally in `TradeQuery.lua:1142`). `generate_trade_url` builds one with **zero
  API requests** (`use_api: true` opts into a server-issued id instead). Reserve
  `search_trade_items` / `search_trade_listings` for when a count or real prices
  are unavoidable, never loop them over mod variations, and check
  `trade_rate_limit` first. The limit is per IP and shared across every tool: a
  single careless burst blocks all searches for a minute or more.
- **Never retype a payload by hand.** "The search is no longer valid" has three
  known causes: a payload wrapped as `{ query, sort }` (the URL carries the bare
  query only), a query with no filters at all, and — most often in practice — a
  *corrupted copy* of a valid URL (one dropped `a`, one `HAoOx` → `HgQOx`, and the
  base64 decodes to garbage). Write links to a file and verify each with
  `decode_trade_url` (or `zlib.gunzipSync` of the base64url payload) before
  handing them over.
- **Secrets** — `.mcp.json` and `POE_SESSION_ID` are sensitive (session cookie /
  account access). Never log or commit them.

## Contributing back

New or improved playbooks, reference data, and pitfalls are valuable to everyone
— see [`playbooks/README.md`](playbooks/README.md) for format conventions and
submission guidelines.
