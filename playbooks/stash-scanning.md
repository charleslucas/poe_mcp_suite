# Playbook: Stash Scanning & Item Pricing

Evaluate stash tab contents to find items worth listing, items to vendor, and currency to invest. Uses the local algorithmic scorer (no GGG trade API calls) for rares and poe.ninja for named items.

Read `playbooks/README.md` first (cursory/detailed gate, pre-flight, context management, narration norms).

---

## Current status: stash access works (undocumented endpoint)

**Verified 2026-11-18:** `list_tabs` returned 80 Standard tabs and 25 Covens tabs through the POESESSID path
(`character-window/get-stash-items`). It had returned HTTP 403 from 2026-06 onward; whether GGG re-enabled it or
the earlier failure was a dead cookie is unknown.

**Caveat:** `character-window/*` is not in GGG's API Reference, and the developer docs say reverse-engineering
endpoints outside the documentation is against Terms of Use section 7i (see `legal_considerations.md`). It can be
withdrawn without notice, so keep usage human-scale and don't build anything that assumes it is permanent.

**League:** every stash tool takes an optional `league` (default `POE_LEAGUE`). A league where the account has no
character has no stash and returns **404** — pass `league="Standard"` for Standard tabs.

**If it fails:**
- **403 (code 6)** usually means the `POESESSID` is dead. A cookie ends when you log out of the website. Get a
  fresh one (see `INSTALL.md`) and update **every** server in `.mcp.json` that sets `POE_SESSION_ID`, then reload.
- **404 (code 1)** means no stash or character for that league/name. Check the `league` and `character_name` arguments.

**Alternatives that need no stash access:**
- `score_rare(item_text=...)` — Ctrl+C one item in-game; local scoring, no API call. Rares only; use `ninja_lookup`
  for named items.
- **[WealthyExile](https://www.wealthyexile.com)** — a community tool on GGG's official OAuth gateway that prices
  whole stash tabs.
- **Your own OAuth app** (`poe_auth`, documented `api.pathofexile.com/stash` endpoint) is the sanctioned route, but GGG's
  developer docs currently say new application registration is closed. If it reopens: register a public client,
  redirect URI `http://127.0.0.1:7878/callback`, add `POE_CLIENT_ID` to `.mcp.json`, run `poe_auth`. The tools then
  prefer OAuth automatically.

---

## Workflow

### Stage 0 — Pre-flight
```
mcp__poe-trade-mcp__list_tabs          # see all tab names and indices
mcp__poe-trade-mcp__cache_status       # check cache freshness
```

### Stage 1 — Load tab contents
```
mcp__poe-trade-mcp__get_tab(tab_name="dump")    # fetch and cache a specific tab
```
Or for all tabs with underscore prefix:
```
mcp__poe-trade-mcp__scan_stash_tabs(min_price=5)   # prices everything worth ≥5c
```

### Stage 2 — Price analysis
```
mcp__poe-trade-mcp__price_tab(tab_name="dump", min_price=5)
```

Returns sorted rare items with:
- `price_estimate` — chaos value estimate
- `total_score` — composite quality score
- `good_mods` — count of valuable affixes
- `junk_mods` — count of poor affixes
- `breakdown` — per-mod contribution

Named items (uniques, currency, gems) are priced via poe.ninja:
```
mcp__poe-trade-mcp__ninja_lookup(name="Divine Orb")
```

### Stage 3 — Decision making

**Worth listing:** `price_estimate ≥ 20c` AND `good_mods ≥ 2`
**Worth vendoring (recipe):** check for 3-link chromatic recipe, 20% quality recipe, etc.
**Worth keeping:** build-relevant mods the character needs

### Stage 4 — Record and act

For high-value finds, update `character_data/<Account>/<League>/<Character>/journal.md` with discovery and decision. For currency investments, check `currency_overview` to find the best conversion path.

---

## Single-item workflow (no stash access needed)

For evaluating individual items from your stash without bulk scanning:

1. Hover over item in stash in-game
2. Press Ctrl+C to copy item text
3. Call `score_rare` with the copied text
4. For uniques/currency: call `ninja_lookup` with the item name
5. Decision: list (≥20c estimate), vendor (recipe), or keep

For a full stash audit without bulk tools, work through items category by category — start with the highest ilvl rares since those have the best chance of high-value mods.
