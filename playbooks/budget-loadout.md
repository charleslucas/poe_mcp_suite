# Playbook: Budget Loadout

For sessions where a **finished target build already exists** in Path of Building (a "goal" loadout), the user states a **budget** and what they already own, and expects a ready-to-buy loadout inside their own copy of that build — plus one page listing everything to do.

Not this playbook: designing a build from a concept (`build-design`), improving an existing character slot by slot (`dps-analysis`, `gear-shopping`), comparing builds (`build-comparison`).

Read `playbooks/README.md` first for the shared meta-framework (cursory-vs-detailed gate, league reference, trust hierarchy).

**This playbook is a living document.** Whenever a run exposes something it should have said — a naming convention, a trap, a step that was missing — append it here before finishing the session. Improvements land in this file, not in conversation notes: the next run reads the file and nothing else.

---

## The four words

Everything below hangs on these, and they are the only progress signals that count:

- **ceiling** — the stated budget. Every purchase is measured against it *before* it is recommended; the running total is reported in divines.
- **caps** — the requirement sheet **read off the target build in Step 1**, not a universal checklist. Its floor is the same for every build: elemental resistances at 75/75/75 and a sane EHP. Everything above that floor exists only if the target has it: chaos resistance, spell suppression, block/spell block, armour, specific attribute thresholds. A build with capped suppression and no chaos res must be matched on suppression, not on chaos; a totem build with 75 chaos and 4k EHP must be matched on those, not on suppression.
- **green** — `get_pob_warnings` returns zero lines. PoB's own warning list is the only place attribute/req problems surface; a green bar is the gate to "done".
- **receipt** — a trade link that has been decoded back to its query and matched. A link the agent retyped is not a receipt.

---

## Step 1 — Read the target, measure what actually matters

Load the build, list loadouts, and identify which loadout is the **goal** and which is the user's **current** state. Record the goal's headline numbers (FullDPS, EHP, life/ES/mana, block, caps) as the baseline.

Then measure, do not guess, the price of leaving things out: clear or swap one item at a time and read the delta. Rank the target's items by measured DPS/EHP contribution.

**Completion criterion:** you can state the goal's numbers, name every item whose removal costs more than ~5% DPS or breaks a cap, and confirm the tree fits the character.

**Check the tree against the character's level before anything else.** PoB's tree panel states the level the *currently allocated nodes* demand — `Required Level: N` under the point counter. Compare that number with the character's level: the difference **is the shortfall in points**, one point per level. Do not try to read it off the pool counters (`life / mana`) — they mix pools and mislead; `Required Level` is the authoritative number. A one-level gap means one node must go (or one level earned); say it in the first message and name two or three cuttable nodes (a travel node at the end of a branch, a utility cluster) so the user can decide immediately instead of discovering it in-game. When the levels match, say that too.

Carry four facts out of this step:

- **Fixed gear** — things the user owns and will not change (a belt + its flasks, a levelled gem set). They survive into the budget version untouched.
- **Essentials** — the mods that make the build function (a 6-link, a level-of-gems modifier the damage scales on, a conversion the build is built around). These are never downgraded for cheapness; if the budget cannot hold one, say so and ask.
- **Point shortfall** — `Required Level` from PoB's tree panel minus the character's level, i.e. how many nodes the target tree cannot fit (zero is the normal answer, and it still gets stated).
- **Requirement sheet** — the target's own defensive and attribute profile, written down row by row with its value: elemental resists, chaos resistance, spell suppression, block and spell block, armour/evasion/ES pools, life/mana, EHP, and every attribute a socketed gem demands. The floor is universal (75/75/75 elemental + a sane EHP for the content); every other row exists because *this* build has it. Quote the target's numbers, not a generic target.

Copying another build's checklist here is the classic error: a suppression build and a MoM totem build have almost nothing in common defensively, and demanding the wrong row either wastes the budget or hides a real gap.

---

## Step 2 — Build the loadout shell

Create the budget loadout with all four families carrying the **same title** (`BUDGET`): passive tree spec, item set, skill set, config set. `copy_loadout` (from the goal loadout) or `create_loadout` does all four in one call; a family that holds a single set is PoB's wildcard and is shared rather than duplicated. Jewel sockets are the one part the MCP surface cannot set — jewels live at `<Tree><Spec><Sockets><Socket itemId=… nodeId=…>`, not in the item set, so `add_item` cannot touch them; use the XML recipe in `assets/budget-loadout/loadout-xml.md`.

