> **Canonical home:** `poe_mcp_suite/frameworks/` (public). Instance data is patch-stamped (3.29) — re-verify after any league/patch change. `local library:` references point into the maintainer's private guide library (character data + digested third-party guides, not distributed); treat them as worked-example citations, not links.

# Style Template: MINIONS

**What this is:** the layer *above* the archetype library — the shared map of minion builds: recognized
options, common infrastructure, staged acquisitions, and known traps. Use it to *design* a minion build
(pick axes → pick archetype → follow the shared spine → diverge where your playstyle wants), then hand off
to a specific `guides/{archetype}/` entry or `build-design.md` for the character itself.

**Confidence labels** (used throughout, per user preference): ✅ verified (sim/in-game/game-data) ·
◐ community-sourced, unverified · ⛔ dead/wrong — kept deliberately so it isn't re-proposed.

**First instance of the style-template idea (2026-08-04).** Shape is provisional; the playbook gets
written once this has survived a couple of real uses.

---

## 1. Decision axes

Pick one from each row; the combination largely determines the archetype.

| Axis | Options |
|---|---|
| **Persistence** | Permanent army (spectres/zombies/skeletons) · temporary swarm (SRS, Animate Weapon) · triggered/hybrid (Holy Relic, Dom Blow, Chains of Command) · immortal crawler (Herald of Agony) |
| **Damage flavor** | Physical/impale · fire · cold · lightning · **chaos/poison** |
| **Player activity** | Zero-button walker → caster upkeep (SRS) → active self-attacker (Holy Relic, Dom Blow, HoAg) |
| **Defense chassis** | Life+block engine (✅ see §3g) · ES/hybrid · life-regen stacking · "minions are the defense" (Meat Shield walls, turtle windows) |

---

## 2. Archetype roster

### In the library (analyzed — start from these entries)
| Archetype | Flavor / persistence | Entry |
|---|---|---|
| **Poison SRS Necromancer** | chaos-poison, temp swarm | `local library: `poison-srs-necromancer/`` — plus a real character's full history in the maintainer's local character notes |
| **pRAW (Poison Ranged Animate Weapon)** | chaos-poison, temp swarm | `local library: `praw-necromancer/`` — ◐ survey consensus: current S-tier poison-minion pick; setup via **Bladefall of Trarthus** (✅ real, already in our entry) |
| **Holy Relic of Conviction** | phys/holy nova, triggered | `local library: `holy-relic-necromancer/`` — ◐ survey: a **Gladiator** variant (Determined Survivor lucky block) is rising |
| **Turtle spectres** | defensive utility | `local library: `turtle-necromancer/`` — ✅ Guardian Turtle confirmed in the 3.29 spectre roster (`text_lake/spectres.txt`); ⚠ mechanic was hotfixed to ~50% uptime |
| **SRS/Absolution leveling trunk** | shared campaign spine | `local library: `srs-absolution-leveling/`` |
| **Luminary merc summoner** | league-mechanic hybrid | `local library: `luminary-merc-summoner/`` — scope-check league availability |

### Survey-surfaced, NOT yet in the library (◐ — digest a guide before committing)
| Archetype | One-liner | Notes |
|---|---|---|
| **Popcorn SRS** | Minion Instability + Infernal Legion: SRS explode for 33% max life as fire | ◐ "untouched by 3.29 nerfs, reliable starter" |
| **Soulwrest Phantasms** | staff auto-summons phantasms off consumed corpses; CwC Cyclone + Desecrate | ◐ tanky, budget; "Life from Death" cluster sustain |
| **Spectre army** (Frostbearers / Wretched Defilers) | permanent ranged army | ✅ **Congregation Support verified** (Exceptional support, req 72, max lvl 15): **30% → 64% MORE maximum minions** from supported skills — the real deal for any max-count scaling. Spectre choices still ◐ |
| **Chains of Command** | Animate Guardian's weapon spawns animated-weapon copies | ◐ archetype real; ⛔ the claimed "3.29 AG gear-inspection UI" **fails verification** — our league doc's dedicated 3.29 string checks found ZERO Animate Guardian changes; cross-version blending |
| **Dominating Blow / Absolution Guardian** | strike-to-summon sentinels, tanky starter | ◐ |
| **Herald of Agony crawler** | immortal crawler, zero minion management | ◐ survey: niche tank, B-tier; pairs with Cyclone/Ball Lightning virulence stacking |
| **Arakaali's Fang spiders** | on-kill spider swarm, poison | ◐ chase tier with The Squire |
| **Block SRS** (no external guide) | SRS + 66/78 block + auto-triggered offerings | ✅ **live, ours** — the maintainer's live character (local notes); the only fully-verified entry here |

