# Playbook: Stash Scanning & Item Pricing

Evaluate stash tab contents to find items worth listing, items to vendor, and currency to invest. Uses the local algorithmic scorer (no GGG trade API calls) for rares and poe.ninja for named items.

Read `playbooks/README.md` first (cursory/detailed gate, pre-flight, context management, narration norms).

---

## ⚠️ Current status: stash tab access is BLOCKED

**The bulk stash scanning tools (`list_tabs`, `get_tab`, `scan_stash_tabs`, `price_tab`) do not currently work.**

GGG disabled the legacy `character-window/get-stash-items` endpoint that the POESESSID fallback relies on. It returns HTTP 403 Forbidden (error code 6) despite a valid session. The character equipment endpoint (`get-items`) still works with the same session, but stash is now restricted to OAuth only.

See `ISSUES.md` → "Stash API access" for the full technical detail and repro.

**The three paths forward:**

### Path 1 — `score_rare` (works today, no setup required)

Ctrl+C an item in-game and pass the clipboard text to `score_rare`. Returns a price estimate, tier breakdown, and which mods are good vs. junk. Works for any rare item, entirely local (no API calls). Use this for individual items you're unsure about.

```
score_rare(item_text="<paste Ctrl+C text here>")
```

Limitations: one item at a time, rares only (named items via `ninja_lookup` instead).

### Path 2 — OAuth developer registration (not recommended for personal use)

The full bulk scanning tools would work with an OAuth developer app registered at `pathofexile.com/developer`. However:
- The registration process is designed for **public-facing applications** (websites, tools used by multiple players authenticating their own accounts) — not personal tools
- It requires justifying each OAuth scope, a redirect URI, review by GGG, and ongoing maintenance
- GGG can revoke access if they decide your use case doesn't qualify

If you eventually build a public-facing tool from this suite, OAuth registration is the right path. For personal use, the overhead is disproportionate.

Setup steps if you choose this path:
1. Register at https://www.pathofexile.com/developer — set redirect URI to `http://localhost:7878/callback`
2. Add `POE_CLIENT_ID` to `.mcp.json` in the `poe` server env block
3. Run `poe_auth` — opens a browser, you authorize, tokens saved automatically

### Path 2b — WealthyExile (recommended for bulk stash pricing today)

**[WealthyExile](https://www.wealthyexile.com)** is a free community tool that uses GGG's official OAuth gateway (the same approved path) to price your stash tabs. It handles the developer registration on its own behalf as a public app — you just log in with your PoE account. It's the practical solution for bulk stash scanning without needing your own developer registration.

Use WealthyExile when you want the full "scan entire tab and show me what's worth selling" experience. Use `score_rare` when you want to quickly evaluate a single item without leaving Claude.

### Path 3 — Wait and see

GGG's API policies evolve. It's possible a future version of the API allows personal stash access via POESESSID or a simpler auth mechanism. The code already handles both OAuth and POESESSID paths — if the endpoint becomes accessible again, it will work without code changes.

---

## What the full workflow would do (for reference)

Once stash access is restored, the intended workflow:

### Stage 0 — Pre-flight
```
mcp__poe__list_tabs          # see all tab names and indices
mcp__poe__cache_status       # check cache freshness
```

### Stage 1 — Load tab contents
```
mcp__poe__get_tab(tab_name="dump")    # fetch and cache a specific tab
```
Or for all tabs with underscore prefix:
```
mcp__poe__scan_stash_tabs(min_price=5)   # prices everything worth ≥5c
```

### Stage 2 — Price analysis
```
mcp__poe__price_tab(tab_name="dump", min_price=5)
```

Returns sorted rare items with:
- `price_estimate` — chaos value estimate
- `total_score` — composite quality score
- `good_mods` — count of valuable affixes
- `junk_mods` — count of poor affixes
- `breakdown` — per-mod contribution

Named items (uniques, currency, gems) are priced via poe.ninja:
```
mcp__poe__ninja_lookup(name="Divine Orb")
```

### Stage 3 — Decision making

**Worth listing:** `price_estimate ≥ 20c` AND `good_mods ≥ 2`
**Worth vendoring (recipe):** check for 3-link chromatic recipe, 20% quality recipe, etc.
**Worth keeping:** build-relevant mods the character needs

### Stage 4 — Record and act

For high-value finds, update `character_data/<Account>/<League>/<Character>/journal.md` with discovery and decision. For currency investments, check `currency_overview` to find the best conversion path.

---

## Workaround workflow (works today)

For evaluating individual items from your stash without bulk scanning:

1. Hover over item in stash in-game
2. Press Ctrl+C to copy item text
3. Call `score_rare` with the copied text
4. For uniques/currency: call `ninja_lookup` with the item name
5. Decision: list (≥20c estimate), vendor (recipe), or keep

For a full stash audit without bulk tools, work through items category by category — start with the highest ilvl rares since those have the best chance of high-value mods.
