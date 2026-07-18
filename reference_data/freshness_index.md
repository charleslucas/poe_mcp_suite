---
maintained: 2026-07-16
purpose: Model-aware index of PoE mechanics/items/systems that postdate (or are unreliable in) Claude training data, so the running model knows what it must verify rather than answer from memory.
committed: yes (gitignore exception — this is curated, not regenerable)
---

# PoE Freshness Index (model-aware)

This is a **router, not a data dump.** Each entry says *what exists*, *which patch it landed in*, and
*where the real data is* — it does not reproduce the data. The point is to defeat **unknown unknowns**:
the cases where the running model doesn't realize its training is stale and asserts a mechanic confidently
and wrongly.

> **Companion view:** this file is keyed by **patch** (vs the running model's cutoff). For a **mechanic-keyed**
> view — each mechanic's lifecycle and, crucially, its **current scope** (`core` / `challenge-league` /
> `event-only` / `removed` / `disabled-this-league`) — see [`mechanics_index.md`](mechanics_index.md). Use it
> at character pre-flight to **filter mechanics to the character's context** so league/event data doesn't bleed
> into the wrong build (e.g. event-only Forbidden Tattoos must not touch a Mirage or 3.29 character).

## How to use it (the procedure)

1. **Identify the running model.** `mcp__pob__get_context_usage` reports the active model ID. (You may
   already know it from the session.)
2. **Look up that model's training cutoff** in the table below.
3. **Anything in the index with a patch *newer* than the running model's cutoff = MUST VERIFY** before you
   assert how it works. Use the "Where / verify via" pointer (a cached file, a memory, or a fresh fetch).
4. **Entries at-or-before the cutoff** are usually safe from memory, but still defer to live tool data when
   it conflicts (trust hierarchy in `playbooks/README.md` §5). **Exception — the cutoff patch itself is a
   boundary zone:** training ended near that league's *launch*, before the community discovered the nerf
   outcomes, interactions, and consensus builds that constitute most of a league's lessons. A model
   "current through 3.26" knows 3.26's patch notes, not its lessons — verify load-bearing claims *at* the
   cutoff patch too, not just past it.
5. This check is most load-bearing **when about to assert how a mechanic works, or evaluate a unique /
   node / item's *current* stats** — it does not need to run at every step of an analysis, only at the
   stages where patch-specific knowledge is the input.
6. **Feedback loop:** when live data contradicts something the running model asserted from memory — the
   exact event this index exists to prevent — add or annotate the relevant entry here (or in
   `mechanics_index.md`) before moving on. The index should accrete exactly the facts models actually get
   wrong; caught failures are better curation signal than guesses about what to include.

> **Maintenance triggers:** (a) the league-transition playbook Step 7 at each league roll; (b) the
> session-start hook's **game-patch signal** for mid-league point releases (it watches the game exe's
> mtime and points at `patch_notes_index.md` when a patch lands). Update `maintained:` whenever you touch
> this file.

> **Removals count as much as additions.** A *removed* mechanic breaks old assumptions just as hard as a
> new one — e.g. Ancestral totems removed (3.25), the "increased Item Quantity" gear affix removed (3.25).
> "It isn't listed as newly added" ≠ "it still works the way you remember." When a model recommends a
> mechanic from memory, that mechanic still existing is itself a freshness claim.

## Model training cutoffs (PoE patch)

