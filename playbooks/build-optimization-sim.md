# Playbook: Build Optimization via PoB Sim

Find upgrades by simulating changes in a live PoB session before spending any currency. The core discipline: **measure first, buy second.** This playbook covers the full audit surface — gems/links, gem quality, jewels, and stat-layer analysis — in a repeatable order that maximizes information per sim.

Read `playbooks/README.md` first (cursory/detailed gate, pre-flight, context management, narration norms).

---

## When to use this playbook

- "Is there a better support gem for my build?"
- "Which jewels should I re-roll?"
- "Where does X divine best move the needle?"
- "Is my attack speed / crit / damage capped?"
- "Optimize my current gear/gems"

Detailed scope — run pre-flight before pulling data.

---

## Stage 0 — Pre-flight and character load

```
mcp__pob__get_context_usage          # headroom check
mcp__pob__lua_get_build_info         # confirm right build is loaded
mcp__pob__get_build_issues           # fast issue scan
mcp__pob__lua_get_stats(all)         # full stat snapshot — Life, DPS, EHP, resists, block
mcp__pob__get_equipped_items         # full gear read — note every slot's mods
```

Read `character_data/<Account>/<League>/<Character>/build.md` and `meta.json` — prior analysis, open questions, upgrade path phases.

**Read the league freshness checklist:** `reference_data/leagues/<league>.md` → "Rule / mechanic changes" section. Confirm no mechanic assumption is stale before proceeding.

**At this point, pause and state the plan** (Stage 1 items you identified, expected data sources, which are PoB sims vs. trade lookups). Wait for confirmation before proceeding.

---

## Stage 1 — Baseline DPS decomposition

Before simming anything, understand *how* the DPS is built:

```
mcp__pob__get_calc_breakdown(TotalDPS)     # top-level: AvgDamage × Speed
```

Try common sub-breakdowns (availability varies by build — call with no stat arg first to see what's available):
```
mcp__pob__get_calc_breakdown(AverageDamage)
mcp__pob__get_calc_breakdown(CritChance)
mcp__pob__get_calc_breakdown(CritMultiplier)
mcp__pob__get_calc_breakdown(Speed)
```

Read the gem layout from the saved XML if `get_skill_setup` doesn't show supports (known gap — see ISSUES.md):
```
Grep "<Gem " in the saved build XML
```

**Key questions to answer at this stage:**
- What is the sustained vs. burst DPS gap? (config/flask state matters — note both)
- Is CritChance at 100% (forced)? If so, crit *chance* mods are wasted; crit *multi* is the lever.
- What is HitChance? (<95% = accuracy is free DPS, investigate before simming.)
- What is the total INC pool for Speed? (>80% INC = attack speed has heavy diminishing returns; crit multi becomes better $/DPS)
- Which attack speed / crit multi mods are conditional vs. unconditional? (`get_stat_breakdown` with `use_skill_config`)

---

## Stage 2 — Gem/link audit (always do first — highest ROI, near-free)

**Snapshot before any changes:**
```
mcp__pob__snapshot_build(tag="before-gem-sim-<date>", description="baseline for gem sim")
```

Work through the main link systematically:

### 2a — Dead / underleveled active and support gems

Check every gem in the main link:
- Level < max? (Verify max for the specific gem — some supports have low max level by design, e.g. Void Shockwave Support max is 2)
- Quality 0%? (See quality sim below — not all quality matters)
- Is the gem's effect actually active for this build? (e.g. Trinity requires multi-element hits to build Resonance; PoB may not model this — see PoB calc limitations below)

**Before flagging a low-level gem as "needs leveling":** check if it's *intentionally* under-leveled for mana cost reasons. Higher gem levels increase mana cost. For gems that fire frequently — especially **marks/curses on a Mark on Hit Support with a channeling skill** (e.g. Poacher's Mark + Cyclone: fires every hit, mana cost compounds continuously) — keeping a gem at level 10–15 instead of 20 can be the correct call for builds with tight mana. Check free mana (`ManaUnreserved` from `lua_get_stats`) before recommending a level-up.

### 2b — Support gem choice sims

