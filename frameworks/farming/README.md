> **Canonical home:** `poe_mcp_suite/frameworks/` (public). Instance data is patch-stamped (3.29) — re-verify after any league/patch change. `local library:` references point into the maintainer's private guide library (character data + digested third-party guides, not distributed); treat them as worked-example citations, not links.

# Farming Strategy Database

**What this is:** the currency-making layer of the library — a roster of farming strategies with the same
conventions as [`_styles/`](../styles/minions.md) and [`_concepts/`](../_concepts/README.md):
**aliases** (community names = survey keys), **✅/◐/⛔ confidence**, **references** (videos, guides, reddit
tutorials), and a dated **survey ledger**. Strategies are durable across leagues; their **viability is
league-stamped** — a 3.29 tier means nothing in 3.30 until re-surveyed.

**Division of labor:** this DB answers *what's worth farming and for whom*. A live
[`atlas-planning`](../../playbooks/atlas-planning.md) session answers *how to set up your atlas for it*.
Pick here, implement there.

**Founding principle** (from a 3.29 thread, and worth keeping forever):
> *"Your 'strat' for profit should be playing Harvest if Harvest juice is high in demand… not because
> there's a broken interaction."* — farm **demand**, not bugs; bugs get hotfixed, demand persists.

---

## 1. Decision axes

| Axis | Range |
|---|---|
| **Investment** | none (just maps) → scarab sets per map → 8-mod corrupted + 5× orbs |
| **Attention/APM** | walking-sim → tower management → speed-clearing |
| **Payout shape** | steady (lifeforce, essences, oils — bulk-sold) vs jackpot (boss drops, div cards) |
| **Build requirements** | speed · burst DPS · tankiness — every strategy leans on one |
| **Sell effort** | raw currency (zero) → bulk commodities (TFT-style selling) → item pricing |

## 2. Strategy roster — 3.29 stamps (surveyed 2026-08-04)

| Strategy | Aliases | 3.29 verdict | Needs | Payout |
|---|---|---|---|---|
| **8-mod Harvest** | "juiced harvest", "lifeforce farming" | ◐ **community meta king, 15-20+ div/hr**. Corrupted 8-mod Jungle Valley/Mausoleum (bosses block bad altars), 110%+ quant / 40%+ pack, ◐ Harvest Scarab of Doubling; clear map FIRST (stack quant altars), then harvest | strong build for 8-mods; bulk-sell effort | steady (lifeforce) |
| **5× Diviner's Delirium** | "div card delirium", "stacked deck farming" | ◐ 24+ div/hr claimed; 5× Diviner's orbs + Beyond + map-mod-effect atlas | **high** — dense juiced T16s; real DPS | steady (stacked decks) |
| **Altar + Strongbox speed farm** | "altar farming", "box farming" | ◐ budget tier; open layouts (Strand), strongbox duplication nodes, Beyond | speed > tank | steady, modest |
| **Low-tier Essence** | "essence farming (white maps)" | ◐ recommended early-week budget starter, zero map-mod management. ⚠ See the juiced version below — same mechanic, opposite verdict | almost nothing | steady (essences) |
| **Juiced Essence** | — | ⛔ **for slow/moderate-DPS builds in 3.29** — ◐ "essence monsters giga-tanky this patch"; multi-essence rares become 5-minute fights or deaths | millions of burst DPS | steady |
| **Blight** | "tower defense", "blighted maps", "oil farming" | ◐ **#1 for tanky/slow builds** — towers do the work; narrow layouts (Silo, Toxic Sewer); payout oils/blighted maps/golden-oil anoints | tankiness; almost no DPS/speed | steady (oils) |
| **Expedition** | "logbook farming", "Tujen haggling", "Rog crafting" | ◐ **excellent for tanky builds** — monsters spawn packed on you; Tujen/Dannig atlas nodes; Extreme Archaeology if burst AoE | tankiness; patience | steady (logbooks/currency) + Rog jackpots |
| **Ritual** | "omen farming" | ◐ decent for tanky builds (locked-arena fighting) — ⚠ ◐ claim: 3.29 removed synthesized implicits from the reward pool, ceiling nerfed; still omens/decks/currency | tankiness | steady + omen jackpots |
| **Pinnacle boss farming** | "boss rushing", "invitation farming" | ◐ needs DPS above all; pays in fragments + chase drops (e.g. **Congregation from Incarnation of Dread** — see `_styles/minions` ledger). EV includes the non-jackpot loot | DPS ≥ multi-million for ubers | jackpot-heavy |