| Model | Cutoff patch | Approx date | Notes |
|---|---|---|---|
| **Opus 4.8** (`claude-opus-4-8`) | **3.26** Secrets of the Atlas | Jan 2026 | Best PoE meta knowledge of current models |
| **Sonnet 4.6** (`claude-sonnet-4-6`) | **3.25** Settlers of Kalguur | Aug 2025 | Default for analysis; stale on 3.26+ |
| **Haiku 4.5** (`claude-haiku-4-5`) | **≤3.24 (unconfirmed)** | — | ⚠ cutoff not documented — treat conservatively; verify anything 3.25+ |
| **Fable 5** (`claude-fable-5`) | **3.26** reliable; **3.27** nominal-but-thin | Jan 2026 | Calibrated 2026-07-08 by in-session self-probe (contamination-aware: tested for detail *beyond* the loaded caches, not mere recognition). Deep 3.25–3.26 (produced Faustus currency exchange, merc subdue→recruit — absent from our caches); **zero independent 3.27 detail → verify-first**; blind 3.28+. Only current model with training knowledge of the original **Feb-2025 Legacy of Phrecia event** (Idols; the 19 alt ascendancies, low per-node detail). PoE recency ≈ Opus 4.8 — its edge is reasoning, not fresher game data. **Subscription access ends 2026-07-12** (an earlier "retired 2026-07-07" note here was wrong — user confirmed live access 2026-07-08). |

> Current league is **3.28 Mirage** — past EVERY model's cutoff. **3.27** is past every model's *reliable*
> window (Fable holds it nominally but with thin detail — still verify). **3.26** is within Opus/Fable, past
> Sonnet 4.6/Haiku. When in doubt, verify.

> **Model not in this table** (new, experimental, or short-lived): treat its PoE cutoff as unconfirmed —
> verify anything 3.25+ from live sources until a calibrated row is added. Never assume a newer model
> implies a newer PoE cutoff.

> **Cutoff rows are calibrated estimates, not vendor guarantees** — they come from probing models against
> known league facts. Knowledge density thins sharply approaching each cutoff (see procedure step 4's
> boundary-zone rule). If a model flunks a fact its row says it should know, tighten the row and note it.

---

## Source bookmarks (quick reference)

The wiki **league page** (mechanic overview + unique/gem tables) and **Version X.Y.0 page** (full patch
notes / balance changes) for each recent league. Fetch via `mcp__poemcp__fetch_wiki_page`.

