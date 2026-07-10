# Issues — poe_mcp_suite

Cross-cutting issue tracker for the whole suite (pob-mcp, poe-mcp-server, POEMCP, the PathOfBuilding fork, skills/playbooks, Claude integration). Lives at the top level rather than per-subdir because most issues touch multiple components or are easier to triage in one place.

**Entry format:** short title (`### ...`), 1–3 sentence description, a **Repro:** line where applicable, and a single-line **Affects:** scope. Move resolved entries to the *Closed* section at the bottom with a one-line note.

**For roadmap / feature work** (open items, deliberately-not-doing decisions, completed roadmap), see [`pob-mcp/TODO.md`](pob-mcp/TODO.md). This file is for *bug-style* issues and behavioral surprises — things that are broken, misleading, or under-investigated, not features-we-haven't-built-yet.

---

## Open — tool quality / bugs

### `.xml` extension mismatch across file-based tools

`lua_save_build` and `snapshot_build` write the build file **with** the `.xml` suffix. But `analyze_skill_links`, `suggest_support_gems`, and `restore_snapshot`, when called with the bare build name, try to open it **without** `.xml` and fail with `ENOENT: no such file or directory, open '...\Builds\<name>'`. Workaround: pass `build_name` with the `.xml` explicitly. Fix: normalize the suffix consistently across all file-based handlers.

**Repro (2026-05-29):** `lua_save_build("Mirage-MirageSixFingeredMan-Analysis")` wrote `Mirage-MirageSixFingeredMan-Analysis.xml`. Same `build_name` passed to `analyze_skill_links` and `restore_snapshot` errored on the suffix-less path; passing `"Mirage-MirageSixFingeredMan-Analysis.xml"` worked for `restore_snapshot`.
**Affects:** pob-mcp `analyze_skill_links`, `suggest_support_gems`, `restore_snapshot` (and likely other file-based handlers).

### `analyze_skill_links` / `suggest_support_gems` are file-only (no TCP path)

Both read from the saved build XML, not the live in-memory PoB state. Per `pob-mcp/CLAUDE.md`'s TCP-first principle, they should prefer TCP (read gems from the live build) and fall back to file only when TCP is unavailable. As-is, they require a manual `lua_save_build` first and can read stale data if the GUI has unsaved changes.

**Affects:** pob-mcp gem-analysis handlers — anything that needs the current 6-link without saving first.

### `get_skill_setup` doesn't list support gems

Returns active skills per group but omits support gems. To see the actual 6-link in the 2026-05-29 gem-sim session we had to grep `<Gem ` lines out of the saved XML. Including supports (with their level / quality / enabled state) in the output would make this a one-call read.

**Affects:** pob-mcp `get_skill_setup` — any workflow that wants to inspect the current link without going to XML.

### `export_build_summary` Main Skill field blank

For the live build, the generated markdown summary showed `**Main:** ` with nothing after it. Other fields (Life, DPS, EHP, resists, block, armour, evasion) were populated correctly. Likely fails to read the active main skill name from live TCP state.

**Repro (2026-05-29):** `export_build_summary` on the live `Mirage-MirageSixFingeredMan-Analysis` session — Main Skill row blank despite Cyclone + Void Shockwave being the active main skill (visible in `get_skill_setup`).
**Affects:** pob-mcp `export_build_summary`.

### `get_build_issues` phantom-empty-jewel-socket count

Reported `47 jewel socket(s) empty` when the user had every *reachable* allocated socket filled with a real jewel. The count was tallying unallocated jewel-socket *nodes* across the entire tree, not allocated-but-empty sockets. Misleading and creates noise in the issues output. Fix: only flag sockets that are both allocated and empty.

**Repro (2026-05-29):** `get_build_issues` on MirageSixFingeredMan listed 47 jewel IDs as empty (Jewel 2311, Jewel 3109, …) — the actual allocated jewel sockets all had jewels.
**Affects:** pob-mcp `get_build_issues`.

### Baseline instability across `remove_gem` + `add_gem` + reload

Between two sims in the same socket group, Speed jumped 1.49 → 1.70 attacks/sec with no apparent cause, and the new value persisted through `restore_snapshot` + `lua_reload_build`. Some PoB config flag or buff state appears to toggle on gem operations and not reset cleanly on reload. Makes A/B sims non-apples-to-apples without identifying which flag flips.