For each support gem that looks questionable, sim the swap one at a time:
1. Remove the suspect gem (`remove_gem`)
2. Add the candidate replacement at level 20 (`add_gem`)
3. Read `lua_get_stats(offense)` — note TotalDPS, AverageDamage, CritMultiplier, Speed
4. Reset to baseline before the next sim (remove replacement, add original back)

**Do NOT compare across sims that used different PoB config states** — Speed can jump between reads if a config toggle flips during gem operations (known baseline instability, see ISSUES.md). Always restore snapshot and reload if Speed/DPS shifts unexpectedly between sims.

Candidate replacements to always consider for melee builds:
- **Melee Physical Damage** — scales phys before conversion; best for conversion builds (Winds of Fate etc.)
- **Awakened versions** of any support currently in the link (1–10 div, additive to normal gem)
- **Brutality** — if build deals no ele/chaos damage (check conversion first)
- **Concentrated Effect** — more damage, less AoE; swap vs. Pulverise for single-target
- **Increased Critical Damage** — only beats Pulverise if crit multi pool is thin; this build (forced 100% crit, saturated crit multi) showed ICD < Pulverise

**Watch for:** a support that shows 0 DPS change on level-up likely isn't modeled in PoB's static calc (Trinity resonance, conditional buffs, leeching-state effects). Note it but don't assume the gem is useless — PoB has known gaps for dynamic/conditional effects.

### 2c — Gem quality sims

Quality matters only when the quality effect is unconditional damage:
- `% increased [DamageType] Damage` on a support → test it
- `% increased Area of Effect` → clearspeed only, skip
- `% increased [something] while Leeching/Channelling` → conditional; PoB static calc often returns 0 even if real-world value exists

Test procedure: set quality to 20 (`set_gem_quality`), read stats, reset to 0. Quality upgrades are cheap (a few GCPs or buy a pre-leveled gem) but the DPS gain is usually small (1–3%).

---

## Stage 3 — Jewel audit

`get_equipped_items` lists all jewels with their mods. For each jewel, classify every mod:

| Mod type | Examples | Action |
|---|---|---|
| Dead | "increased Damage with Bleeding" on a non-bleeder; "increased Crit Chance with [Element] Skills" on a 100%-crit-forced build | High priority swap |
| Marginal | Defensive filler (chill reduction, stun avoidance) on an offense jewel | Medium priority |
| Good | `+% crit multi with 2H`, `% increased attack speed with 2H`, `% increased melee damage`, `% increased maximum life` | Keep |

**Sim procedure (API limitation):** `add_item` does not accept jewel socket slots — only gear slots (Helmet, Body Armour, etc.). To sim a jewel swap:
1. Ask the user to make the change in the PoB GUI ("Create Custom" or right-click → Edit on the jewel)
2. Read stats immediately after they confirm

**Critical: exact mod text for PoB's custom item editor:**
- Crit multi: `+17% to Critical Strike Multiplier with Two Handed Melee Weapons` (requires the leading `+`)
- Attack speed: `6% increased Attack Speed with Two Handed Melee Weapons` (no `+`, uses "increased")
- Verify mods went green/blue in PoB's tooltip before reading stats — if PoB shows "not supported" the mod isn't registering

**Expected gains per dead-mod swap on a 2H melee jewel:** ~3–4% TotalDPS (driven by +17% additive crit multi when total crit multi pool is ~400%). Multiple swaps stack additively.

**Attack speed diminishing returns:** when the total INC pool for Speed is already >80%, each additional +6% INC contributes <1% relative Speed gain. At that point, crit multi is a better DPS-per-stat-point investment. To verify: call `get_stat_breakdown(Speed, use_skill_config=true)` and sum the INC column.

---

## Stage 4 — Stat layer / reservation audit

These are reads, not sims:

```
mcp__pob__get_calc_breakdown(ManaReserved)   # how much mana is reserved
mcp__pob__lua_get_stats(defense)             # Life, EHP, resists, block
```

**Enlighten level:** Enlighten 3→4 frees reservation. Check whether the freed amount (~20–30 mana typically) is enough to add another aura. If not, note it as "not actionable until reservation addressed from other sources."

**Overcapped resistances** are wasted gear budget. From `get_build_issues`, check the info section for "X resist Y% over max cap." Each overcapped point represents affix budget that could be offense or life instead. Flag slots contributing most to the overcap.

