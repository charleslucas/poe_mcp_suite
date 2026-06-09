# Playbook: League Transition

For Claude sessions when a PoE temp/challenge league is ending or has just ended, or when a new league has just launched. PoE leagues run ~3 months; at the boundary, characters and items migrate to permanent leagues (see the user's notes below) and a fresh league launches with new mechanics.

Use this playbook when:

- The user says "the league is ending" / "I want to prep for the new league" / "Mirage is over, what do I update?"
- `get_active_leagues` shows ⚠ POE_LEAGUE points to a league no longer active
- A new league has just launched and `reference_data/leagues/{new-league}.md` doesn't exist yet

This is a checklist, not an analysis. No triage step — just walk the list in order.

---

## What actually happens at league end (background)

From the user's notes:

- **Characters** move to the parent (permanent) league: softcore challenge → Standard; hardcore challenge → Hardcore. They keep their name, level, gear, and tree — only the `league` field changes.
- **Stash tabs** become "remove-only" in the permanent league. Items can be removed but not added. League-specific currency/items either move to core or get deleted/converted (check GGG's end-of-league post).
- **Atlas progress** merges with the permanent league's atlas — game keeps the higher completion bonus per node. Master progress (Einhar, Jun, Alva, Niko) also merges.
- **New league** requires a brand-new character on a fresh economy. Old characters stay in the permanent leagues forever.

The mapping the suite uses (in `pob-mcp/src/services/leagueResolver.ts`):

| Temp league pattern | Parent (where characters go on end) |
|---|---|
| `Mirage` (softcore challenge) | `Standard` |
| `Hardcore Mirage` | `Hardcore` |
| `SSF Mirage` | `SSF Standard` |
| `Hardcore SSF Mirage` | `SSF Hardcore` |

The heuristic matches on the words "Hardcore", "SSF", "Ruthless" in the league name. Cross-check at transition time against `get_active_leagues` — GGG occasionally tweaks naming.

---

## Step 0 — Frame the work

One sentence: *"Walking the league-transition checklist for [league] → [parent]. I'll update the env var, character meta files, and per-league docs in order."*

If unsure whether a transition has actually happened yet, run `mcp__pob__get_active_leagues` first. The ⚠ warning is the unambiguous signal.

---

## Step 1 — Confirm transition state

| # | Check | How | Action |
|---|---|---|---|
| 1.1 | What does `POE_LEAGUE` currently say? | Read `.mcp.json` | Note current value (e.g., "Mirage") |
| 1.2 | Is that league still active? | `mcp__pob__get_active_leagues` | If ⚠ present → transition has happened. If still active → too early, stop. |
| 1.3 | What's the parent league? | Tool output reports it | Note for Step 2 (e.g., "Standard") |
| 1.4 | Is the new league live yet? | Tool's temp-league list | If a new challenge league appears, note its name for Step 4 |

If 1.2 shows ⚠ but the user hasn't decided to migrate yet (e.g., they're still using Mirage stash before remove-only kicks in), pause and ask. Don't update the env var until they're ready to switch their default queries to the permanent league.

---

## Step 2 — Update env var

Edit `.mcp.json` and replace `POE_LEAGUE` with the parent league name. Use the value from `get_active_leagues` rather than guessing — GGG's naming for HC/SSF variants has shifted across patches.

```jsonc
"env": {
  "POE_LEAGUE": "Standard",  // was: "Mirage"
  ...
}
```

After editing, the user must **restart Claude Code fully** (close, reopen) so the MCP server subprocess respawns with the new env. A `/reload` of just Claude doesn't reload MCP env vars.

Sanity-check by re-running `mcp__pob__get_active_leagues` — the warning should be gone.

---

## Step 3 — Update character meta files

Every character in `character_data/{Account}/{League}/{Character}/meta.json` whose `league` field matches the old temp league needs updating. Reading the file first is fine; use `Edit` to change just the league field rather than rewriting the whole JSON.

```bash
# Find affected characters
Glob character_data/**/meta.json
# For each, check the `league` field, update if it matches the old league
```

After the update, the character itself is unchanged — same level, same gear, same tree. Only the `league` field reflects where she lives now. Add a journal entry noting the transition:

```markdown
## 2026-XX-XX  League transition

- Mirage league ended; character migrated to Standard.
- Stash tabs from Mirage are now remove-only on Standard.
- Updated `meta.json` league: Mirage → Standard.
```

---

## Step 4 — Bootstrap the new league (if one launched)

When a fresh league launches, generate the per-league reference doc so future sessions don't re-fetch the wiki:

1. Note the new league's name from `get_active_leagues` (e.g., "Settlers").
2. Generate `reference_data/leagues/Settlers.md` via a sub-agent (see `playbooks/README.md` §6) that fetches `https://www.poewiki.net/wiki/Settlers_league`, summarizes drop tables / unique items / mechanic specifics, and writes the cache. Don't pull the raw wiki page into main context.
3. Update `POE_LEAGUE` in `.mcp.json` to the new league name *only if* the user is creating a character there. If they're staying in Standard, leave POE_LEAGUE alone.
4. Restart Claude Code so the env var change takes effect.

Once a character is created and imported via `lua_import_character`, follow the standard post-import checklist (see `pob-mcp/CLAUDE.md` → "After lua_import_character"): ask about bandits, quest passives, pantheon.

---

## Step 5 — Invalidate cached price data

Trade and ninja results are cached per-league. After updating `POE_LEAGUE`:

- Trade cache TTL is 1 hour ([tradeClient.ts](../pob-mcp/src/services/tradeClient.ts)) — expires naturally.
- ninja cache lives in `poeNinjaClient` — same TTL.
- Cached stash tab listings from `poe-mcp-server` may still reference the old league name; the next `list_tabs` call refreshes them against the new default.

Nothing to manually invalidate; just be aware that the *first* price lookup after the switch may take a moment longer than usual while caches warm.

---

## Step 6 — Audit per-league reference docs

`reference_data/leagues/Mirage.md` (and any other ended-league files) are now historical. Leave them in place — they're useful for "what did Mirage have, again?" questions. Don't delete; just don't load them as current-league context anymore.

The `playbooks/README.md` §2b directive says to load `reference_data/leagues/{current-league}.md` — once `POE_LEAGUE` is updated, that resolves to the new file automatically. No code change needed.

---

## Done table

When the checklist is complete, report:

| Item | Status |
|---|---|
| `POE_LEAGUE` updated | ✓ / pending |
| Claude Code restarted | ✓ / pending — required for MCP subprocess to pick up env change |
| Character meta files updated | ✓ N/A (no affected characters) |
| New-league reference doc created | ✓ / N/A (no new league live yet) |
| `get_active_leagues` shows no ⚠ | ✓ / ⚠ persists (investigate) |

---

## Pitfalls

- **Don't update `POE_LEAGUE` before the user is ready to act on Standard prices.** Once flipped, the trade tools query Standard by default. If the user is still trying to liquidate Mirage stash, leave it pointing at Mirage until they're done.
- **Hardcore characters go to Hardcore, not Standard.** If the user runs HC, double-check `get_active_leagues`'s parent column — don't assume "Standard" for everything.
- **Restart Claude Code, not just `/reload`.** MCP servers are subprocesses spawned at session start. Env-var changes need a full process restart.
- **PoB submodule updates are NOT aligned with league boundaries.** PoB updates on patches (~weekly during a league, irregular otherwise). Don't expect a league transition to also bring a tree/mod update.