**Repro (2026-05-29):** baseline Speed 1.49; after `remove_gem(group=5, gem=4)` + `add_gem(group=5, "Increased Critical Damage")` + revert via snapshot restore + reload, Speed read 1.70. AverageDamage / CritMulti / HitChance unchanged across the same operations — only Speed flipped.
**Affects:** any gem-sim workflow that compares DPS before/after.

---

## Open — Claude.ai web integration

### HTTP/SSE transport not implemented — servers are stdio-only

All three MCP servers (pob-mcp, poe-mcp-server, POEMCP) currently use stdio transport, which works for Claude Code (subprocess model) but not Claude.ai web (which requires HTTP/SSE transport + a publicly accessible URL).

**Remaining work per server:**

- **POEMCP** (easiest): Uses `FastMCP` which already supports `mcp.run(transport="sse", port=...)`. Change `server.py` to accept a `--transport sse --port N` flag. ~10 lines.
- **poe-mcp-server**: `mcp_server_utils.py` shim hardcodes `stdio_server()` and ignores the port arg. Replace with SSE transport when a `--http` flag is passed. ~20 lines. Each sub-server or `poe_all.py` needs to accept the flag.
- **pob-mcp** (most work): Node.js MCP SDK has `SSEServerTransport` available but it's not wired in. Need a `--http --port N` startup mode that starts `SSEServerTransport` instead of `StdioServerTransport`. ~50 lines.

**Intended user experience once done:**
1. Start servers in HTTP mode
2. Run `cloudflared tunnel --url http://localhost:PORT` for each server (free, no account)
3. Add the tunnel URLs to Claude.ai Settings → Integrations
4. Full tool access from Claude.ai web, with credentials staying local

See `INSTALL.md` → "Step 6 (optional)" for the full intended setup guide.

**Note:** This preserves the git/PR contribution model. Each user runs their own instance; no shared server is needed. The playbooks and CLAUDE.md remain in the repo as before.

---

## Open — stash API access

### Stash scanning blocked: GGG disabled legacy character-window stash endpoint

`list_tabs`, `get_tab`, and `scan_stash_tabs` use `poe_lib.py`'s two-path design:
1. **OAuth** (if `client_id` + tokens): hits `api.pathofexile.com/stash/{league}` — requires developer app registration
2. **POESESSID fallback**: hits `character-window/get-stash-items` — returns **HTTP 403 Forbidden (code 6)**

GGG has shut down the legacy `character-window/get-stash-items` endpoint for stash access while keeping `character-window/get-items` (character equipment) alive. The fallback code is correct but the endpoint it targets is no longer accepting requests.

**The only working path** is OAuth registration at `pathofexile.com/developer`, which is designed for public-facing applications and is onerous for a personal tool (full review process, requires justification for each scope).

**Impact:** `price_tab` and `scan_stash_tabs` are blocked — these are cache-read-only tools (no GGG calls during pricing) but can't populate their cache without a working `get_tab`. The stash scanning workflow cannot be used or playbookeduntil this is resolved.

**Possible directions:**
- Accept the limitation: stash scanning requires developer OAuth registration
- Investigate if GGG's public stash stream (`/api/public-stash-tabs`) offers an alternative path (public listings only, not your own stash)
- Document the stash scanning workflow anyway (what it would do) so it's ready when OAuth is eventually set up

**Repro (2026-06-04):** `list_tabs` → `HTTP 403: {"error":{"code":6,"message":"Forbidden"}}` despite valid POESESSID in env. Character endpoints (`get-items`) work fine with the same POESESSID.

---

## Open — data persistence

### Hand-curated knowledge in gitignored caches doesn't survive a fresh clone

`reference_data/` and `character_data/` are both gitignored, treated as regenerable per-machine caches:

- `reference_data/` is meant to regenerate from poewiki + GGG patch notes + GGG repo submodules (skilltree, atlastree). README documents the regen path.
- `character_data/` is a junction to `%APPDATA%/poe_claude_data/` (Windows) — per-machine user state, never intended to be committed.

Two kinds of content have crept into these dirs that **are not regenerable** from any wiki fetch or import:

1. **FRESHNESS CHECKLIST entries in `reference_data/leagues/<league>.md`** — hand-curated "this patch's mechanic diverges from Claude's pre-2024 knowledge" notes. Example added 2026-05-29: *The Unseen Hand (Nameless bloodline) grants a 3rd ring slot in 3.28 Mirage.* A regen from poewiki re-fetches the league mechanic content but loses these curated divergences. The whole point of the checklist is durable freshness support across sessions, so losing it on reclone defeats the design.
2. **`character_data/<Account>/<League>/<Character>/build.md`** — per-character upgrade plans, gap analyses, decision rationale, deferred follow-ups. Built up across multiple sessions. Exists only in the user's `%APPDATA%`. A fresh clone, a different machine, or a wiped junction has zero of it. Same for the per-character journal entries.

