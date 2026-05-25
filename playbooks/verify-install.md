# Playbook: Verify Install

For Claude sessions where the user wants to confirm the suite is correctly installed and all four MCP servers are healthy. Run after any of:

- Fresh `git clone --recurse-submodules` of `poe_mcp_suite`
- `git pull` + `git submodule update --remote --recursive`
- Touching `.mcp.json`, env vars, or relaunching the MCP client
- A regression fix landing in any submodule (e.g., the MapStash crash fix in `poe-mcp-server`)
- The user says "verify the install" or "run the test suite"

This is a deterministic checklist, not an analysis task — no triage step. Run every test, report a green/red table at the end, and stop *before* any destructive cleanup (the user might keep older standalones around for comparison).

---

## Step 0 — Frame the work for the user

One sentence: *"Running the install verification suite — I'll exercise each of the four MCP servers in turn and report a green/red table at the end."*

Narrate per tier (see CLAUDE.md → "Notes for Claude" → narration bullet). If a test fails, say *which* server failed and *what the failure means* before moving on — do not silently continue.

If a tier's prerequisite isn't met (e.g., PoB isn't running for Tier 4), report it as "skipped — prerequisite missing" rather than "failed." Then ask the user whether to wait for them to fix the prereq (e.g., launch PoB) or move on.

---

## Step 1 — Tier 1: File system and config (no MCP calls)

Run these via `Bash` / `Read` / `Glob`. They catch broken installs before any MCP call is made.

| # | Check | Tool / command | Pass criteria |
|---|---|---|---|
| 1.1 | `.mcp.json` exists in suite root | `Read .mcp.json` | File exists; contains `pob`, `poe`, `poemcp` keys under `mcpServers` |
| 1.2 | All submodules populated | `Glob */README.md` | Returns matches for `pob-mcp/`, `poe-mcp-server/`, `POEMCP/`, `PathOfBuilding/` |
| 1.3 | `pob-mcp` built | `Glob pob-mcp/build/index.js` | One match (means `npm run build` was run) |
| 1.4 | PoB API files installed | `Glob "$env:APPDATA/Path of Building Community/API/*.lua"` (Windows) | Three matches: `TcpServer.lua`, `Handlers.lua`, `BuildOps.lua` |
| 1.5 | `reference_data/` set up | `Glob reference_data/skilltree/data.json`, `Glob reference_data/atlastree/data.json` | One match each (GGG repos cloned per `reference_data/README.md`) |

A failure in any 1.x check usually means an install step from `CLAUDE.md` was skipped. Cite the specific step number (e.g., "Step 2 — Install pob-mcp") so the user knows where to resume.

---

## Step 2 — Tier 2: POEMCP server (no credentials)

POEMCP needs no auth, so it's the cheapest server to validate. If this tier fails, the Python install (`pip install -e .` in `POEMCP/`) is broken.

| # | Test | Tool call | Pass criteria |
|---|---|---|---|
| 2.1 | Server alive + ninja API reachable | `mcp__poemcp__currency_overview` (no args) | Returns a currency table with Chaos values |
| 2.2 | Wiki/poedb scraping works | `mcp__poemcp__get_item_detail` with `item_name: "Headhunter"` | Returns mod text mentioning rare monsters / buffs |
| 2.3 | Gem search works | `mcp__poemcp__search_gem` with `query: "Spark"` | Returns at least one gem with `name` matching `Spark` |

---

## Step 3 — Tier 3: poe-mcp-server (needs POE_SESSION_ID)

If the session cookie is expired, every test here fails with 401/403. If only Tier 3 fails (Tiers 2 and 4 pass), suspect the cookie before the install.

| # | Test | Tool call | Pass criteria |
|---|---|---|---|
| 3.1 | Auth + stash listing works | `mcp__poe__list_tabs` | Returns an array of tab objects with `index`, `name`, `type` |
| 3.2 | **MapStash regression test** | `mcp__poe__get_tab` with `tab_index: 3` (or whichever index has `type: "MapStash"` from 3.1) | Returns `{count, items}` *without* a crash. Empty `items` is fine — the historical bug was an exception, not zero items |
| 3.3 | Ninja lookup works | `mcp__poe__ninja_lookup` with `name: "Mirror of Kalandra"` | Returns a price in chaos |
| 3.4 | Character API works | `mcp__poe__get_character` with `character_name: <any char on the account>` | Returns class, level, and equipped item list |

If the account has no MapStash tab, skip 3.2 and note it — but flag that the regression test wasn't exercised.

---

## Step 4 — Tier 4: pob-mcp (needs PoB GUI running)

**Prerequisite:** PoB must be running via `pob-mcp\LaunchPoBWithAPI.bat` (not the normal shortcut). If `Test-Connection 127.0.0.1 -Port 59166` fails or the next test errors with `ECONNREFUSED`, ask the user to launch PoB before continuing.

| # | Test | Tool call | Pass criteria |
|---|---|---|---|
| 4.1 | TCP connection to PoB GUI | `mcp__pob__lua_get_build_info` | Returns build name, level, class, ascendancy. No `ECONNREFUSED` |
| 4.2 | Calc engine works | `mcp__pob__lua_get_stats` (no args) | Returns stat object including `TotalDPS`, `Life`, `EnergyShield` |
| 4.3 | Character list works | `mcp__pob__lua_list_characters` (no args) | Returns array of characters for the account |
| 4.4 | GGG league API works | `mcp__pob__get_leagues` | Returns current league list including `Standard` and the active temp league |

If 4.1 fails but PoB is running, the most common cause is the Main.lua patch was overwritten by a PoB update — relaunch via the batch file (it self-heals).

---

## Step 5 — Output shape

End the run with a single summary table the user can scan at a glance:

```
Tier 1 (Filesystem)   ✅ 5/5
Tier 2 (POEMCP)        ✅ 3/3
Tier 3 (poe-mcp)       ✅ 4/4   ← MapStash regression: passed
Tier 4 (pob-mcp)       ⚠ 0/4   ← skipped: PoB GUI not running
```

For any red row, follow with one short paragraph: which test failed, what the failure means, and the next action (usually "re-run Step N of CLAUDE.md" or "check the env var X"). Don't dump raw error output unless the user asks.

If everything green: state explicitly *"All four servers are healthy — safe to proceed with normal work."* Don't bury the headline.

---

## Step 6 — Pitfalls

Concrete lessons from prior verification sessions. Add to this list when a new failure mode surfaces.

**Path / install pitfalls**
- A stale standalone clone of `pob-mcp` / `poe-mcp-server` / `POEMCP` elsewhere on disk can mask a suite install: if `.mcp.json` still points at the old paths, you're testing the wrong copy. Confirm the `args:` paths in `.mcp.json` resolve into `poe_mcp_suite/` before trusting any green result.
- After a PoB update, `Modules\Main.lua` loses its TCP patch. `LaunchPoBWithAPI.bat` self-heals — but only on next launch. If PoB is already open and 4.1 fails, the user has to close it and relaunch via the batch file.
- `npm run build` in `pob-mcp/` is easy to forget after a submodule pull. Check 1.3 catches this — if it fails, run `cd pob-mcp && npm install && npm run build`.

**MCP client pitfalls**
- Tool schemas are loaded lazily in Claude Code. The first call to any `mcp__*` tool can return `InputValidationError` if the schema hasn't been fetched yet — use `ToolSearch` with `select:<tool_name>` to load the schema before the test call. This is a tooling quirk, not an install failure.
- `mcp__poemcp__get_leagues` does NOT exist (despite the name suggesting parity with `mcp__pob__get_leagues`). Use `currency_overview` to verify POEMCP is alive.

**Credential pitfalls**
- `POE_SESSION_ID` cookies expire silently. A 401/403 on every Tier 3 test points at the cookie, not the install. The fix is reauth in a browser and updating `.mcp.json` — do NOT log the cookie value when diagnosing.
- `POE_ACCOUNT_NAME` must include the discriminator (`Account#1234`). Missing `#NNNN` causes `get_character` to fail without a clear error.

**Regression-test pitfalls**
- 3.2 (MapStash) passing means the *exception* is gone — it does NOT mean the items are being returned correctly. If the user reports the tab "looks empty" after a green 3.2, that's a separate bug from the original crash. Treat the two failure modes distinctly.

---

## When to extend this playbook

Add a new test whenever:

- A regression fix lands that's worth keeping a permanent check for (the MapStash test is the model — name it explicitly in the table so future Claudes don't optimize it away)
- A new MCP server is added to the suite (add a new Tier)
- A new env var becomes required (add a Tier 1 check that verifies it's set)
- A user hits a failure mode that the current suite missed (capture in Step 6 *and* add the test that would have caught it)

When you extend, also update the entry in [`playbooks/README.md`](README.md) so the playbook stays discoverable.