**HitChance < 95%:** each missing 1% is ~1% DPS loss (13% miss rate = 13% DPS lost). Sources: `get_stat_breakdown(Accuracy, use_skill_config=true)`. Fix: accuracy on rings/gloves/amulet, or Precision aura level.

---

## Stage 5 — Prioritize and recommend

After all sims and reads, rank findings by **DPS-per-div** and **risk**:

| Finding | DPS gain | Cost | Risk |
|---|---|---|---|
| Dead support gem → MPD (example) | +50% | ~1c | None (gem swap) |
| Main-link support gem quality 0→20% | +1–3% | 5–30c | None |
| Dead-mod jewel re-roll (1 jewel) | +3–5% | 20c–1div | None |
| Awakened support gem | +8–15% | 1–10div | None |
| Accuracy fix (87% → 95% HitChance) | +~9% | 0–50c | None |

Gems and quality almost always win on DPS-per-div. Jewels stack but are modest per-swap. Gear upgrades (rings, amulets) require careful mod analysis to confirm they don't break other things (attribute requirements, resistance caps, unique-item mechanics).

**The in-game character sheet DPS is unreliable for complex builds.** Conversion builds (phys→ele), trigger setups (General's Cry warriors, Void Shockwave procs), and multi-element damage pipelines are all systematically under-reported by the character sheet. It doesn't model the full conversion chain, proc rates, or warcry interactions. **Trust PoB's TotalDPS number, not the character sheet.** For real-world confirmation, compare hit numbers on a map boss or tankier rare before/after the change — there is no player-accessible training dummy in PoE.

**Before recommending a gear swap, check:**
- Does swapping break attribute requirements? (Check `get_build_issues` after simming)
- Does it displace a mod that's load-bearing for the build mechanic (e.g. a unique that enables a crit engine)?
- Does it push any resistance overcapped (wasted) or undercapped (dangerous)?
- **Craft vs. buy:** use `search_craft_mods(target_mod)` to confirm the target mods are in the craftable pool. If trade listings are thin or overpriced, flag crafting as an alternative — especially when the item needs only 1–2 key mods. Direct the user to the craftofexile Calculator for actual odds and expected cost.

---

## Stage 6 — Record findings and close

Update `character_data/<Account>/<League>/<Character>/build.md`:
- Add a dated "Gem/Link Audit" or "Optimization Audit" section
- Record: current link setup with per-gem level/quality, findings per sim (delta and verdict), recommended actions in priority order
- Add undone items to the "Open Questions / Follow-ups" section
- Add any new PoB calc limitations discovered to ISSUES.md

---

## PoB calc known limitations (relevant to this playbook)

These produce 0 DPS change even when the real-world effect is real. Note them rather than concluding the gem is useless:

| Effect | Reason not modeled |
|---|---|
| Trinity Support resonance | Requires dynamic hit-type accumulation across time; static calc can't simulate it |
| Infused Channelling quality bonus | PoB's static calc for channelling quality effect may not apply in all configs |
| Energy Leech quality ("while Leeching") | Leeching state not active in static calc |
| Any "while you have X buff" | Buff state must be enabled in PoB Config tab manually |

**Rule of thumb:** if leveling a gem 1→20 produces exactly 0 change, check whether its primary effect requires a runtime state or PoB Config toggle. Verify in actual play before concluding it's worthless. **Note: there is no player-accessible training dummy in PoE** — GGG has intentionally not added one (a dev-only version exists in the game code). For real-world DPS verification, compare hit numbers on a map boss or tankier rare between before/after states.

---

## Playbook wishlist / gaps

- Sim support for jewel slots via XML edit + reload (currently requires user to make GUI change)
- Awakened gem tier comparison (Standard vs. Awakened vs. Exceptional)
- Accuracy audit path (HitChance < 95% → which slot to fix)
- Resistance rebalancing (overcapped → offensive mod swap)
- Pantheon analysis belongs in the planned `defense-audit.md` playbook (not here) — it reads defensive gaps and recommends major/minor gods to fill them. Key inputs: `lua_get_stats(defense)`, `get_calc_breakdown(StunAvoidChance)`, keystone awareness (e.g. Unwavering Stance = unconditional stun immunity, making Brine King redundant).
