> **Canonical home:** `poe_mcp_suite/frameworks/` (public). Instance data is patch-stamped (3.29) — re-verify after any league/patch change. `local library:` references point into the maintainer's private guide library (character data + digested third-party guides, not distributed); treat them as worked-example citations, not links.

# Meta-Farming Guides — strategy roster

**What this is:** the currency-making layer of the library — a roster of farming strategies with the same
conventions as [`_styles/`](../styles/minions.md) and [`_concepts/`](../_concepts/README.md):
**aliases** (community names = survey keys), **✅/◐/⛔ confidence**, **references** (videos, guides, reddit
tutorials), and a dated **survey ledger**. Strategies are durable across leagues; their **viability is
league-stamped** — a 3.29 tier means nothing in 3.30 until re-surveyed. Entries ride the same **evidence ladder** as builds (see [`../README.md`](../README.md)), with one caveat: farming proofs also expire when the **mid-league economy** moves, so yield claims carry their survey *date*, not just their patch. And viability is **cyclical, not merely decaying**: strategies age out mid-league as the economy saturates, then come back early next league (low-tier Essence in this very roster is stamped “recommended early-week” — a phase-locked strategy). So **re-stamps append to a verdict history instead of overwriting it**: a pattern like “strong weeks 1–3, dead by mid-league, every league” is the roster's most *predictive* content — it says what to run on day one of the next league before any new survey exists.

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
| **League phase** | early-league window (mats everyone needs week 1) · evergreen · late-league/juiced · **cyclical — returns each league start** |

## 2. Strategy roster — 3.29 stamps (surveyed 2026-08-04)

| Strategy | Aliases | 3.29 verdict | Needs | Payout |
|---|---|---|---|---|
| **8-mod Harvest / Fruiting Astrolabe rushing** | "juiced harvest", "lifeforce farming", "brain off blasting" (the no-reading variant) | ✅ **PROVEN (3.29, BawLoch video digest 2026-08-05)**: 8-mod corrupted maps + **Doubling scarab + 2x Monstrous Lineage + 2x Sacrificial Fragments** (~25c/map, "at minimum triple"); RUSH the harvest (no full-clear) while trimming the fruiting Astrolabe; on the mod combo **"seeds at least T2" + "T2 chance to upgrade T3"** toggle **Synthesised Stability** and re-run the juiced map; escalate to Risk Scarab + pack-size chisels + full-clear for quant altars. **Floor ~4.5k lifeforce/map (50-map sample); >100k lifeforce / ~20 div per 20 maps with NO jackpots; 30k single-map jackpot ~6 div; creator: "60 div in a few hours"** — all creator-stated ◐ numbers, play-evidenced | ⚠ **survivability-gated**: late-chain maps "super rippy — getting killed, not killing" — favors tanky builds | steady + jackpot |
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

### 2026-08-05 — FIRST YOUTUBE EVIDENCE DIGESTION (Step 3b pipeline): BawLoch's Harvest video
- ✅ Full pipeline run: description (links, chapters) → auto-sub transcript (2,507 words) → digest. The
  8-mod Harvest row is now **play-evidenced** with creator-stated numbers and the actual operating loop.
- ✅ **Scarab names verified by the creator** (Doubling, Monstrous Lineage) — closing yesterday's ◐.
- ✅ **BawLoch is a Maxroll author** (maxroll.gg/@bawloch) and the description carries his **strategy
  spreadsheet incl. the atlas tree**: docs.google.com/spreadsheets/d/1EI9RSn4mVuuNVMURAtTuvZIBnoOcPYAsym4lvZxYlhE
  — yesterday's survey claim of a "BawLoch spreadsheet" was real.
- ◐ **New 3.29 system vocabulary learned from play narration, NOT yet properly documented**: "fruiting
  Astrolabe" (map-blob with per-map modifiers + a paying "vault"), "Synthesised Stability" (keystone
  enabling re-running a targeted map; maps "bisect" the blob), "Risk Scarab", "Regenerator/Originator(?)
  influence" (auto-sub garble — term unresolved), "T2/T3/T4 plants" tiers. → queue item below.
- 📌 Creator hand-off: **Milky** named as the league-mechanic (charts) farming specialist — human-vetted
  pointer, added to guide_sources. BawLoch's own next videos: Delve, Card, Legion, Breach, Abyss farms.
- 🔧 Pipeline tooling: universal yt-dlp stalls root-caused (v2026.06.09 stale → updated 2026.07.04 + deno
  JS runtime installed; CLI now ~3s). ⚠ the MCP youtube tools still stall — long-running server env
  predates the fix; retest after next MCP restart.

### Verification queue
- [ ] ◐ scarab names (Harvest Scarab of Doubling, Influencing/Monstrous Lineage/Mania) — **no scarab data in
  the text lake** (known gap); verify via wiki/trade before buying sets
- [ ] ◐ "3.29 removed synthesized implicits from Ritual" and "3.29 essence monsters giga-tanky" — check
  `patch_notes_index.md` / league doc
- [ ] Allflame league-mechanic profitability (seafloor / Reliquarian / merc farming) — directed survey
- [ ] **Document the Astrolabe / Synthesised Stability atlas system properly** — 3.29 endgame system,
  post-training for all models; currently known only from play narration. Wiki/league-doc pass; resolve
  the "Regenerator/Originator influence" term
- [ ] Digest Milky (league-mechanic/charts farming) + Redviles channel; BawLoch's upcoming Delve/Card/
  Legion/Breach/Abyss videos as they land
- [ ] Lifeforce + oil + logbook prices via `currency_overview` at session time (prices stale in hours)
- [ ] After a strategy is picked: `atlas-planning` session to implement it
