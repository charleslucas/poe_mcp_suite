# Playbook: Gear Shopping

For Claude sessions where the user wants to find a replacement or upgrade for a specific gear slot, identify the best upgrade opportunity across all slots, or evaluate a specific found item. Load this playbook in full at the start of the task.

---

## Prerequisites (always run before anything else)

**1. Load the build profile** — `character_data/{Account}/{League}/{Character}/build-profile.md`. If it doesn't exist, create a minimal one from the current PoB state before proceeding. Gear analysis without build-specific mod value overrides (Section 4) and hard constraints (Section 5) misses the most important signal: whether a mod actually matters to *this* build. A T6 mod the build doesn't scale is worse than a T2 mod on a core stat.

**2. Compute the constraint margin table** — call `mcp__pob__compute_constraint_margins(profile_path, write_back=true)`; it fills Section 6 (Constraint Status) from live stats and flags violated/near-floor rows (manual fallback: `lua_get_stats(category='all')` + fill by hand). This is the baseline for cascade analysis *and* constraint repacking. A margin is spendable budget; zero margin means any loss requires compensation before the change is valid.

---

## Step 0 — Frame the work for the user

*"Using the Gear Shopping playbook — loading build profile and computing constraint margins, then quick triage before I pull market data."*

Task-specific narration: before searching trade, note that pseudo-stat filters are used (they match items regardless of which explicit line the stat rolls on). When a result looks good, simulate it in PoB before recommending — numbers on paper can hide attribute or resistance problems. When trade returns nothing, lower requirements incrementally and explain which stat was dropped and why.

---

## Step 1 — Session prerequisites (triage)

Run via `AskUserQuestion`. Skip any question where the answer is already clear from context.

**Q1 — Session goal**
- Upgrade a specific slot (user knows which one)
- Find the best upgrade across all slots ("where should I spend my div?")
- Fix a specific constraint violation (resistance gap, attribute shortage, mana pressure)
- Evaluate a found or dropped item ("is this worth equipping?")
- Budget reallocation (sell a valuable piece, replace cheaper)

**Q2 — Which slot(s)?** (skip if Q1 is "find best upgrade" or "fix constraint" — gear audit in Step 2 determines this)
- Single slot (user names it)
- Multiple slots (e.g., "rebalance resistances across rings + belt")

**Q3 — Optimization objective**
- Cheapest valid path — satisfy all constraints, minimize cost
- Sweet spot — willing to spend more for meaningful threshold gains
- Threshold — trying to hit a specific target ("4000 life", "100% hit chance", "Uber-ready")
- Budget allocation — "X div to spend, where does it go furthest?"

**Q4 — Hard constraints to preserve** (skip if fully established in build profile Section 5)
- Any resistance caps that must be maintained
- Minimum attributes (Str / Dex / Int) required for gems or other gear
- Flask constraints (e.g., Screams of the Desiccated — only Seething instant flasks allowed)
- Unique item locked in an adjacent slot that cannot move

**Q5 — Budget**
- Read from stash first via `mcp__poe__list_tabs` + ninja lookups on notable items before asking. Present the estimate for confirmation.
- If budget is clear from prior conversation, skip.

---

## Step 2 — Gear audit (when Q1 = "find best upgrade" or slot is unknown)

> **Current-league note:** before sourcing a replacement, check whether the current league can *transform*
> an existing item. **Mirage:** a **Djinn coin** (Restoration ↔ Desecration) flips a dual-form Mirage unique
> to its better stat profile (Desecration also adds a corrupted implicit). See
> `reference_data/leagues/{league}.md` → Djinn Coins.

Run `mcp__pob__analyze_item_mods` on all equipped slots. For each mod, apply a two-axis classification:

**Axis 1 — Tier** (as reported by the tool)
**Axis 2 — Build relevance** (cross-reference build profile Section 4, Mod Value Overrides):

| Classification | Meaning |
|---|---|
| **Load-bearing** | Enables a hard constraint (leech source, hit chance, flask type) or is required by an anchor item dependency |
| **High-value** | In the "worth more than tier suggests" list — scales with the build's primary damage chain |
| **Resistance / attribute budget** | Provides needed res or attributes — necessary but not build-specific |
| **Weak and relevant** | Low-tier mod of a stat the build cares about; upgrading it would translate to DPS or defense |
| **Weak and irrelevant** | Low-tier mod of a stat in the "worth less" or "irrelevant" list — marginal value |
| **Wasted** | Explicitly "irrelevant or detrimental" per Section 4 — affix slot exists but does nothing for this build |

