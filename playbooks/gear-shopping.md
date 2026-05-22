# Playbook: Gear Shopping

For Claude sessions where the user wants to find a replacement or upgrade for a specific gear slot. Load this playbook in full at the start of the task; it gates which data sources you need to fetch and saves context.

---

## Step 0 — Frame the work for the user

Open with one sentence: *"Using the Gear Shopping playbook — quick triage first, then I'll pull the current build state and check the market."*

Narration norms:
- Before reading the build: "Pulling current equipped items and stats to map what we'd be giving up."
- Before searching trade: "Searching trade with pseudo stat filters — these match items regardless of which explicit mod line the stat comes from."
- When a result looks good: "Let me simulate this in PoB before recommending it — numbers on paper can hide attribute or resistance problems."
- When trade returns nothing: lower the requirements incrementally and explain which stat was dropped and why.

---

## Step 1 — Triage (structured)

Run via `AskUserQuestion`. Skip any question where the answer is already clear from context.

**Q1 — What's driving the search?**
- Upgrade (strictly better version of what's there)
- Constraint fix (attribute shortage, resistance gap, flask limitation)
- Budget reallocation (sell a valuable piece, replace cheaper)
- Slot is empty / item dropped

**Q2 — Which slot(s)?**
- Single slot (user names it)
- Multiple slots (e.g., "rebalance resistances across rings + belt")
- Open — "find the weakest piece"

**Q3 — Hard constraints to preserve**
- Any resistance caps that must be maintained
- Minimum attributes (Str / Dex / Int) required for gems or other gear
- Flask constraints (e.g., Screams of the Desiccated — only Seething instant flasks allowed)
- Unique item locked in an adjacent slot that cannot move

**Q4 — Budget**
- Read from stash first via `mcp__poe__list_tabs` + ninja lookups on notable items before asking. Present the estimate for confirmation.
- If budget is clear from prior conversation, skip.

---

## Step 2 — Data loads

### Always load
- Equipped items: `mcp__pob__get_equipped_items`
- Current stats (resistances, attributes, life, DPS): `mcp__pob__lua_get_stats(category='all')`
- Character analysis doc if it exists: `character_analyses/{League}-{CharacterName}.md`

### Add if shopping for a resistance-critical slot (ring, belt, amulet, body, boots, gloves)
- Map ALL resistance contributions before proposing any swap — know exactly what each piece provides so the math is correct before hitting trade. A ring might be contributing fire + cold + lightning + chaos simultaneously from implicit AND explicit mods.

### Add if the target item involves a unique
- Ninja lookup via `mcp__poe__ninja_lookup` for current price and variant pricing
- Wiki fetch via `mcp__poemcp__fetch_wiki_page` if the unique's interaction with the build isn't obvious

### Add if the swap affects attributes
- Check total Str / Dex / Int before and after. Losing an item with +53 Dex affects gems AND other equipment that has Dex requirements.
- Check which gems and gear pieces have the closest attribute requirements — those are the first to fail if an attribute source is removed.

### Add if the user mentions stash scanning
- Fetch relevant stash tabs: `mcp__poe__get_tab` (populates cache)
- Ninja lookup on any notable uniques found — check ALL stash tabs including Char Stash, not just dump tabs. Valuable items accumulate in character stashes.
- Note: `mcp__poe__price_tab` returns 0 priced items for rares by design — the rare scorer identifies items worth checking on trade, but does not produce price estimates. Use trade search for actual rare prices.

---

## Step 3 — Analysis pattern

1. **Map what the current item contributes** — list every stat it provides that matters: resistances (each element separately), attributes, life, DPS mods, flask mods, utility. This is what the replacement must cover.

2. **Calculate minimum requirements for the replacement** — the new item must cover the delta. Be precise:
   - Current resistance total → target cap (75% ele, user's chaos target)
   - Minus what all *other* items provide in that element
   - = Minimum resistance the new item needs
   - Same math for attributes

3. **Search trade with pseudo stat IDs** — pseudo stats (`pseudo.pseudo_total_*`) match the total regardless of where it rolls, making them far more effective than explicit stat filters:
   - `pseudo.pseudo_total_life`, `pseudo.pseudo_total_dexterity`, `pseudo.pseudo_total_cold_resistance`, etc.
   - Use `mcp__poe__get_stat_ids` to find the right IDs before building the filter

4. **Evaluate results by shape, not just headline number** — check:
   - Does it cover fire AND cold, or just one? (overcapping one element is wasted budget)
   - Is it corrupted? (no further crafting possible)
   - Are there open affixes for crafting? (ilvl 82+ base usually needed for best crafts)
   - Does the base type matter? (Two-Stone Ring has dual-res implicit; Sapphire Ring has cold; Ruby has fire, etc.)

5. **Simulate in PoB before recommending** — use `mcp__pob__add_item` with the item text, then re-read stats to confirm resistances, attributes, and DPS all land correctly. Save the build file after if changes are good.

6. **Provide the trade link** — always include the `trade_url` from the search result so the user can verify availability themselves.

---

## Step 4 — Output shape

For quick single-item swaps, a chat summary is enough:
- Best option found, price, key stats, trade link
- What it fixes vs what it trades away
- Any follow-up needed (craft the open suffix, check PoB for attribute issues, etc.)

For multi-slot rebalances or large budget sessions, append to `character_analyses/{League}-{CharacterName}.md`:
- **Gear Swap Log** dated entry with: slot, old item, new item, cost, stat delta
- Any identified follow-on gaps (e.g., "still 3% cold short — watching for a helm enchant")

---

## Step 5 — Pitfalls (lessons from past sessions)

### Stash API
- **PoE stash API requires the full account name WITH discriminator, URL-encoded.** `AccountName#1234` must be sent as `AccountName%231234`. Stripping the `#discriminator` (`account.split('#')[0]`) causes persistent HTTP 403 on all stash endpoints even with a valid POESESSID. Character-window endpoints for character data are more lenient and accept the base name.
- **POESESSID expires.** If stash calls return 403 and character imports still work, the session is likely still valid but the stash endpoint has changed. Check the discriminator first. If that's correct, the session may genuinely be expired — get a fresh cookie from browser DevTools.
- **Special stash tabs (MapStash, FragmentStash, CurrencyStash) return items nested in sub-tabs**, not at the top-level `items` array. The legacy API uses a `stash` list key; the OAuth API uses `children`. `stash_cache.py` handles both — but if items are missing from a special tab, check that the normalization is unwrapping correctly.

### Resistance math
- **Always calculate per-element, not "total elemental resistance."** An item can contribute 12% fire, 32% cold, and 20% chaos simultaneously from a single Two-Stone Ring (12% fire+cold implicit + 20% cold+chaos explicit). Treat each element independently.
- **Overcapping one element wastes stat budget.** Check all four elements, not just the ones you're trying to fix. A swap that over-solves cold while fire stays uncapped is a poor trade.
- **Removing a ring/belt often drops multiple resistances at once.** Map all contributions before hitting trade — it's easy to fix cold but miss that fire also drops below cap.
- **Lightning overcap is common and costly.** Builds with body armour lightning resistance often have 70–80% overcap on lightning from rings. Don't design upgrades around maintaining that overcap.

### Attribute requirements
- **Removing a dex source can fail gems AND other gear simultaneously.** A single ring with +53 Dex removed can cause 2+ skill gems and a piece of equipment to go red at the same time. Always check total attribute totals before and after, not just the item being swapped.
- **Body armour "reduced attribute requirements" is item-specific, not global.** `32% reduced Attribute Requirements` on Sacred Chainmail lowers only that armour's requirements. It does not help meet requirements for rings or gems.
- **Gem attribute requirements scale with gem level.** A level 20 Precision, Frostblink, or Multistrike can require 90–130 Dex. Check gem-level requirements, not base requirements.

### Flask constraints
- **Screams of the Desiccated grants Diamond Shrine buff only while NO flasks are active.** Any flask with a duration effect (Quicksilver, Granite, Basalt, "during effect" suffixes) disables the buff for its entire run time. Only Seething (instant recovery) life and mana flasks are compatible — they consume instantly with no lingering effect.
- **"Grants Immunity to X for N seconds if used while X" (conditional immunity) does NOT count as an active flask** — the immunity is granted as a separate buff, not a flask effect. This is why Seething conditional-immunity flasks preserve the Diamond Shrine buff.
- **"Immunity to X during Effect" DOES count as an active flask** and kills the Diamond Shrine buff for the duration. Never recommend "during effect" suffixes for this belt.
- **Tinctures do NOT count as flasks for Screams of the Desiccated.** Activating a tincture does not remove the Diamond Shrine buff. Tinctures are a free damage layer for this belt — particularly strong with high elemental damage tinctures like Sap of the Seasons (95% increased elemental damage, up to 200% penetration).

### Trade search
- **poe.ninja prices are variant-specific.** Queen's Decree is priced at 287c for 6-linked. A 2-socket Queen's Decree in your stash is worth ~10c. Always check the `links` and `variant` fields in ninja results before reporting a price.
- **Pseudo stat IDs find more listings than explicit stat IDs.** `pseudo.pseudo_total_dexterity` matches any combination of `+# to Dexterity` and `+# to Dexterity and Intelligence` etc. Use explicit IDs only when you specifically need a mod from one explicit line.
- **Jewel dex is capped well below 35.** A single viridian jewel cannot roll 35+ dex — the max roll for a single `+# to Dexterity` mod is ~25. If you need 35 dex from a jewel, it must come from two mods (e.g., `+# to Dex` + `+# to Dex and Int`). If no listings exist at that threshold, lower to 25+ and look for a ring instead.

### Stash scanning
- **Check the Char Stash tab too.** Valuable items accumulate in character stashes, not just dump tabs. Scanning only numbered dump tabs misses items that can be worth many divines.
- **`price_tab` min_price filter always returns 0 results for rares** because `rare_scorer.price_estimate` is intentionally set to 0. The scorer identifies items worth checking on trade via `should_trade_check`, but does not produce chaos estimates. Use `mcp__poe__search_trade` for actual rare pricing.
- **Unique items need ninja lookup, not the rare scorer.** The scorer only handles magic/rare items. For uniques, call `mcp__poe__ninja_lookup` directly.
- **Foulborn variants are priced separately from base versions.** `Foulborn Ventor's Gamble` (Foulborn prefix = reroll) has its own price tier. Check both the base and Foulborn entries in ninja results.

---

## Trust hierarchy

When sources conflict, prefer in this order:
1. Live in-game observation by the user (item pastes, character API data)
2. Live PoB TCP stats after simulating the swap
3. Live trade API results (actual current listings)
4. poe.ninja live lookup (cached 15 min in the MCP server)
5. Cached `reference_data/` (check freshness)
6. Claude's training (last resort — often outdated on prices, mod availability, and league mechanics)