### Directed follow-ups (2026-08-04 — the "absences" resolved; both alive)
| Archetype | Aliases | Verdict |
|---|---|---|
| **Skeleton mages** | "Mage Skelly", "skele mages" | ◐ B-tier mapper, good starter. ⚠ **Freshness catch: Dead Reckoning is NO LONGER the enabler** — the `Summon Skeletons of Mages` transfigured gem does it natively. Variants: Doryani's Prototype lightning; **chaos/poison via conversion gloves** (→ [`minion-fire-to-chaos`](../concepts/minion-fire-to-chaos.md)) |
| **Zoomancer** | "zoo build", "minion army", "walking simulator" | ◐ "Zoo" = **many minion types at once** (70+ active) + zooming mobility. Dominant 3.29 variant: **Chaos Poison Zoomancer** on The Covenant + Ghastly Eyes — the same core our live character runs. Components: Carrion Golem *of the Hordes* (more phys per nearby non-golem — wants a crowd), zombies, Vaal Skeletons on demand, buff spectres (charge-generators), AG with ◐ Asenath's Gentle Touch (curse-explode clear). Creators: GhazzyTV (poe-vault), HelmBreaker (pobarchives) |

| **Golem armies** (Elementalist) | "Golemancer", "golem-stacker" | ◐ Pure minion golems: B-tier chill mapping. The S-tier form is **golems as a BUFF SHELL** — 10+ auto-reviving golems (Liege of the Primordial) scaling the *player's* damage/defence via stacked **Primordial Bond** clusters (◐ ~10% dmg per golem) under Phys-DoT/ignite self-cast builds. Count via Anima Stone, Primordial Chain, Dark Monarch (exclusivity acceptable in a golem-only shell). ⓘ "Minions as player-buffs" is a **tech** — candidate `_concepts/` entry |

---

## 3. Shared infrastructure — what nearly every minion build wants