Aggregate per slot: slots with wasted or weak-and-irrelevant affixes are upgrade candidates even if their overall tier looks acceptable.

**Output: ranked upgrade candidate list**, sorted by:
1. Wasted affix count (slots with explicit irrelevant mods are highest priority)
2. Weak-but-relevant mod count (slots where tier upgrades would translate to build DPS or defense)
3. Constraint margin proximity (slots contributing to stats where margin is near zero are risky to change — treat with caution)

Present this list to the user and confirm which slot to target before proceeding.

---

## Step 3 — Data loads

### Always load (build profile is already loaded from prerequisites)
- Equipped items: `mcp__pob__get_equipped_items`
- Current stats: `mcp__pob__lua_get_stats(category='all')` — already computed for constraint margins; re-use that call
- Character journal if it exists: `character_data/{Account}/{League}/{Character}/journal.md`
- **Current-league item levers**: `reference_data/leagues/{league}.md` — slot-relevant transform/craft options the league adds (e.g. Mirage Djinn coins flipping dual-form uniques). The league can change what "upgrade" means for a slot; check affirmatively, don't wait to remember.

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

## Step 4 — Analysis pattern

1. **Map what the current item contributes** — list every stat it provides that matters: resistances (each element separately), attributes, life, DPS mods, flask mods, utility. This is what the replacement must cover.