**Completion criterion:** `list_loadouts` reports the new loadout as complete (no "incomplete" warning), the same character level as the target, and the item set is active.

---

## Step 3 — Price the uniques, then spend

Uniques and gems: price from poe.ninja in one batch (`poe-data.price_check`), never from a trade search. Convert to the user's currency convention on output: `>= 1 div` in divines, below that in chaos, totals always in divines.

Put every affordable unique in place and re-read the numbers after each block of changes.

**Completion criterion:** the running unique+gem total is known and under the ceiling, with the remainder explicitly reserved for rares.

---

## Step 4 — Close the requirement sheet with rares

Design the rare slots against the **requirement sheet from Step 1**, not against a generic list: one slot per open row (elemental resists first, then whatever this build actually carries — chaos, suppression, attribute threshold, life/mana pool). Keep the essentials from Step 1 intact.

Iterate: change one slot, read the stats, move the next open row into the slot that can hold it. When a rare must carry a fractured/eldritch mod (conversion, implicit conversion), that is a *design*, not a luxury — but it still has to fit the ceiling.

**Completion criterion:** every row of the requirement sheet matches the target's value (the elemental floor at minimum), `get_pob_warnings` is empty, and the DPS/EHP delta versus the target is written down.

If an attribute check fails, fix the *source* — add the attribute to a rare — rather than lowering a gem level.

Rows the target does not have are not gaps: a build at 4% chaos resistance is being matched correctly at 4% unless the user asks otherwise. Say what you *did not* close and why, instead of silently padding it.

---

## Step 5 — Produce receipts, not links

Generate every link with `generate_trade_urls` for the equipped slots of the budget loadout. The tool derives the filters from each item's own mods, sets the base type and category, and writes a markdown file; it verifies each link by decoding it back.

**Completion criterion:** the tool reports `Verified: N/N`, and a second independent decode of the file shows every link valid with `status=securable` (Instant Buyout).

Rares are searched with the mod filters present and the roll bounds empty — the user sets rolls in the UI — with one exception: **life gets a floor of 70% of the item's own roll**. A search that happily returns a 10-life base is noise; the floor removes it without demanding a good roll. Everything else stays presence-only unless the caller passes an explicit `min_roll_pct`.

**Filter by intent, not by mod line.** Copying the target's mods one-to-one is what narrows the search to nothing: a ring that must supply resistance is equally served by fire, cold or lightning, and a slot that must supply "resistance in general" is served by 25+20 as well as by 45 of one type. So each mod is bucketed first, and the bucket decides the filter shape:

| Mod family | Filter | Threshold |
|---|---|---|
| elemental resistance (any mix) | `pseudo.pseudo_total_elemental_resistance` | `needs.ele_res` |
| one resistance, when the slot only needs *a* resistance | OR group fire / cold / lightning | `needs.ele_res` each, only with `or_mode` |
| chaos resistance | its exact stat | `needs.chaos_res` |
| attributes | their exact stat | `needs.dex / str / int` — never interchangeable |
| life | `pseudo.pseudo_total_life` | `needs.life`, else 70% of the roll |
| damage, cast speed, everything else | exact stat | none |

`needs` comes from the requirement sheet produced in Step 1, never from the item's own rolls: a high-roll target would set a threshold the market cannot meet. When a slot has no need for a family, its filter carries no bound at all. An implicit that the base itself guarantees (a resistance or attribute implicit) is skipped — the base filter already covers it. Two scope rules keep the search wide without making it wrong:

- **Base type only where the base means something.** Jewellery, weapons and jewels are base-locked: their implicit (a resistance, an attribute, a damage conversion) is part of what you are buying, so the base goes into the query. Ordinary ES/EV/AR armour is not — pinning one base throws away every equally good item of a neighbouring base. For armour, state the defence **pool** instead (`es: 1`, `ev: 1`, both for a hybrid piece) and let the mod filters do the work.
- **Never filter on eldritch implicits.** They are rolled by the buyer with ichor or ember, so requiring the seller's exact roll narrows the result to almost nothing. If the item carries a `Searing Exarch Item` or `Eater of Worlds Item` tag, the implicit lines are skipped.
- **A fractured affix is searched as its explicit twin.** "Fractured" describes how the item was made; the buyer needs the mod, not the crafting origin. `fractured.stat_*` would restrict the search to fractured items only, so the query uses `explicit.stat_*` for the same line.