### 3a. Minion gem levels (✅ the cheapest damage in the game)
Stack `+N to Level of (all) Minion Skill Gems`: wand/sceptre, helmet (+2 tier exists on rares), shield
(+1), Necromancer's **Unnatural Strength** (+2). ✅ Worked example: Raise Spectre 21 gem read 26 effective
(3-spectre breakpoint at gem 25; spectre counts live in the gem's level table, `get_gem_detail`).

### 3b. Darkness Enthroned + Ghastly Eyes (✅)
The belt roughly doubles its 2 socketed Ghastly Eyes (✅ owned copy: 97% increased effect) — belt jewels are
worth ~2× a tree socket. ✅ Poison builds: **poison scales off PHYSICAL and CHAOS damage only** — added
chaos on an eye feeds hit *and* poison; cold/fire/lightning feed only the hit.

### 3c. Offerings + automation (✅ the biggest QoL lever we've found)
Bone (block) / Flesh (speed) / Spirit (regen) Offering, fed by Desecrate. **Automate it**: a wand with the
bench craft *"Trigger a Socketed Spell when you Use a Skill"* fires Desecrate + Offering off your normal
casting. ✅ This single craft enables a 66/78-block chassis with zero extra buttons. Alternative: Mistress
of Sacrifice (offering affects you) if playing that ascendancy node.

### 3d. Defensive supports for permanent minions (✅ in-game verified)
Minions that die constantly usually have **zero defensive supports** — check before buying anything.
✅ Adding Minion Life to zombies+golem stopped repeated wipes outright; spectres/AG want Meat Shield +
Minion Life. ⚠ Minion life/res appear in **no PoB readout** — only in-game observation verifies this.

### 3e. Spectre toolbox by role
Grep the full roster: `rg --no-ignore -i "<tag/skill>" reference_data/text_lake/spectres.txt` (**268**
spectres — tags, skill lists, and a `grants:` column of every player/ally/minion modifier). Roles: damage ·
buffers (◐ "Perfect Spirit of Fortune" utility) · defensive windows (✅ Guardian Turtle). Meat Shield on
defensive spectres makes them taunt/body-block.

**Spectres that buff the PLAYER are rare and worth hunting — only 7 of 268 carry a `PlayerModifier`:**
Guardian Turtle + Perfect Guardian Turtle (3%/5% phys damage reduction), Perfect Druidic Alchemist (**200%
increased flask effect** + life-flask charge generation), Perfect Needle Horror (impale effect), Perfect
Runic Skeleton (5% MORE phys damage), Perfect Slashing Horror (5% phys gained as fire), Perfect Spider
Matriarch (wither effect — ⚠ PoB's own comment says *"Does not work"*). Find them with
`rg --no-ignore "grants:.*PlayerModifier" reference_data/text_lake/spectres.txt`.

⚠ **`grants:` alone under-reports — cross-check the `skills:` column for auras.** The Perfect Guardian
Turtle's biggest gift is *Determination* (✅ measured on a live build: armour 889 → **3,650**, EHP +18.6%),
which lives in its skill list, not its mods; `grants:` catches only its 5% PDR. Conversely a spectre with
`grants:-` may still do nothing for you: the Perfect Judgemental Spirit's Discipline is minion-only —
✅ confirmed in-game 2026-08-09, character-sheet ES matched PoB exactly with it raised.

⚠ **PoB never learns your spectres from an import** (the PoE API doesn't report them), so an unset build
silently simulates *generic* spectres and misses all of the above. Set them with `set_spectres`
(fuzzy names, e.g. `["perfect guardian turtle"]`) — pob-mcp, added 2026-08-09.

### 3f. Auras & reservation
Typical: Anger+Generosity, Skitterbots, Purity of Elements, **Envy via United in Dream** (✅ measured ~87%
of a poison build's damage — dropping it is a build-defining decision, not a tweak). ⚠ Reservation maxes
out fast; ✅ reservation efficiency essentially **cannot roll on rings** (only a corrupted Anger implicit) —
it lives on helmet/body (Essence of Loathing ✅ `essences.txt`) and influenced amulets.

### 3g. Defense chassis notes (✅ hard-won)
- **Block engine** (✅ live): Bone Offering + Rumi's + Tempest Shield + `As The Mountain` **as an anoint** →
  66/78. Auto-generated endurance charges via **Enduring Composure** small cluster (✅ worth 9,553 EHP; PoB
  needs `useEnduranceCharges` set to count it).
- ⛔ **Glancing Blows without an on-block payoff** — ✅ simmed −1,307 EHP (blocked hits deal 65%; 2X×0.35 <
  X). It's the keystone most summoner-block advice assumes. Needs Aegis-style recovery to be worth it.
- ⛔ **MoM + Eldritch Battery on a summoner** — ✅ removed after repeated failure: mana lost to hits = unable
  to summon. **PoB scores MoM as top EHP and is structurally blind to this.**
- ⛔ % increased armour on an ES chest (tiny base); flat armour (Granite flask) is the only armour lever.
- ✅ Hit-fed sustain beats kill-fed: `Flagellant's` flasks / Enduring Composure stay up in the lone-rare and
  boss fights that starve kill-fed charges.

### 3i. Cross-build TECH (→ [`_concepts/`](../concepts/README.md) — the tech database)
Techs are archetype-independent — record them once in `_concepts/` (with **aliases** and **references**)
and link from here. First entry, ✅ realized in-game: **[fire→chaos conversion](../concepts/minion-fire-to-chaos.md)**
(Anger+Generosity flat fire + `Minions convert 100% of Fire Damage to Chaos Damage` gloves → everything
exits as poison-scaling chaos; ✅ **+19.8% measured**; same tech powers skeleton-mage and zoomancer
chaos variants). Trigger-wand offering automation (§3c) is the next candidate to get its own entry.

### 3h. Cluster jewels (✅ mechanics verified)
Minion-damage Large (8-11 passives) → **sockets accept own size or smaller**, chain **Large → Medium →
Small** (max 3 deep). Smalls with `Added Small Passive Skills grant:` enchants are point-efficient (✅
measured ~29-38k DPS/pt on a live build). Full smalls pool: `text_lake/clusters.txt`. Key notables to
watch: ◐ Renewal, Feasting Fiends, Vicious Bite, Blessed Rebirth; ✅ Enduring Composure (defense).

---

## 4. Staged acquisitions (generic minion spine)

| Stage | Get | Confidence |
|---|---|---|
| **A1 (lvl 1-12)** | SRS from **Breaking Some Eggs**; ◐ Sidhebreath amulet; +1 minion wand (vendor recipe: magic wand + Ghastly Eye + Orb of Alteration) | ✅ quest timing banked in `reference_data/quest_gem_rewards.md` |
| **A2-A3 (12-38)** | Bandit: usually Kill All; ◐ Praxis (mana), Bones of Ullr (✅ used), Reverberation Rod (+2 socketed, Spell Echo), Tabula; Siosa (A3) backfills gems | ✅/◐ |
| **A4 (38+)** | **Unleash from Eternal Nightmare** (✅ NOT at Siosa); Normal Lab | ✅ |
| **Campaign tail (55-68)** | Cruel/Merciless Lab; +2 minion helm tier; re-cap res after BOTH Kitava hits (−30% each) | ✅ |
| **Maps entry (68-75)** | Uber Lab; 5L→6L; Darkness Enthroned + 2 good Ghastly Eyes; archetype-defining unique (✅ e.g. United in Dream was 16c at league week 1 — fork-deciders are cheap early) | ✅ |
| **Mid maps (75-90)** | Cluster jewel package; anoint (✅ can carry a 9-pt notable like As The Mountain for one oil set); ◐ The Dark Monarch (spectre/golem count), Soulwrest, Alberon's (str-stack skeletons); The Covenant for poison variants (✅) | ✅/◐ |
| **Endgame (90+)** | ◐ Arakaali's Fang + The Squire (poison chase); ◐ Doryani's Prototype (lightning spectres); awakened supports; AG chase gear | ◐ |

---

## 5. Known traps (all ✅ verified, all cost someone real currency or a death)

1. ⛔ **The Dark Monarch is Wraithlord-class** — ✅ every one of its 16 variants pairs *"Maximum number of
   X is Doubled"* with **"Cannot have Minions other than X"** (`uniques.txt`). Survey advice calls it
   "mandatory for spectre/golem setups" without the exclusivity — it is **mono-minion only** and deletes a
   mixed army (zoo, our block SRS, anything with an AG + zombies). Fine for golem-shells and pure spectres.
2. ⛔ **Wraithlord** — "+1 spectre per socketed Ghastly Eye" *but* "You cannot have Non-Spectre Minions" —
   deletes SRS/zombies/AG on mixed builds.
3. ⛔ **Vis Mortis +1 spectre is legacy-only** (`{variant:1,2}`) — the current item doesn't grant it.
4. ⛔ Veiled `+1 Spectre` prefix is Catarina-only; **not benchable** onto owned gear.
5. ⚠ **PoB group-count conflation**: a socket group holding Raise Spectre *and* Animate Guardian can't have
   its count set without multiplying the AG too — spectre DPS reads low or AG reads absurd.
6. ⚠ **Every import resets**: Full-DPS flags, group counts, pantheon, bandit, charge toggles. Checklist
   before trusting any post-import number.
7. ⚠ Minion stats are invisible: minion life/res in no readout; minion-mod items read "unchanged" in
   import diffs; zombie/golem groups excluded from Full DPS. Judge minion survivability in-game.
8. ⚠ **"In the game data ≠ obtainable"** — gate every find: spawn weight (read *which key* the zero is
   under) → variant → slot legality → market. See `playbooks/gear-shopping.md` pitfall.

---

## 6. Survey ledger

### 2026-08-04 — initial roster + infrastructure discovery (3 queries, Google AI Mode)
- Queries: "best minion summoner builds 3.29 all archetypes" · "minion build essential uniques leveling to
  endgame" · "poison minion builds which options viable HoAg AW SRS". All returned real r/PathOfExileBuilds
  / r/PathOfExileSSF threads (3.29-current).
- **Poison-minion consensus**: pRAW S-tier > poison SRS A-tier (safest starter) > HoAg B-tier (niche tank);
  "Spiders" (Arakaali's Fang) also in the conversation. Core poison gear consensus matches our verified
  stack (The Covenant + United in Dream/Severed in Sleep).
- **Existence-gated** against the text lake: ✅ Congregation Support, Dark Monarch, Soulwrest, Sidhebreath,
  Arakaali's Fang, Guardian Turtle, and ✅ **Bladefall of Trarthus** (pRAW's setup skill — survey garbled it
  as "of the Tarter"; user caught it, and our own `praw-necromancer/` entry already documents the real gem).
  ⚠ **Gate lesson (2026-08-04): an exact-string miss is NOT proof of nonexistence — fuzzy-grep the base name
  ("bladefall") before ruling a name a synthesis artifact.** AI-synthesized sources garble proper nouns
  routinely; the first verdict here was a false ⛔.
- **Known-wrong claims caught**: "United in Dream grants Unholy Might" (✅ our owned copy granted **Envy**
  L25 + 60% poison chance + minion chaos res); "SRS last ~30 seconds" (base is 5s); "Unnatural Strength =
  100% phys-to-chaos conversion" (it's +2 minion gem levels) — cross-version/synthesis blending, standard
  for this source.
- One query-2 source was **r/pathofexile2builds (PoE2)** and another was a 2019 compendium — leveling-staple
  claims are old-but-stable items, kept at ◐.

### 2026-08-04 (later) — directed searches: skeleton mages + zoomancer
- Both "absent" archetypes are alive (rostered above with aliases). Key freshness catch: **skeleton mages no
  longer need Dead Reckoning** (transfigured gem does it natively) — older guides mislead here.
- **Chaos Poison Zoomancer** confirmed as a dominant 3.29 minion variant, built on the exact core our live
  character already owns (The Covenant + Ghastly Eyes + poison scaling) — a zoo pivot would be cheap.
- ✅ **Tech-db validated in the field the same day:** the fire→chaos glove tech (`_concepts/minion-fire-to-chaos.md`,
  banked as an IDEA on 2026-07-19 from a friend's concept) was equipped on the live character (+19.8% measured),
  AND surfaced independently in both directed surveys as the chaos-variant enabler for skeleton mages and
  zoomancer. One tech, three archetypes — the reason _concepts/ is cross-style.

### 2026-08-04 (later still) — verification queue worked
- ✅ **Congregation Support**: Exceptional support, req 72, **30-64% MORE max minions** (lvl 1→15), quality =
  minion MS. Verified via `get_gem_detail`. Big enough to sim on any max-count build.
- ✅ **Dark Monarch**: full mechanics from `uniques.txt` — promoted to trap #1 (mono-minion exclusivity the
  surveys omitted).
- ⛔ **"3.29 AG gear-inspection UI"**: refuted by the league doc's dedicated patch-note string checks.
- ◐ **Golem armies**: rostered — pure golemancer B-tier; the live form is the S-tier *buff-shell* (golems
  scale the player). One garbled league name in the response ("Curse of the Old Flame") — standard synthesis
  noise, ignored.

### Verification queue
- [ ] Gladiator Holy Relic variant — digest a guide (`guide-analysis`) before crediting
- [ ] Popcorn SRS + Soulwrest + Chains of Command — candidate `guide-analysis` targets to fill roster gaps
- [x] Congregation Support price: ✅ **~9 div minimum on trade** (user-checked 2026-08-04) — Exceptional gems
  are chase-tier, consistent with the Pact gems' class. ✅ Drop source (user, from item info): **Incarnation of Dread or Uber Dread** — the Incarnations are the 3.27 pinnacle bosses (league doc: 'new chase-drop sources'). Drop RATE ◐ unknown. Still open: the sim on the live character's SRS 6L (sim BEFORE grinding)
- [ ] "Minions as player-buffs" (Primordial Bond golem shell) — write the `_concepts/` entry
