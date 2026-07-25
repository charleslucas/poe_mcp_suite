# RELEASING.md — how the suite and its components ship

## TL;DR — the suite is a git clone, not a published package
**Nothing we build is on npm or PyPI.** The suite runs from a **local clone**: `.mcp.json` points each MCP
server at a local file, and the **submodule forks are the unit of release**. "Releasing a change" = push the
relevant submodule fork, then advance the suite pointer (submodule-first ordering). No `npm publish` /
`twine upload` is involved today. Companion docs: [`UPDATING.md`](UPDATING.md) (data-refresh cascade),
[`INSTALL.md`](INSTALL.md) (first-time setup).

## Component distribution map
| Component | Our repo (branch) | Lang | Ships as / "release" = | State |
|---|---|---|---|---|
| **pob-mcp** | `charleslucas/pob-mcp` (main) | TS/Node | git fork; run locally via `.mcp.json` (`node build/index.js`) | pkg `pob-mcp-server` **v1.0.0, NOT on npm** |
| **poe-data-mcp** | `charleslucas/poe-data-mcp` (main) | Python | git fork; `python server.py` | has `pyproject.toml`; **NOT on PyPI** |
| **poe-trade-mcp** | `charleslucas/poe-trade-mcp` (master) | Python | git fork; `python poe_all.py` | no packaging files; **NOT on PyPI** |
| **PathOfBuilding** | `charleslucas/PathOfBuilding` (api-stdio) | Lua | **git fork push** — this is where pob-mcp's *runtime* Lua (`src/API/{Handlers,BuildOps,TcpServer}.lua`) actually releases; it reaches the user's PoB via `pob-mcp/InstallTcpApi.ps1` (run by `LaunchPoBWithAPI.bat`) | e.g. the 2026-07-25 3.29 import fix shipped here |
| **skilltree / atlastree** | `charleslucas/poe-{skilltree,atlastree}-export` (master) | data | git fork push (GGG mirror — see `UPDATING.md`) | tracks GGG releases |

## Third-party deps — NOT ours, never "release" these
- **`google-ai-mode-mcp`** (npm; maintainer `pleaseprompto <hello@geromedexheimer.de>`) — the Google-AI-Mode
  search server, consumed via `npx google-ai-mode-mcp@latest` in `.mcp.json`. **We only use it.** This is the
  package most likely to be mistaken for "our npm release" — it is **not** ours; we can't and shouldn't publish it.

## The release procedure (git-based, today)
1. Commit + **push the submodule fork FIRST**. Branches differ: `PathOfBuilding`=`api-stdio`, `poe-data-mcp`=`main`,
   `poe-trade-mcp`=`master`, `pob-mcp`=`main`, tree exports=`master`.
2. **Advance the suite pointer:** in the suite, `git add <submodule> && git commit && git push`.
3. The tracked `.githooks/pre-push` hook guards the ordering (submodule commit must exist on its fork first).
4. **Runtime Lua** (`PathOfBuilding/src/API/*`) additionally requires the user to **re-run `InstallTcpApi.ps1`**
   (via `LaunchPoBWithAPI.bat`) and relaunch PoB — pushing the fork alone doesn't update a running PoB install.

That's the entire "release" today. There is no registry publish step.

## If we ever want to publish to npm / PyPI (deliberate future project — NOT set up)
Publishing is permanent; treat it as its own scoped task with explicit go-ahead + registry auth. Current gaps:
- **pob-mcp → npm:** add a `bin` entry (so `npx pob-mcp-server` launches the server), a `files` whitelist (else
  the whole repo ships), **decide how the TCP-bridge Lua ships** — bundle `PathOfBuilding/src/API/*.lua` into the
  package at pack time, or fetch it — plus an npm-facing README, a version bump, and an end-to-end `npx` smoke test.
- **poe-data-mcp / poe-trade-mcp → PyPI:** complete packaging (poe-trade-mcp has none), console-script entry
  points, version, then `python -m build` + `twine upload`.

## History
- **2026-07-25** — 3.29 (`Allflame`) import-handler fix released via the `PathOfBuilding` fork push
  (`b12d7df8b`; suite pointer `5ca9b5c`). Also refreshed the text lake + GGG tree exports to 3.29 (see
  `UPDATING.md`). **No npm/PyPI publish** (none is set up; see above).
