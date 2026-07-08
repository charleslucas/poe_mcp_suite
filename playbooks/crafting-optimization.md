# Playbook: Crafting Optimization

For *deciding* what to craft: which mod to put on an open affix, how to design a full item from a base, which Eldritch implicit to take, whether a corruption gamble is worth it, which essence/fossil route to run. Distinct from [`crafting-lookup.md`](crafting-lookup.md) (pure data lookups — what *can* roll); this playbook chooses among the options and prices the choice. The build profile (README §2d) is the engine: Sections 3–4 are the scoring function, and they collapse a 30–40 mod pool to the 6–10 candidates worth simming.

---

## Step 0 — Frame the work

*"Using the Crafting Optimization playbook — build profile as scoring function. I'll reduce the mod pool to the candidates this build actually scales, sim the finalists in PoB, and rank by impact per expected cost."*

Announce sims ("simming the 4 finalist mods against live PoB") and odds sources ("odds from craftofexile data, not memory").

---

## Step 1 — Triage

Auto-derive before asking: currency/fossils/essences on hand (stash scan), open affix count on the target item (`analyze_item_mods`), and whether the target is equipped or a scratch base.

**Q1 — Decision type** (drives everything downstream):
- (a) Single-slot mod selection — open prefix/suffix or multimod plan on an existing item
- (b) Full item design — craft a slot from a purchased/found base
- (c) Eldritch implicit choice — which Searing/Eater implicit for a slot
- (d) Corruption gamble — Vaal orb / double-corrupt EV on a specific item
- (e) Route selection — essence vs fossil vs chaos-spam vs harvest for a target mod set

**Q2 — Crafting on the equipped item, or a copy/base?** Equipped-item crafts are irreversible in game — this gates how conservative the recommendation must be.

**Q3 — Risk tolerance:** deterministic-only (bench, Eldritch, harvest — guaranteed outcomes at known cost) vs gamble-tolerant (essence/fossil spam, corruption — better EV, real variance). Default to deterministic-first when unstated.

**Q4 — Budget** for this craft (skip if clear from context).

---

## Step 2 — Data loads

| Condition | Load | Via |
|---|---|---|
| Always | Build profile + constraint margins | README §2d; `mcp__pob__compute_constraint_margins(profile_path, write_back=true)` |
| Always | craftofexile cache ready | `craftofexile_cache_status` → `update_craftofexile_cache` if stale/missing (crafting-lookup Step 1) |
| (a)/(b)/(e) | Craftable pool for the base | `mcp__pob__list_craftable_mods_for_base` / `mcp__poemcp__search_craft_mods`; tiers + weights via `get_craft_tiers` |
| (a) | Target item's current mods + open affixes | `mcp__pob__analyze_item_mods` |
| (c) | Eldritch implicit pools for the slot | `reference_data/` cached wiki pages (fetch if stale — patch-stamped) |
| (d) | Corrupted-outcome prices | `mcp__poe__ninja_lookup` for base + corrupted variants; wiki corruption-outcome table |
| (e) | Fossil/essence affinities | `mcp__poemcp__get_fossil_info` / `get_essence_mods` |
| Odds needed | Hit probability | `mcp__pob__calculate_mod_odds`; direct the user to the craftofexile calculator for multi-mod compound odds |

---

## Step 3 — Analysis pattern

1. **Reduce the pool through the profile.** Apply Sections 3 (Stat Priority) + 4 (Mod Value Overrides) *before* enumerating: mods in "irrelevant or detrimental" are excluded outright; "worth more than tier suggests" mods are promoted. Typical result: 30–40 rollable mods → 6–10 candidates. Without this step, exhaustive evaluation is intractable or wrongly ranked.

2. **Enumerate candidates precisely.** For each surviving mod: which tiers can roll at the base's ilvl, non-zero weights only, weight share = tier weight ÷ pool total (crafting-lookup Step 2). Confirm base properties first — fractures and influence change the pool.