**Corruption is never filtered unless asked.** Links carry no `misc_filters.corrupted` by default: with the filter absent the search returns clean and corrupted copies alike, so nothing is hidden from the buyer. Send it only on an explicit request (`true` = corrupted only, `false` = clean only) and never derive it from the item text. A slot whose required mod exists only on corrupted copies needs no special handling — requiring that mod is what narrows the search, and a clean-only filter there would be the dangerous direction: it silently removes the cheap half of the market.

`generate_trade_url` accepts `use_api: true` to return a server-issued id instead of a local payload. Offer it; the default is the zero-request local payload.

---

## Step 6 — Order the purchases

The order is a decision, not a courtesy: it goes into the page's `steps` and the user follows it literally. It is **not** importance, price, or armour-before-jewellery. Uniques have their own rule; the rest is decided by two properties, and neither depends on the budget.

**Uniques first — always.** A unique is a provider by construction: nothing else supplies its mods, its stats are not a choice, so there is no cap to balance and no design that could change. The only questions are price and whether it is still listed. So the first sweep is every unique in the plan (jewels included), biggest and least-verified line first. All uniques ahead of everything else is the default; a user who wants a different order says so.

**1. Whether another slot can supply the same thing.** Armour and accessory slots all feed the same handful of caps (elemental resists, chaos, attributes, block) on top of their own contributions. Within the *rares*, sort every slot into one of two roles:

- **provider** — supplies something no other slot can: a mechanic that lives on one item type (block chance on a shield), an uncraftable mod (a fractured conversion), a base-locked implicit, an attribute threshold no other slot reaches. Missing it costs a layer, not a roll.
- **closer** — tops up a shared cap that two or three other slots also carry: elemental resists and life on boots/rings/jewels, chaos on rings and jewels, an attribute on any armour slot.

Providers first, closers last. The reason is information: the last slot is the only one bought with the exact deficit known, after uniques, gems and the providers are in place. A closer bought early is a guess, and a guess is paid for twice — once on the purchase, once on the item that replaces it.

**2. How narrow the search is.** A provider is also the thinnest search: one specific uncraftable mod or one rare mechanic yields dozens of listings, not thousands. Open those searches early, before money is committed, because the answer can change the design (accept a lower block roll, move the conversion to another slot, raise the ceiling and ask). Discovering it after the budget is spent is the expensive version.

Between two closers the order is arbitrary — say so instead of inventing a rationale. A jewel that only closes a leftover resist belongs at the very end: it is the most interchangeable item in the plan and nothing depends on it.

Two adjustments that come from the money side, not the mechanics: the **most expensive or least verified line goes first**, so a price surprise invalidates the plan before anything is bought (inside the unique sweep it is already the first line; when it is a gem or a rare, it moves up), and **scarcity beats sequence** — a provider found below market is bought out of order.

**Completion criterion:** the page's `steps` open with every unique, then the gems, then the rares in provider → closer order; the table's prices and total let the user track the remainder; no closer appears before its deficit is known; and every "buy this first" is justified by one of the properties above — never by "it matters more".

---

## Step 7 — One page, generated

Build the page from the **verified file** and let the **build name the items** — never by retyping either:

```
node playbooks/assets/budget-loadout/make-page.cjs \
  --links trade_links.md --meta page-meta.json \
  --pob "<build>.xml" --itemset BUDGET --out final.html
```

`page-meta.json` carries the headline stats, the purchase table, the ordered steps (**in the Step 6 order, providers first**), the never-do list, the upgrade ladder and the checks. `page-template.html` is the layout; keep the styling as is unless the user asks.

Each purchase row needs three separate fields, because a slot name alone tells the buyer nothing:

- `slot` — where it goes (`Body`, `Shield`, `Ring 1`). Hand-written in the meta.
- `item` — **derived by the script, not written by you.** With `--pob`/`--itemset` it reads the item set of that loadout (plus the tree's `<Socket nodeId>` entries for jewels) and formats the item's own text: the base, the defence lines PoB writes (`Armour:`/`Evasion:`/`Energy Shield:`/`Ward:`), and `Implicits:` for jewellery. A unique gets its name, a rare gets category + defence type + base, and an armour piece always states its defence pool, because the buyer does not have the base table memorised. The script refuses (`NO ITEM IN BUILD`) when a link has no matching item instead of falling back to a guess, and prints `label corrected: …` whenever the meta disagrees with the build. Any hand-typed label is suspect: a hybrid base recalled from memory reads as a single defence type, while the item text states both pools two lines apart.
- the table is **sorted by `pos`, not by the links file**. The links file comes out in PoB slot order (weapons, armour, jewellery, jewels), which is not a buying order. Give every `prices` entry and every `extras` entry a `pos` taken from Step 6 (uniques 10+, gems 20+, rares 30+, fixed-gear notes 40+); the script merges both lists into one table and stable-sorts by it. A row left without `pos` lands at the end — that is the sign the order was never decided.
- `note` — why it is on the list, in one line (the mod that matters, the DPS it carries).

Check the built page: every `href` decodes, every price follows the div/chaos convention, the total is in divines, `labels from PoB` equals the link count, and no `{{PLACEHOLDER}}` survived.

**Completion criterion:** the page opens in the review pane, its link count equals the receipt count, every row's label came from the build, and no link inside it fails a decode.

---

## Step 8 — Leave the build self-explanatory

Write the plan into the build notes (`set_build_notes`) so the loadout survives without this conversation: budget, essentials, damage sources, upgrade order, pre-flight checks. **ASCII only** — PoB's font has no Cyrillic and renders it as `[U+041B]`.

Save the build, then report the delta to the target and the remaining ceiling.

**Completion criterion:** notes read back correctly, the file is saved, and the summary states DPS/EHP versus the target plus what the remaining budget buys.

---

## Reference rules

**Trade API discipline.** Any tool that calls GGG's trade API (`search_trade_items`, `search_trade_listings`, `generate_trade_url(s)` with `use_api: true`) needs the one-time consent in `CLAUDE.md` → "GGG trade API". Links cost nothing; searches cost the user's rate limit, which is per IP and shared by every tool. Price uniques from poe.ninja. Reach for `search_trade_items` only when a count or real prices are unavoidable, never in a loop over mod variations, and check `trade_rate_limit` first.

**Receipts.** A 400-character payload retyped by hand loses characters invisibly: one changed base64url character breaks the gzip CRC and the site answers *"the search is no longer valid"*. Hand the user a file path, or a link verified by `decode_trade_url` in the same breath.

**Names come from the item, never from memory.** Base type, defence pool and implicits are printed in the item's own text, and the build file holds that text for both the target and the loadout you assembled — so a label can be derived instead of recalled. A recalled base survives review because it looks plausible; a derived one cannot. The same applies to the trade query: the defence minimums are read off the item, so a hand-written label is the only place a wrong defence type can hide — which is why the page generator takes `--pob`/`--itemset` and overrides whatever the meta says.

**Alternate skill gems are selected by `type.discriminator`, not by name.** For an ordinary gem `type` is a string; for an alternate it is an object `{ "option": <base gem>, "discriminator": <disc> }`. `GET /api/trade/data/items` gives the mapping — the entry's `type` → `option`, its `disc` → `discriminator` — while its `text` is a display label and is **not** accepted as `type`. `misc_filters.filters.gem_transfigured` is Any/Yes/No and selects nothing. Both wrong shapes (the display name as a plain `type`, or the base name plus the trans flag) produce valid URLs that quietly return the ordinary gem: the payload decodes, the CRC passes, and the search is simply about a different item. When the search schema is undocumented, take one payload from the site UI by hand, decode it, and copy its shape — never infer it from the data endpoint. Gems otherwise need only `misc_filters.gem_level`/`quality`, and a gem is the one row that cannot be derived from the build's items: it has no equipped slot, so the name comes from the skill set (`<Gem nameSpec=…>`).

**Ceiling honesty.** Never present a loadout as complete while a row of the requirement sheet is open, and never quietly swap an essential for a cheaper substitute. State the gap, its price, and let the user decide.

**Compare by measurement, not by reading mods — but know what PoB does not model.** `compare_items` equips each trade copy-paste in the slot in turn, reads FullDPS/TotalDPS/EHP/life/ES and PoB's own warning list, then restores the original item. Use it for every "is this listing better" question — the answer is a delta against what is already equipped, not an opinion about which mod looks strong. Two things it exposes that a mod-by-mod argument misses: lines that do nothing for this build (a local weapon mod on a caster weapon measures as exactly 0%), and requirements the swap breaks (socket count, attributes) — PoB's warning text is printed per candidate, and a warning that the DPS table does not show is still a reason not to buy.

The reverse also holds: **a 0.0% delta means "PoB does not simulate it", not "it does nothing"**. Shrine buffs, on-kill triggers, ramping buffs and movement speed all measure as zero while being the whole reason the item is in the plan. So before quoting a table, ask what the item is for. If the answer is an effect PoB cannot see, the table is silent on the thing that matters — say so and rank by that effect's own roll range instead.

**Gem quality is not a uniform stat — measure it.** `compare_gem_quality` sets a gem to each quality in turn and reports DPS: on some gems quality is worth double digits, on others exactly 0.0% (utility and defensive quality lines), and a 20/20 copy costs several times a 20/0 one. Run it before buying any 20/20 support, and before assuming a "quality upgrade" row is an upgrade at all. Quality granted by items (an amulet giving quality to all gems) stays in place, so the numbers are the marginal value of that gem's own quality.

`compare_items` deletes its test items and re-selects the original by id when it finishes; on a PoB API older than `restore_item_slot` (PoB not relaunched since the update) it falls back to re-adding the original and says the test items remain — reload the build before saving in that case.

**A sandbox copy must be closed in the same breath.** Measuring on a copy of the build keeps the user's file clean, but the copy becomes the *loaded* build: leave it loaded and the user sees its warnings, its empty slot and its test items. Reload the original as the last action of the measurement, before reporting anything, and delete the copy.

**No universal caps.** Resistances, chaos, suppression, block, attribute thresholds and pool sizes come from the target build. The only constants are the elemental floor (75/75/75) and an EHP that survives the content the user named. Importing another build's defensive checklist is a bug, not diligence.

**Compare bases by simulation, not by reputation.** Two bases that look equivalent can differ by a few percent, and which wins depends on what the build already has: an implicit that adds cast speed can beat one that adds elemental damage when nothing else supplies cast speed, while a defensive base loses once the caps are met and its damage affixes cannot compete. When a slot's base is undecided, hold the explicit mods constant, swap the base, and read the numbers — a few sims cost less than a wrong purchase.

**Base type: match what the build actually scales.** The base sets the defence pool and which *defence* affixes can roll on it (`% increased Energy Shield` / `Evasion` / `Armour`, and the flat versions); life, resistances, attributes and cast speed roll on every armour base. A different defence type therefore only matters where the build leans on that defence — ES for a MoM or EB pool, evasion for a suppression build — and trading one for another is not a downgrade by itself. Prefer the target's base type when it feeds a defensive layer the build relies on, and when you deviate, state the measured cost (EHP or DPS delta), never an impression.

**Check a defensive unique against the fixed gear before buying it.** The target may carry a piece that only exists to patch a weakness the user's own gear already covers — curse mitigation next to a flask that already grants it, ailment immunity next to a setup that grants it. Before pricing such an item, ask what it defends against and whether the fixed gear already does that; if it does, the slot is free and belongs to damage.

**Currency convention.** Item price `>= 1 div` → divines; below → chaos; any total → divines.

**Fixed gear stays fixed.** The user's belt, flasks and gem setup are inputs, not variables. If a change to them would help, ask first.

**Report the shortfall.** When the budget cannot reach the target's numbers, say which mods were dropped and what they cost to add back, rather than reporting the reduced number as if it were the goal. The same applies to points: a tree that demands a higher level than the character has is a shortfall, and it belongs in the first message.

**Name the item, not the slot.** In every artifact the user reads — the page, the notes, the summary — a unique is called by its name and a rare by category + base. Every **armour** slot, unique or rare, additionally states its defence type and base (`<unique name> (ES, <base>)`, `rare · EV/ES (<base>)`), because the buyer does not have the base table memorised. A bare slot name, or "rare: life / res", forces them to reconstruct the item in their head.

**Fix the generator, not the output.** When a generated artifact is wrong (a placeholder left in, a column missing, a link unverified), patch the script under `assets/` and regenerate. Editing the HTML by hand reintroduces exactly the transcription errors the generator exists to prevent.
