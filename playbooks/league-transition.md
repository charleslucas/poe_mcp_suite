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

## Event leagues — a recurring, lighter variant of this transition

Per the [wiki](https://www.poewiki.net/wiki/League), *temporary* leagues come in two recurring flavours:
**challenge leagues** (the ~13–16-week **expansion** leagues this checklist is built for) and **event leagues**
(shorter, also recurring — e.g. **Legacy of Phrecia / Return of the Ancestors**, races, Mayhem, Endless Delve).
Event leagues happen regularly (often between or running alongside expansions), so treat them as a normal,
repeating part of the cycle — not a one-off. Handle one as a *lightweight* version of this checklist:

- **Usually DON'T flip `POE_LEAGUE`** to the event — events have thin/separate economies; typically keep
  `POE_LEAGUE` on the main challenge league unless the user is actively trading in the event.
- **Cache it** in `reference_data/leagues/{event}.md` (Step 4 sub-agent) and **scope its mechanics `event-only`**
  in `reference_data/mechanics_index.md` (they vanish when the event ends — re-scope at event end).
- **Characters** are fresh-start for the event and migrate to **Standard or Void** at its end (not necessarily
  the current challenge league's parent). Update their `meta.json` league at end like any transition.
- Event characters use the normal `character_data/{Account}/{EventLeague}/{Character}/` layout. ⚠ Alternate
  ascendancies / event tech may not be modelled by mainline PoB's **default** tree — but check for a
  **"3.XX (alternate)" tree version** first (PoB ships `TreeData/3_XX_alternate/` for Phrecian-style events;
  switching the imported spec's tree version enables the alternate ascendancies — discovered 2026-07-09,
  details in `leagues/return_of_the_ancestors.md` → Tooling). Don't conclude "PoB can't model it" from the
  default tree alone.

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
3. **Generate index entries for the new mechanics** (same sub-agent or a second one). Enumerate from the wiki `Version_X.Y.0` page ("New Content and Features" section) plus the league page, cross-checked against the canonical lifecycle list at [`League_mechanics`](https://www.poewiki.net/wiki/League_mechanics) (every mechanic, active and removed). For each new mechanic: add a patch-keyed entry to `freshness_index.md` and a scope-tagged row (`challenge-league` until GGG cores it) to `mechanics_index.md`. Also record any removals/reworks the notes announce (removals break assumptions as hard as additions). Community-survey is for consensus *later*, not enumeration — the wiki pages are the enumeration source.
4. Update `POE_LEAGUE` in `.mcp.json` to the new league name *only if* the user is creating a character there. If they're staying in Standard, leave POE_LEAGUE alone.
5. Restart Claude Code so the env var change takes effect.

Once a character is created and imported via `lua_import_character`, follow the standard post-import checklist (see `pob-mcp/CLAUDE.md` → "After lua_import_character"): ask about bandits, quest passives, pantheon.

---

## Step 5 — Invalidate cached price data

Trade and ninja results are cached per-league. After updating `POE_LEAGUE`:

- Trade cache TTL is 1 hour ([tradeClient.ts](../pob-mcp/src/services/tradeClient.ts)) — expires naturally.
- ninja cache lives in `poeNinjaClient` — same TTL.
- Cached stash tab listings from `poe-trade-mcp` may still reference the old league name; the next `list_tabs` call refreshes them against the new default.

Nothing to manually invalidate; just be aware that the *first* price lookup after the switch may take a moment longer than usual while caches warm.

---

## Step 6 — Audit per-league reference docs

`reference_data/leagues/Mirage.md` (and any other ended-league files) are now historical. Leave them in place — they're useful for "what did Mirage have, again?" questions. Don't delete; just don't load them as current-league context anymore.

The `playbooks/README.md` §2b directive says to load `reference_data/leagues/{current-league}.md` — once `POE_LEAGUE` is updated, that resolves to the new file automatically. No code change needed.

---

## Step 7 — Roll the knowledge anchors

Committed knowledge files hardcode the "current league", and league-scoped knowledge needs re-scoping. This checklist is the only procedure guaranteed to run at the moment they all change — walk every row:

| # | Where | What to update |
|---|---|---|
| 7.1 | `reference_data/freshness_index.md` | The "Current league is **X.Y Name**" callout under the cutoff table; add source bookmarks (league page + Version X.Y.0 page) for the new league |
| 7.2 | `reference_data/mechanics_index.md` | The "Current context anchors (update at each league roll)" line; re-scope every `challenge-league` mechanic from the ended league (→ `core` if GGG cored it, else `removed`); clear or set `disabled-this-league` entries per the new patch notes |
| 7.3 | Claude memory (`MEMORY.md` + files) | Update or delete league-scoped memories (e.g. a mechanic memory tied to the ended league); refresh the league-transition-dates memory for the next cycle |
| 7.4 | `scripts/session-start-check.sh` | Roll the league anchor variables at the top. **Challenge cycle:** `TEMP_LEAGUE` → the new league's name, `LEAGUE_END` → its end date, `NEXT_LEAGUE_START` + `NEXT_LEAGUE_NAME` → the league after (name is known from GGG's reveal). **Event cycle (check 4b):** point `EVENT_LEAGUE` / `EVENT_END` at the next event when one is announced, else set `EVENT_LEAGUE=""` to silence it. Check 4b self-limits — it fires only while an un-migrated event character exists (its meta.json `league` still names the event), so Step 3's meta.json flip already stops it; clearing the anchors at the next event roll is housekeeping, not required. Authoritative dates: the challenge-league table on the wiki [`League`](https://www.poewiki.net/wiki/League) page (exact end timestamps + versions); GGG's announcement post for the next launch date |

**Wait for the new league's patch notes before re-scoping mechanics** — whether a mechanic goes core is announced there and in GGG's end-of-league news post, not guessable in advance. If running this checklist before the notes drop, mark 7.2's re-scoping as pending and leave a journal/memory note to finish it.

---

## Step 8 — Archetype refresh (guide library trunks)

Archetype analyses in `character_data/guides/{archetype}/` are **league-spanning living
documents** (see the library README → "League lifecycle — trunk & branches"); characters
instantiate from the trunk's current-league state. At each transition, refresh the trunks
that matter — gated on patch notes, like 7.2:

1. **Which archetypes?** Active candidates first (anything marked as a league-start pick or
   with a character planned), then any the user asks about. Skip dormant archetypes — their
   trunks just stay stamped with their last-reviewed league.
2. **Resolve re-verify watchlists.** Archetype READMEs/profiles and
   `guides/_comparisons/*.md` carry "re-verify at patch notes" triggers (nerf-exposed gems,
   masteries, mechanics). Walk each against the actual notes: survived / buffed / nerfed /
   removed. A nerf that breaks a core mechanic ("they're nerfing this trigger — what
   replaces it?") → targeted mini [`build-design.md`](build-design.md) research loop for a
   replacement; record the outcome either way.
3. **Scan for new opportunities.** *"What new equipment/gems/mechanics could make this build
   better?"* — new uniques/gems from the Version X.Y.0 notes (Step 4.3 already enumerated
   them) filtered through the archetype's build-profile scaling; plus early-league
   [`community-survey.md`](community-survey.md) queries once the community has data.
4. **Archive, then bump.** Before rewriting a trunk for the new league: copy the superseded
   plan to `{archetype}/history/{league}-build-plan.md`, then update `build-profile.md` /
   `build-plan.md` and their `league:` stamps. Standing `_comparisons/` decisions whose
   numbers a nerf invalidated get re-opened (or re-affirmed with a dated note).

A character created for the new league then forks the freshly-bumped trunk — that's the
branch point.

---

## Done table

When the checklist is complete, report:

| Item | Status |
|---|---|
| `POE_LEAGUE` updated | ✓ / pending |
| Claude Code restarted | ✓ / pending — required for MCP subprocess to pick up env change |
| Character meta files updated | ✓ N/A (no affected characters) |
| New-league reference doc created | ✓ / N/A (no new league live yet) |
| Knowledge anchors rolled (freshness index, mechanics index, memories) | ✓ / pending (re-scoping may wait on patch notes) |
| Archetype trunks refreshed (watchlists resolved, plans archived + league-bumped) | ✓ / pending (waits on patch notes) / N/A (no active archetypes) |
| `get_active_leagues` shows no ⚠ | ✓ / ⚠ persists (investigate) |

---

## Pitfalls

- **Don't update `POE_LEAGUE` before the user is ready to act on Standard prices.** Once flipped, the trade tools query Standard by default. If the user is still trying to liquidate Mirage stash, leave it pointing at Mirage until they're done.
- **Hardcore characters go to Hardcore, not Standard.** If the user runs HC, double-check `get_active_leagues`'s parent column — don't assume "Standard" for everything.
- **Restart Claude Code, not just `/reload`.** MCP servers are subprocesses spawned at session start. Env-var changes need a full process restart.
- **PoB submodule updates are NOT aligned with league boundaries.** PoB updates on patches (~weekly during a league, irregular otherwise). Don't expect a league transition to also bring a tree/mod update.