3. **Sim each finalist in PoB.** `snapshot_build` → apply the candidate to a copy of the item text via `add_item` → read the DPS/EHP delta → `restore_snapshot` (the build-optimization-sim bracket pattern). Sim the *realistic* tier (the one the odds say you'll hit), not the T1 dream roll.

4. **Price the path.** Hit probability × cost per attempt = expected cost per candidate; deterministic routes (bench, Eldritch, harvest) cost their sticker price with zero variance. Rank by **build impact per expected cost** on the profile's objective axis (DPS-per-div, EHP-per-div, or constraint-fixed-per-div).

5. **Constraint check.** Run the winning candidate through the margin table — a craft that pushes a margin negative needs a compensation plan before it's a recommendation (cascade analysis, gear-shopping step 3).

6. **Corruption gambles get an EV table, not a vibe.** Enumerate outcomes (brick / no-change / each win) with probabilities, value each outcome at ninja prices, compare the EV against simply *buying the already-corrupted winner on trade*. Buying the outcome usually dominates for single-item needs — say so explicitly when it does.

7. **Compare against not-crafting.** The finished item may exist on trade below the expected crafting cost (gear-shopping step 8's mirror image). "Don't craft — buy it" and "don't craft — keep the current item" are both first-class outputs; record rejected routes in build profile Section 8.

8. **Deterministic-first default.** For a single item on a real character, variance is itself a cost: prefer bench/Eldritch/harvest routes within budget even at a modest premium over a better-EV gamble. Recommend gambles only when the user opted into risk (Q3) or the deterministic path can't reach the target.

---

## Step 4 — Output shape

Chat: a ranked table — candidate mod/route, simmed DPS/EHP delta, hit odds, expected cost, verdict — with the recommended path called out and the "buy instead" comparison stated.

Files:
- Executed crafts → journal entry (`## YYYY-MM-DD`): item, route, cost, outcome — **record failures as faithfully as successes**; failed crafts prevent expensive re-attempts (see the Marylene's lesson below).
- Rejected/infeasible routes → build profile Section 8 (Design Attempt Log).

---

## Step 5 — Pitfalls

- **Odds from memory are always wrong.** Weights are per-tier, pool-relative, and patch-dependent — `calculate_mod_odds` / craftofexile or nothing. (Core rule inherited from crafting-lookup.)
- **Eldritch pools are slot-specific in non-obvious ways.** Body armour's Eldritch pool has NO "reduced mana cost" mod — it's helmet-only (verified 2026-05-21, MirageSixFingeredMan). Verify pool membership per slot before promising an implicit.
- **Double corruption can destroy natural implicits that gate requirements.** A double-corrupted Marylene's Fallacy lost its natural +Int Lapis implicit, breaking helmet attribute requirements and blocking the swap entirely (2026-05-21, 1 div lost). Corruption outcome tables replace *all* implicits — check what the natural implicit is load-bearing for first.
- **Count open affixes before pricing multimod.** "Can have up to 3 crafted modifiers" economics only work with 2+ open affixes; a filled suffix block silently halves the plan.
- **Sim the tier you'll actually hit.** Ranking candidates by their T1 versions when the odds say T3 inverts recommendations — expected tier, not best tier.
- **Never craft on the equipped item without an explicit go-ahead.** PoB sims are reversible; game crafts are not. Snapshot first, state the irreversible step plainly, and wait for confirmation on anything that consumes the item's current state (recombination, corruption, slam on a full item).
- **Conditional beats unconditional when the condition is the content.** The 39% "while Unique Enemy in Presence" Hatred effect beat the 36% unconditional max for boss content (2026-05-21 body craft) — profile Section 4 context decides, not the bigger number.

---

## Trust hierarchy

See [`README.md`](README.md) §5. For crafting specifically: craftofexile cached data (patch-stamped) ranks above wiki for weights/pools; live PoB sim is the final arbiter of value; ninja prices decide craft-vs-buy.
