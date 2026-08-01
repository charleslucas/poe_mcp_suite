# Playbook: Gear Crafting Audit

Answers **"are there easy crafts/upgrades I can do to my *current* equipment?"** — a **breadth-first sweep of
the whole loadout** looking for cheap, deterministic wins: open affixes, available bench crafts, an empty
anoint, missing quality, and low-tier mods worth overwriting.

Distinct from its neighbours:
- [`crafting-optimization.md`](crafting-optimization.md) — **depth-first on ONE item** ("what should I put on
  this open suffix?"). This playbook *finds* the candidates; hand a chosen item to that one to design the craft.
- [`crafting-lookup.md`](crafting-lookup.md) — pure "what can roll" data lookups.
- [`gear-shopping.md`](gear-shopping.md) — replacing an item by buying. **This audit routinely concludes
  "replace, don't craft"** — hand off there.

---

## Step 0 — Frame the work

Detailed-scope by default (10+ slots × several checks). Confirm the goal before pulling data: a *defensive*
audit and a *damage* audit rank the same findings differently. If the user has a live symptom ("I keep dying to
X"), make it the ranking lens — see §Step 3.

**Prerequisite:** a live PoB build (`lua_import_character` recently run). Nearly every tool below reads the
loaded build over TCP.

## Step 1 — Triage

Skip the full sweep and answer directly when:
- The question is about **one** item → `crafting-optimization.md`.
- The user wants to **buy** an upgrade → `gear-shopping.md`.
- Nothing has changed since the last audit (check `journal.md`) → re-state the prior open items.

## Step 2 — Data loads

| Load | Tool | Notes |
|---|---|---|
| Whole loadout, all slots | `get_equipped_items` | Orientation; also reveals uniques (uncraftable affixes) |
| Per-slot mods, tiers, **ilvl** | `analyze_item_mods` with `item_slot` | The core call — reads live from PoB. Run per rare slot |
| Bench crafts available for a slot | `search_master_crafts` (`item_type`, `type`) | Deterministic pool. **Check group collisions — see Pitfalls** |
| Anoint candidates | `find_best_anointment` | Simulates ALL ~450 notables through PoB's engine |
| **Oil prices** | `ninja_lookup` per oil | **Mandatory** — the tool ranks impact, not cost |
| Build-level gaps | `validate_build` | Prefer over `get_build_issues` + `analyze_defenses` (covers both) |

**Don't** run `analyze_item_mods` on uniques — their affixes are fixed. Check them only for an empty anoint
(amulets, Cord belts) or missing quality.

## Step 3 — Analysis pattern

Per rare slot, ask in this order — cheapest first:

1. **Open affixes?** Count prefixes/suffixes from `analyze_item_mods` (3 max each on a rare).
2. **If open — is a *useful* bench craft actually available?** Run `search_master_crafts` for the slot, then
   **eliminate every craft whose `group=` matches a mod already on the item** (see Pitfalls — this is the #1
   false positive).
3. **Low-tier mods worth overwriting?** `analyze_item_mods` prints `Tier: N of M` and the next tier. A mod at
   T9/10 or T11/11 is a dead slot in disguise.
4. **Is the item's `ilvl` capping it?** A low-ilvl item can't roll good tiers *at all*. When the ceiling is the
   problem, the answer is **replace, not craft** → `gear-shopping.md`.
5. **Quality below 20%?** ⚠ **Confirm with the user in-game** — PoB's import appears to drop item quality.

Then once per build: **anoint** (empty amulet/Cord belt) and `validate_build` for anything structural.

**Rank by gain-per-chaos, not raw gain**, and against the user's stated lens. Present the ranked list, then the
honest "these are not craftable" residue.

## Step 4 — Output shape

A single table, cheapest-first: **action · measured gain · cost**, followed by two short sections:
- **Skip / blocked** — with the *reason* (group collision, bench slot used, affixes full). Users act on these
  otherwise.
- **Not craftable — needs a purchase or a structural change** — the honest ceiling of the audit.

Sim anything non-trivial before recommending it (`add_item` the modified version → `lua_get_stats`), and
**restore the build afterwards** (`lua_import_character`).

## Step 5 — Pitfalls

- ⚠ **Mod-group collisions kill most "open affix" wins.** A bench craft in the same `group=` as an existing mod
  **cannot be applied**. Real example: a ring with an open prefix, `+60 life` (group `IncreasedLife`) and a junk
  `+3 ES` (group `EnergyShield`) — both the life and ES bench crafts were blocked, leaving only worthless mana.
  **Always diff craft groups against the item's existing groups before promising anything.**
- ⚠ **One bench craft per item.** If a slot already shows `{crafted}`, its craft slot is spent — a second needs
  multimod (itself a craft, and only economic with 2+ open affixes).
- ⚠ **`find_best_anointment` ranks by impact, not cost.** Price every candidate's oils with `ninja_lookup`
  before recommending. Real example: the #1 pick needed a **232c Golden Oil** for +1,121 EHP, while the #3 pick
  cost **~1–2c** for +742 EHP — ~100× better per chaos.
- ⚠ **PoB import drops item quality** — it will look like "add 20% quality" is available when it's already done.
  Confirm in-game before recommending it, and treat imported armour/evasion/ES as a floor.
- ⚠ **Low ilvl is invisible until you look.** `analyze_item_mods` reports it; a mod at T9/10 on an ilvl-36 base
  isn't a bad roll, it's a *ceiling*. Recommend replacement.
- ⚠ **Crafting cannot fix a missing defensive layer.** If the user dies to physical burst with minimal armour,
  no affix on their current gear solves it. Say so plainly and route to the structural fix.
- Uniques: no affix crafting. Anoints, quality and corruptions only.

## Trust hierarchy

PoB data files & live PoB sim (authoritative, patch-current) → craftofexile cache → poewiki → community
opinion. **Never** AI search for craft mechanics or mod data (see the `ai-search-is-for-opinion-not-facts`
memory). Prices: poe.ninja (`ninja_lookup`) before trade queries.