> For **official forum patch-note threads** and **granular point releases / hotfixes** (X.Y.0a..z — which
> the wiki usually doesn't have per-release), see [`patch_notes_index.md`](patch_notes_index.md). The wiki
> Version pages below are the consolidated transcription; the forum threads there are GGG's primary source.

| Patch | League page | Version (patch notes) |
|---|---|---|
| **3.29 Curse of the Allflame** | https://www.poewiki.net/wiki/Curse_of_the_Allflame_league _(pending)_ | **Forum (primary):** https://www.pathofexile.com/forum/view-thread/3985332 · wiki https://www.poewiki.net/wiki/Version_3.29.0 _(pending)_ |
| 3.28 Mirage | https://www.poewiki.net/wiki/Mirage_league | https://www.poewiki.net/wiki/Version_3.28.0 |
| 3.27 Keepers of the Flame | https://www.poewiki.net/wiki/Keepers_of_the_Flame | https://www.poewiki.net/wiki/Version_3.27.0 |
| 3.26 Secrets of the Atlas | https://www.poewiki.net/wiki/Secrets_of_the_Atlas | https://www.poewiki.net/wiki/Version_3.26.0 |
| 3.25 Settlers of Kalguur | https://www.poewiki.net/wiki/Settlers_of_Kalguur | https://www.poewiki.net/wiki/Version_3.25.0 |
| — all patches — | | https://www.poewiki.net/wiki/Version_history |

---

## Index entries

### 3.29 — Curse of the Allflame  (launches 2026-07-24; past ALL models' cutoffs → always verify / use cache)
Full cache: [`reference_data/leagues/curse_of_the_allflame_3.29.md`](leagues/curse_of_the_allflame_3.29.md) —
**pre-launch, from the 2026-07-16 patch notes**; its **drill-down ledger** tracks per-line depth/confidence.
Videos + community surveys not yet ingested; wiki not yet populated.

| Mechanic / item / system | What it is (one line) | Where / verify via |
|---|---|---|
| **League mechanic: seafloor Voyages** | Valerie/The Sovereign — dive the ocean floor under Allflame lantern light; Charts→Voyages; ship-heart item-split (keep one ghost outcome); **Ducats** warp items. ⚠ "Allflame" here ≠ the 3.24 Allflame Embers corpse item | cache §Mechanic |
| **🔴 GEM SOCKET REWORK (core)** | Any gem fits any socket colour; +10% quality on colour match; sockets default WHITE; Chromatics force one non-white socket. **All recolouring/off-colour intuition is stale** | cache §Rule changes #1 — VERIFY exact rules before advising |
| **Minions never pause while attacking** | All non-spectre minions — explicit big DPS gain (zombies/skeletons/SRS/golems) | cache §Minion balance |
| **Spectre life nerf** | "No Spectre should have more life than a Meatsack" | cache §Minion balance |
| **Triad Grip reworked** | Converts per **socketed gem colour** (empty socket→Chaos), not socket colour | cache §Minion balance |
| **Abyss / Legion / Talisman revamps** | Pre-opened soul-fed pits + Abyss boss; Legion Crystals of Permutation; Talismans = enchantments, uncorrupted | cache §Rule changes #4-6 |
| **Mercenaries → core + Luminary (Scion)** | Act 3+; wagered duels; mercs don't count as party members; Luminary ascendancy hires permanently | cache §Rule changes #7 |
| **New gems** | 4 "Pact of X" Exceptional skills; Coursing Currents + Crystalfall Exceptional supports; Mana-Infused Staff; 4 Str/Int transfigured (incl. Divine Blast of Radiance) | cache §New content |
| **15 new uniques / 3 div cards / Pearlescent Amulet / 2 Bloodline classes** | Counts only — names not in notes | cache ledger (headline — enumerate via wiki/videos) |
| **Absolution cast 0.75→0.65s; Companionship/Communion supports; Maw of Mischief mana-efficiency** | Minion-line balance details | cache §Minion balance |
| **Ascendancy changes = exactly 5 classes** (Assassin, Hierophant, Inquisitor, Occultist, Reliquarian) | ✅ verified 2 sources — **Necromancer/Deadeye/Guardian explicitly UNCHANGED**. New: Luminary (Scion, permanent mercs) + 2 Bloodline classes (one league-exclusive, unenumerated). **Reliquarian = Scion asc (3.28); notables copy unique-item mods, roster swaps EVERY league. ✅ Full 3.29 roster (23 notables) VERIFIED 2026-07-17 (OCR'd from notes' images)** — minion nodes Femurs of the Saints / Arakaali's Fang; defensive copies Kaom's Roots / Presence of Chayula / Melding | cache §Reliquarian roster |
| **Bifurcated Critical Strikes (new keyword)** | Crit chance rolled twice — either roll crits; both → extra crit damage doubled; lucky/unlucky per roll; always-crit prevents it. Introduced via Assassin's Mystical Infusion | cache §Ascendancies |
| **Atlas Anomalies (new endgame system)** | Manifest on the Atlas after Voidstone maps; no map item / no Atlas-tree / no fragments; Cadiro shop, Mana Forge, relocated Nameless Seer + Reflecting Mists (now anomaly-only; scrying → new Scrying Orb) | ✅ CONFIRMED in notes' Endgame section (2026-07-17) — cache §Content-reveal |
| **Luminary (Scion ascendancy) + merc system** | ✅ nodes VERIFIED verbatim (poewiki, 2026-07-17). **Mercenary-COMMANDER class, NOT a player-minion class** — every minion node = "Your Mercenary and *their* Minions" (the merc's), ZERO "your Minions" scaling. Permanently hire up to 3 mercs (1 active); mercs = character-like life + built-in DR, scale off FLAT stats, have a hidden internal tree. Kit: Legendary Arms / Oath of Fealty / Golden Glory / Loyal Bodyguard / Bestowed Knighthood | cache §Luminary nodes |
| ⚠ **Launch datetime (7/24 vs "July 25" NZT)** | Reveal says July 25; anchors say 7/24 — likely timezone. Confirm before trusting either | cache §Reconciliations |

### 3.28 — Mirage league  (past ALL models' cutoffs → always verify / use cache)
Full cache: [`reference_data/leagues/mirage.md`](leagues/mirage.md).

> ### 🔴 END OF LEAGUE — Mirage does **NOT** go core in 3.29 (GGG end-of-league post, read 2026-07-16)
> **Mirage ends 2026-07-20, 3PM PDT.** This is the authoritative "what goes core" answer the league-transition
> playbook (Step 7.2) waits for — re-scope `mechanics_index.md` from it. GGG's stated outcomes:
>
> | Thing | Fate after 7/20 |
> |---|---|
> | **The Mirage league mechanic itself** (Djinn → Mirage sub-zones) | ❌ **NOT going core** → scope `removed`. Everything gated behind it (Djinn coins, Essence of Desolation, Volatile Vaal Orb, Mirage-exclusive drops) goes with it. |
> | **Astrolabes** | ✅ **stays core** (was Mirage-introduced *Atlas* content) |
> | **Exceptional Support gems** | ✅ **stays core** |
> | **Transfusion Support** | ⚠ **no longer obtainable from Divination Cards** (existing copies presumably persist; new supply dies) |
> | **Maps with Empowered Mirages covering the entire map** | ❌ **not openable in Standard** (dead maps) |
> | **Black Baryas** | ⚠ **existing ones usable, no way to obtain more** → legacy/finite |
>
> ⚠ **Modelling note:** the rows in the table below are `challenge-league` scope and become **`removed`** at
> league end EXCEPT Astrolabes / Exceptional Supports (→ `core`). Don't recommend a Mirage-gated lever
> (e.g. **Djinn coins** — see `[[mirage-djinn-coins]]`) to any Standard or 3.29 character after 7/20.
> **Not yet answered here:** whether Screams of the Desiccated / dual-form uniques / Heroic Tragedy / The
> Unseen Hand persist as legacy drops — the post didn't say; verify at the transition.

| Mechanic / item / system | What it is (one line) | Where / verify via |
|---|---|---|
| **Mirage league mechanic** | Free a Djinn → enter a "Mirage" sub-zone that duplicates the map's league mechanics for exclusive drops | `leagues/mirage.md` |
| **Djinn coins** | Mirage currency: Power/Skill/Knowledge = free random support on a lvl-20 gem; Restoration/Desecration = dual-form unique swap | `leagues/mirage.md` → Djinn Coins; `[[mirage-djinn-coins]]` memory |
| **Essence of Desolation** | New essence (from Essence inside a Mirage) → slot-specific bonus reforge | `leagues/mirage.md` |
| **Screams of the Desiccated** | Belt rolling a shrine-buff-while-flask-free; Saresh version rolls two | `leagues/mirage.md` + `shrines.md` |
| **The Unseen Hand (Nameless bloodline)** | Grants a **3rd ring slot** — PoB correctly shows Ring 1/2/3; not an error | `leagues/mirage.md` + `[[...]]` |
| **Mirage dual-form uniques** | Fleshrender↔Skysunder, Desecrated↔Sacred Chalice, etc. (Maraketh/Afarud profiles) | `leagues/mirage.md` |
| **Heroic Tragedy** | Timeless Jewel — **Kalguur** line (not Karui); same mechanic, different conversions | `leagues/mirage.md` |
| **Volatile Vaal Orb** | Mirage currency: rerolls unique mod values OR destroys it | `leagues/mirage.md` |
| **Crucible is ABSENT in Mirage** | No Crucible furnaces/atlas nodes; existing Crucible weapon mods can't be re-applied | `leagues/mirage.md` |

### Return of the Ancestors — event league (concurrent with 3.28 Mirage, ~2026-06-25 → 07-16)
Full cache: [`reference_data/leagues/return_of_the_ancestors.md`](leagues/return_of_the_ancestors.md). A
**time-limited (~3-week) fresh-start event** on the 3.28 client — surfaced in the 3.28.0j patch notes. You
**make NEW characters** for it: **nothing transfers in from Mirage, nothing transfers out to 3.29** (event
characters migrate to Standard at the end). So **existing Mirage characters and the 3.29 build plans are
unaffected** — the entries below apply **only to characters made inside the event.** For those,
**normal ascendancy intuition does not apply.** ⚠ Time-boxed — expires when the event ends (~2026-07-16);
verify it's still running before applying.

| Mechanic / item / system | What it is (one line) | Where / verify via |
|---|---|---|
| **Phrecian alternate ascendancies (forced, the 19)** | **Binary swap**: the normal 19 ascendancies are replaced by a parallel set of 19 alternates for the event (3 per class + Scion 1). Event-only — these alternates don't exist in core play. Every event character runs one; normal ascendancy intuition doesn't apply. Full list in cache. | `leagues/return_of_the_ancestors.md` |
| **Forbidden Tattoos** (event-exclusive) | **Not class-restricted** — splice another class's random ascendancy notable onto your tree; shared limit 1; can strategically disable unwanted ascendancy passives. Deleted on migration. | `leagues/return_of_the_ancestors.md` |
| **Trial of the Ancestors (ToTA) returns** | Re-enabled via drop-anywhere **Silver Coins** → Halls of the Dead tournament; ToTA rewards/tattoos farmable | `leagues/return_of_the_ancestors.md` |

### 3.27 — Keepers of the Flame  (past ALL models)
Cache: [`leagues/keepers_of_the_flame_3.27.md`](leagues/keepers_of_the_flame_3.27.md). Breach-sequel expansion (2025-10-31).
| Mechanic / item / system | What it is (one line) | Notes |
|---|---|---|
| **Bloodline Ascendancy classes** | New ascendancy classes | ⚠ origin of **The Unseen Hand → 3rd ring slot** (seen in Mirage). Unfamiliar ascendancy / extra slot → suspect a Bloodline |
| **Assassin rework** | Shadow/Assassin ascendancy changed | old Assassin intuition stale |
| **Breach overhaul** | New Breach art/encounters/bosses/rewards (Hiveborn) | Breach farming/atlas strategy |
| **New gems** | Conflagration, Thunderstorm, Kinetic Fusillade/Rain, Wall of Force; supports **Windburst, Kinetic Instability, Living Lightning** | the 3 supports are the Djinn-coin blacklist entries (cross-ref Mirage) |
| **Full passive refund (char + atlas) with Gold** | Respec is cheap now | don't assume regret-orb scarcity when advising tree changes |
| **Spectres auto-revive on new instance**; async trading; Vaal Orb replaces Remnant of Corruption | QoL that changes workflow assumptions | — |

### 3.26 — Secrets of the Atlas  (past Sonnet/Haiku; within Opus)
Cache: [`leagues/secrets_of_the_atlas_3.26.md`](leagues/secrets_of_the_atlas_3.26.md). Additive endgame expansion + major crafting.
| Mechanic / item / system | What it is (one line) | Notes |
|---|---|---|
| **Shaper's / Elder's Exalted Orb** | Add Shaper/Elder influence + a new influenced mod to a rare | Influence crafting is accessible again |
| **Memory Strands** (Orb of Remembrance / Unravelling / Intention) | New **mod-tier-upgrade** crafting path on bases | Relevant to "improve this rare" |
| **Runegrafts** | Currency applied to an **allocated passive Mastery** to replace it with a Runegraft effect (NOT a gear enchant — corrects earlier cache). One per *type*, no cap on total → can graft several masteries. Notable: **the Fortress** (+40% global def, −10% attr), **Gemcraft** (+1 all non-exceptional supports), **Restitching** (40% of crit damage taken recouped as life), **the River** (20% chance to full-heal on reaching low life). **Farmed via Kingsmarch shipments** to Kalguuran ports (Riben Fell DEX / Pondium INT / Kalguur STR / Any). Removable via Orb of Scouring. | ✅ confirmed live in 3.28 Mirage (wiki 2026-06-16). ⚠ **trust the [wiki Runegraft page](https://www.poewiki.net/wiki/Runegraft)** — third-party blogs (e.g. aoeah) list only a partial/"all new" subset and miss the Any-pool ones (Fortress/Gemcraft) |
| **Recombinator now core** | Mid-game crafting tool, permanent | — |
| **Animate Guardian keeps its items on death** (3.26.0) | AG's equipped items are **no longer destroyed when it dies** (pre-3.26: permanently lost) — it just can't be resummoned in the same area it died in. Kills the old "AG death = lose your gear" risk framing. Also (stable, oft-forgotten): items with socketed gems **cannot be animated**, and the AG **cannot use skills from gems or item-granted skills** — sockets/gems are inert; only item *mods* + "nearby allies" auras (Leer Cast, Dying Breath) matter. | wiki [Animate Guardian](https://www.poewiki.net/wiki/Animate_Guardian). ⚠ **Boundary-zone miss:** Opus 4.8 (cutoff *at* 3.26) confidently asserted the OLD delete-on-death rule 2026-07-10 — proof of procedure step 4 (verify load-bearing claims *at* the cutoff patch, not just past it). Relevant to the 3.29 Holy Relic Necro (AG is core there). |
| Betrayal/Syndicate revamp; Veiled Chaos Orb back; Legacy of Phrecia ascendancies; Allflame Embers; Kalguuran Scarabs | endgame/crafting/farming systems | see cache |

### 3.25 — Settlers of Kalguur  (past Haiku; at Sonnet cutoff; within Opus/Sonnet)
Cache: [`leagues/settlers_3.25.md`](leagues/settlers_3.25.md). Mechanic integrated to core in 3.26.
| Mechanic / item / system | What it is (one line) | Notes |
|---|---|---|
| **Gold currency + Kingsmarch + shipments** | Semi-AFK income layer; gold spent on town ops | economy planning |
| **Runes / Runesmithing** | Extra rune-mod enchant layer on gear (→ Runegrafts in 3.26) | gear crafting |
| **Melee rework — Ancestral totems REMOVED** | Melee rescaled, scales with gem level; no more Ancestral Protector/Warchief | ⚠ don't recommend ancestral-totem buffing |
| **"increased Item Quantity" removed from gear** | IIQ is no longer a gear affix | ⚠ breaks old MF-gearing assumptions |
| **Warden replaced Raider**; Gladiator reworked; Tinctures back | ascendancy/skill changes | — |

---

## Training-data corrections (NOT league-gated — unreliable across models regardless of cutoff)
These are things models commonly get wrong from training noise, independent of patch:

| Correction | Pointer |
|---|---|
| **No player-accessible training dummy exists** — don't suggest "test on a dummy" | `[[poe-no-training-dummy]]` memory |
| **Eldritch implicit pools differ by slot** (e.g. no "reduced mana cost" on body) — check before promising a mod | `reference_data/eldritch_implicits/` |
| **Shrine buff effects** (Diamond ≠ ailment immunity, etc.) | `reference_data/shrines.md` |

---

## Gaps / to research
- [x] **3.25 Settlers** detail cache → `leagues/settlers_3.25.md` (2026-06-16).
- [x] **3.26 Secrets of the Atlas** detail cache → `leagues/secrets_of_the_atlas_3.26.md` (2026-06-16).
- [x] **3.27 = Keepers of the Flame** (Breach sequel, 2025-10-31) — detail cache → `leagues/keepers_of_the_flame_3.27.md` (2026-06-16).
- [ ] **3.28 Mirage atlas tree nodes** — `leagues/mirage.md` notes the GGG export predated release; refresh when available.
- [x] **Fable 5** cutoff calibrated 2026-07-08 (see model table; subscription access ends 2026-07-12).
- [ ] Confirm **Haiku 4.5** training cutoff (still a conservative placeholder).
- [ ] Confirm **Sonnet 5** (`claude-sonnet-5`) cutoff — in active session use since 2026-07 but has no row; until calibrated, treat per the model-not-in-table rule above.

## Maintenance
- Add a row whenever a session surfaces a mechanic/item the running model got wrong or didn't know.
- At each **league transition** (see `playbooks/league-transition.md`), add the outgoing league's entries here and start the new league's row.
- When a new Claude model ships, add its cutoff to the model table.
