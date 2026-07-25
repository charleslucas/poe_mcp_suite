# RELEASING.md — how the suite and its components ship

## TL;DR — two release paths
**`poe-data-mcp` is published** to **PyPI + the MCP Registry** via a **tag-driven** GitHub Actions workflow
(push a `vX.Y.Z` tag → CI builds & publishes; no manual `twine`/token — PyPI trusted publishing via OIDC).
**Everything else runs from the local clone** — `.mcp.json` points each server at a local file, and the
**submodule forks are the unit of release** (push the fork + advance the suite pointer; no registry). So:
(a) `poe-data-mcp` → **tag it**; (b) all other components → **fork push**. `google-ai-mode-mcp` is third-party
(not ours). Companion docs: [`UPDATING.md`](UPDATING.md) (data-refresh cascade), [`INSTALL.md`](INSTALL.md) (setup).

## Component distribution map
| Component | Our repo (branch) | Lang | Ships as / "release" = | State |
|---|---|---|---|---|
| **pob-mcp** | `charleslucas/pob-mcp` (main) | TS/Node | git fork; run locally via `.mcp.json` (`node build/index.js`) | pkg `pob-mcp-server` **v1.0.0, NOT on npm** |
| **poe-data-mcp** | `charleslucas/poe-data-mcp` (main) | Python | **PUBLISHED — PyPI** (`uvx poe-data-mcp` / `pipx run`) + **MCP Registry**; this machine also runs it locally via `.mcp.json`. Release = **push a `vX.Y.Z` git tag** → `publish-mcp.yml` builds (`uv build`) + publishes to PyPI (trusted publishing/OIDC, no token) + MCP Registry + GitHub Release. The **tag** is the version (static `pyproject` version is ignored). | **v0.3.0 on PyPI** |
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

## Releasing `poe-data-mcp` (the one published package)
In the `poe-data-mcp/` submodule: move `[Unreleased]` CHANGELOG entries into a new `## [x.y.z] - YYYY-MM-DD`
section → commit + push `main` → `git tag vx.y.z && git push origin vx.y.z`. The tag triggers `publish-mcp.yml`
(PyPI trusted-publishing + MCP Registry + GitHub Release; the tag *is* the version). Then advance the suite
pointer. **Tagging = an irreversible public publish** — confirm the version + changelog first.

## Publishing the OTHER components (not set up — deliberate future task)
`poe-data-mcp` is the reference model. The rest aren't publishable yet:
- **pob-mcp → npm:** add a `bin` entry (so `npx pob-mcp-server` launches the server), a `files` whitelist (else
  the whole repo ships), **decide how the TCP-bridge Lua ships** (bundle `PathOfBuilding/src/API/*.lua` at pack
  time, or fetch it), an npm README, a version bump, and an `npx` smoke test. Never published (`pob-mcp-server` v1.0.0).
- **poe-trade-mcp → PyPI:** add packaging (no `pyproject.toml` yet) + a console-script entry point + the
  `mcp-name` PyPI marker, then copy `poe-data-mcp`'s `publish-mcp.yml` tag-driven flow.

## History
- **2026-07-25** — 3.29 (`Allflame`) import-handler fix released via the `PathOfBuilding` fork push
  (`b12d7df8b`; suite pointer `5ca9b5c`). Also refreshed the text lake + GGG tree exports to 3.29 (see
  `UPDATING.md`). Separately, **`poe-data-mcp` has a pending youtube fix** (`47cd8c4`) awaiting a `v0.3.1` tag.