2. **Calculate minimum requirements for the replacement** — the new item must cover the delta. Be precise:
   - Current resistance total → target cap (75% ele, user's chaos target)
   - Minus what all *other* items provide in that element
   - = Minimum resistance the new item needs
   - Same math for attributes

3. **Cascade analysis** — before searching trade, compute what replacing the current item costs across all constraints:
   - For each stat the current item contributes, subtract from the corresponding constraint margin (from the table computed in Prerequisites)
   - Identify which margins go negative
   - For each negative margin: what is the cheapest compensation path? (other gear, tree node, gem swap)
   - Sum total cost: target item + all compensations
   - **"Don't make this change" is a valid output.** If the cascade cost exceeds the budget or no viable compensation exists, record the finding in build profile Section 8 (Design Attempt Log) and stop. Knowing what not to do is as useful as finding what to buy.

4. **Constraint repacking — run when the target slot carries ≥2 constraint mods (resistances/attributes)** — the trade search inherits whatever load the current item carries, so a burdened slot searches a needlessly narrow space, and the candidates that would win *after* a rebalance never surface (cascade can't chase consequences of an item the search never found). Before building the filter:
   - From the margin table + the Step 2 `analyze_item_mods` output, list the **constraint load per slot** — who carries which resistances/attributes.
   - For each constraint the target slot carries, probe the **cost to carry it elsewhere**: quick trade queries for the absorbing slot with vs. without that mod (a sub-agent can batch these).
   - If absorption is cheap (rule of thumb: total absorption cost under ~30% of the slot budget), plan the **multi-slot move** — liberated target-slot search plus the absorber swap — and run the next step against the *liberated* requirement set, not the inherited one.
   - Cascade analysis (step 3) then re-runs on the **whole multi-slot move** to validate it — same waterfall, now fed better candidates.
   - "The current packing is already optimal" is a valid outcome; proceed with the normal single-slot search.

5. **Enumerate the slot's unique/special candidates — kill the unknown-unknown** — weighted searches explore the *rare* mod space; the best item for the slot is often a unique or special base the model didn't think of, and unique knowledge is model-cutoff-bound. Enumerate instead of recalling:
   - Dispatch an Explore sub-agent to sweep the **complete current unique list for the slot** (poe.ninja unique overviews — name, one-line effect, price) and filter it through the build profile's Core Mechanics + Section 4 to the 3–5 that actually interact with this build. The agent reads the full list; main context sees only survivors.
   - Check `reference_data/leagues/{league}.md` for **this league's new uniques** in the slot — newer than every model's cutoff by definition.
   - Include **special bases** where the profile flags a relevant pool: influenced, fractured-mod, synthesis-implicit, eldritch-dominated versions of the slot.
   - Survivors compete with the rare-search results in the PoB simulation step on the same DPS/EHP-per-cost axis.
   - For **meta convergence** ("what do other players of this build use here?"): a slot-specific `community-survey` query or the `guides/` library. Do NOT wrap poe.ninja's builds API — explicitly prohibited by their docs (see README wishlist, investigated 2026-07-08); the user browsing poe.ninja/builds and pasting findings is the sanctioned path.

6. **Search trade with pseudo stat IDs** — pseudo stats (`pseudo.pseudo_total_*`) match the total regardless of where it rolls, making them far more effective than explicit stat filters:
   - `pseudo.pseudo_total_life`, `pseudo.pseudo_total_dexterity`, `pseudo.pseudo_total_cold_resistance`, etc.
   - Use `mcp__poe__get_stat_ids` to find the right IDs before building the filter

7. **Evaluate results by shape, not just headline number** — check:
   - Does it cover fire AND cold, or just one? (overcapping one element is wasted budget)
   - Is it corrupted? (no further crafting possible)
   - Are there open affixes for crafting? (ilvl 82+ base usually needed for best crafts)
   - Does the base type matter? (Two-Stone Ring has dual-res implicit; Sapphire Ring has cold; Ruby has fire, etc.)
   - **Apply build profile mod value overrides**: a T4 mod that the build scales is worth more than a T2 mod it doesn't. Shape > tier.

8. **Evaluate crafting as an alternative to buying** — before finalising a trade recommendation, run a quick crafting feasibility check:
   - Use `mcp__poemcp__search_craft_mods(target_mod)` to confirm the target mods are in the craftable pool.
   - Use `mcp__poemcp__get_craft_base_items(base_name)` to confirm the base exists and its drop level.
   - Signal "crafting is worth considering" when: trade has few or no good listings at budget, the target item needs only 1–2 key mods, or the user already has relevant fossils/essences in stash (check with `mcp__poe__scan_stash_tabs` if unsure).
   - Signal "just buy it" when: the item needs 3+ specific mods simultaneously (crafting cost becomes exponential), budget is tight and the user needs a guaranteed result, or a good trade listing already exists within budget.
   - For actual odds and cost estimates, direct the user to the craftofexile Calculator — our tools confirm what can roll and which fossils have affinity, but the probability math lives in their client-side engine.

9. **Simulate in PoB before recommending** — use `mcp__pob__add_item` with the item text, then re-read stats to confirm resistances, attributes, and DPS all land correctly. Save the build file after if changes are good. Uniques from step 5 and rares from step 6 rank on the same simulated axis here — the sim ranking is the recommendation, not the listing order.

10. **Provide the trade link** — always include the `trade_url` from the search result so the user can verify availability themselves.

---

## Step 5 — Output shape

For quick single-item swaps, a chat summary is enough:
- Best option found, price, key stats, trade link
- What it fixes vs what it trades away
- Any follow-up needed (craft the open suffix, check PoB for attribute issues, etc.)

For multi-slot rebalances or large budget sessions, append to `character_data/{Account}/{League}/{Character}/journal.md`:
- **Gear Swap Log** dated entry with: slot, old item, new item, cost, stat delta
- Any identified follow-on gaps (e.g., "still 3% cold short — watching for a helm enchant")

If cascade analysis found a change infeasible, record in build profile Section 8 (Design Attempt Log): what was tried, what it cost in constraint margin, why it failed. This prevents repeating the same analysis in future sessions.

---

## Step 6 — Pitfalls (lessons from past sessions)

### Build profile required
- **Do not evaluate gear without loading the build profile first.** Tier analysis alone misses build-specific mod value. A T6 mod the build doesn't scale is worse than a T1 mod on a core stat. On a phys-conversion build with Winds of Fate, flat physical damage is nearly irrelevant — but a generic tier analysis ranks it highly.
- **Apply mod value overrides before ranking trade results.** The best listing on trade may have high-tier mods that the build profile marks as "worth less than tier suggests." Always apply the override lens before reporting a recommendation.

### Cascade analysis
- **Compute cascade before searching trade, not after.** Discovering that a ring upgrade drops cold resistance below cap after you've already recommended it wastes a step. Run the constraint delta first.
- **"Don't make this change" is a first-class output.** The cascade analysis for Determination (cost: ~50% mana reservation on a build with no mana budget) took 10 seconds to run and saved a guaranteed regression. Knowing what to skip is as useful as finding what to buy.
- **Record infeasible changes in Section 8 of the build profile.** If you don't, the same change will be re-analyzed in the next session.

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

See [`README.md`](README.md) section 5. For gear shopping specifically: live trade API results and poe.ninja lookups (both current) rank above cached `reference_data/` for prices, since prices change daily. Build profile mod value overrides rank above generic tier evaluation for build-specific recommendations — a live PoB simulation of the proposed item is the final arbiter.