Both kinds of content are human/Claude-authored *analysis*, not cache data. They survive only as long as the local `%APPDATA%` and the local `reference_data/` survive — not across reclones, machine swaps, or repo sharing.

**Possible directions** (no decision yet):
- Carve out a committed sibling for the durable parts — e.g. `reference_data/divergences/<league>.md` *not* in `.gitignore`, while keeping the regenerable mechanic data ignored. Same shape for per-character: commit a slim `character_data/notes/` while keeping bulky imports/snapshots/buffers ignored.
- Accept the loss and require active sessions to repopulate by re-importing characters and re-running the freshness check from scratch.
- A hybrid: auto-export the durable parts to a committed `KNOWLEDGE.md` (or per-area files) on a hook / periodic basis, treating the gitignored caches as authoritative working state.

**Affects:** any session that depends on prior cross-session knowledge accumulation — most notably the freshness-check axis (defeats its own purpose if the curated entries vanish), and per-character build planning continuity.

---

### ~~Non-affiliation notice missing from trade tool outputs~~ ✅ Fixed 2026-05-31

Added `NON_AFFILIATION_NOTICE` constant to `poe_trade.py`; included in JSON output of `search_trade`, `search_by_item_mods`, and `fetch_listing`. pob-mcp tools already had it added earlier the same day.

---

### ~~`poe-mcp-server` trade tools lack Bottleneck-style rate limiting~~ ✅ Improved 2026-05-31

`poe_trade.py` now parses `X-Rate-Limit-Ip`/`X-Rate-Limit-Account`/`X-Rate-Limit-Client` response headers and dynamically adjusts the inter-request interval (with 25% safety margin). Also uses `Retry-After` header value on 429 responses instead of fixed wait times. Floor remains 1.5s. Cross-process coordination with pob-mcp's Bottleneck limiter is still not possible (separate processes), but the header-driven approach means each process self-tunes to GGG's actual observed limits.

---

## Open — PoB calc behavior

### Trinity Support resonance not modeled in default calc

Leveling Trinity 1 → 20 in a Cyclone + Void Shockwave conversion build produced **0 DPS change** in PoB's calc (TotalDPS identical to one significant figure across multiple reads). Either PoB requires an explicit Resonance config toggle that isn't on by default, or its calc doesn't simulate the resonance build-up at all (Trinity's effect is per-hit-accumulated, which static stat calcs may not capture).

Worth confirming the true state — search PoB's calc config UI for Trinity/Resonance options, or trace `Trinity` references in `Calcs/`. If PoB genuinely doesn't model it, document in our wrapper docs (`get_stat_breakdown`, `get_calc_breakdown`, `suggest_support_gems`) so we don't recommend leveling Trinity expecting a measurable PoB number.

**Repro (2026-05-29):** Trinity at level 1 in MirageSixFingeredMan's main 6-link. `set_gem_level(group=5, gem=6, level=20)` → no change to TotalDPS, AverageDamage, CritMulti, or any other offense stat read via `lua_get_stats`.
**Affects:** DPS analysis of conversion / multi-element builds that use Trinity Support.

---

## Open — hook integration

### Tiered context-usage hooks (80% / 90%) + debug the 70% hook

`get_context_usage` (pob-mcp) is wired to a `PreToolUse` warning hook at 70% in `.claude/settings.json`. User flagged that the 70% hook may not be firing reliably, and asked about adding additional tiers at **80%** and **90%** for escalating urgency.

Tasks:
1. Reproduce the 70% hook miss — check whether the hook's gating condition is correct, whether `get_context_usage` returns timely data on every tool call, and whether there are race conditions when many tools fire in parallel.
2. Add 80% and 90% tier hooks with progressively stronger language (e.g. "consider compacting" → "compact recommended" → "compact now — context is critical").
3. Verify all three fire at the correct thresholds during a deliberately context-heavy session.

**Affects:** session ergonomics — without reliable hooks, the model has to self-poll `get_context_usage` and may miss the compact window.

---

## Closed

*(none yet — move resolved entries here with the resolution commit / PR / date.)*