**League-mechanic strategies (Allflame-specific — check `reference_data/leagues/Allflame.md`):** the
league's nautical/seafloor mechanic, Reliquarian, and Mercenaries of Trarthus (⭐ source of the fire→chaos
conversion gear — merc item farming may be quietly profitable given that tech's visibility) are all
unsurveyed as money-makers. ◐ Queue item.

## 3. Build-fit: our Block SRS Necromancer (L91, 57.8k EHP, ~0.7-1M DPS, moderate speed)

| Fit | Strategies |
|---|---|
| ✅ **Natural** | **Blight** (stand and block while towers + SRS work), **Expedition** (packed spawns onto a build that cannot be burst down; can take deadly remnants glass cannons skip), **Ritual** (locked arena = block heaven) |
| ◐ Workable | 8-mod Harvest (survivability yes — check DPS against juiced 8-mod rares), low-tier Essence, altar farming (speed is only moderate) |
| ⛔ Wrong shape | Juiced Essence (burst-DPS check we fail), 5× Delirium (density outpaces ~1M DPS), **Uber** boss farming |

### Worked example: maintainer's atlas state (2026-08-04)
Two-loadout plan: an existing tree specced **Abyss + Harvest** (Harvest = the surveyed meta king; Abyss
self-supplies the build's own Ghastly Eye economy — farming your own gear upgrades is EV the div/hr number
misses), plus a second loadout to build for **Blight/Expedition/Ritual** (the tanky-build tier). Strategy
switching = loadout swap, not respec. Implementation: `atlas-planning` session.

## 4. Survey ledger

### 2026-08-04 — founding surveys (2 queries)
- Q1 (general div/hr meta): partial sourcing (inline threads real, source list empty — treat numbers as ◐).
  Yielded the top-3 meta strats + the farm-demand-not-bugs principle (thread `1v8l2oo`, 1wk old).
- Q2 (tanky-build fit): fully sourced (r/pathofexile `1vas4d1` + YouTube). Yielded the Blight/Expedition/
  Ritual/Essence fit table and two ◐ 3.29 patch claims to verify.
- **Contradiction preserved:** Essence is both "recommended budget starter" (unjuiced, low maps) and "trap
  for slow builds" (scarab-juiced). Same mechanic, different investment tier — the axes matter.

### 2026-08-04 (addendum) — creator sources user-verified
BawLoch (farming videos) and Redviles (@Redvilespoe) confirmed real by direct check — both are now standing
survey targets / References sources (indexed in `reference_data/guide_sources.md`). The 6-year-old
untagatunu compendium spreadsheet also real (post deleted, sheet alive): mine it for *structure*, not data.

### Verification queue
- [ ] ◐ scarab names (Harvest Scarab of Doubling, Influencing/Monstrous Lineage/Mania) — **no scarab data in
  the text lake** (known gap); verify via wiki/trade before buying sets
- [ ] ◐ "3.29 removed synthesized implicits from Ritual" and "3.29 essence monsters giga-tanky" — check
  `patch_notes_index.md` / league doc
- [ ] Allflame league-mechanic profitability (seafloor / Reliquarian / merc farming) — directed survey
- [ ] Lifeforce + oil + logbook prices via `currency_overview` at session time (prices stale in hours)
- [ ] After a strategy is picked: `atlas-planning` session to implement it
