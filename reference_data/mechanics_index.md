---
maintained: 2026-11-17
purpose: Mechanic-keyed registry of PoE mechanics/systems — each one's lifecycle (introduced → changed → removed/returned) and, critically, its CURRENT SCOPE, so analyses can filter mechanics to a character's actual context and not bleed league/event data into the wrong build.
committed: yes (gitignore exception — curated, complements freshness_index.md)
---

# PoE Mechanics Index (mechanic-keyed + scope-tagged)

A **mechanic-keyed** companion to the **patch-keyed** [`freshness_index.md`](freshness_index.md). Same
underlying facts (detail lives in `leagues/*.md`), different axis:

- `freshness_index.md` answers *"given the running model, what must I verify?"* (patch vs model cutoff).
- **This file** answers *"what is the current **state** and **scope** of mechanic X, and how did it get
  there?"* (mechanic lifecycle). It is the **source of truth for a mechanic's status/scope**; freshness rows
  can stay terse and point here.

**Why mechanic-keyed:** every league adds one or more mechanics and usually removes/disables/nerfs others.
A league-keyed view fragments a single mechanic's history (Runegrafts span 3.25→3.28; Trial of the Ancestors
is a 3.22 league that's now a 2026 event). Tracking per-mechanic keeps each one's lifecycle and **current
availability** in one place.

---

## ⚠ Compartmentalization rule (the point of the scope tags)

**Before applying any mechanic to a character, check its Scope against that character's context.** At
character pre-flight (see `playbooks/README.md` §2c), establish: which **league/realm** is the character in,
and is it an **event** character? Then:

> **Only consider mechanics whose Scope includes the character's context.**
> A `challenge-league` mechanic does not exist for a Standard character. An `event-only` mechanic does not
> exist for a normal league character. A `removed` mechanic does not exist at all. A `disabled-this-league`
> mechanic is off right now even though it's normally core.

This is what keeps **Return of the Ancestors** (event-only) from contaminating **Mirage** or **3.29** work,
and **Mirage** mechanics (Djinn coins, etc.) from being assumed present in **3.29**.

### Scope / status vocabulary

> **PoE temporary-league taxonomy** (per the [wiki](https://www.poewiki.net/wiki/League)): *temporary* leagues
> come in two recurring flavours — **challenge leagues** (the ~13–16-week **expansion** leagues: Mirage 3.28,
> Keepers 3.27, Settlers 3.25… — new mechanic + expansion + challenges; characters migrate to **Standard** at
> end) and **event leagues** (shorter, also recurring: **Legacy of Phrecia / Return of the Ancestors**, races,
> Mayhem, Endless Delve… — characters migrate to **Standard or Void** at end) — plus private leagues. So
> "Ancestors" is precisely an **event league**, a *sibling* of the Mirage challenge league, not a challenge
> league itself. **Both kinds are fresh-start, temporary, and RECUR**, so the tags below cover both and you
> **re-scope at every transition (challenge OR event)**.

| Tag | Meaning | Example |
|---|---|---|
| `core` | Permanent; present in all leagues incl. Standard | Recombinator, Runegrafts |
| `challenge-league` | Only in the named **challenge (expansion) league** (~13–16 wk); gone next league unless cored | Djinn coins (Mirage 3.28) |
| `event-only` | Only during a specific **event league** (short, recurring; sibling to challenge leagues) | Forbidden Tattoos / Phrecian ascendancies (Return of the Ancestors) |
| `removed` | Taken out of the game | Ancestral totems |
| `disabled-this-league` | Normally core, but off in the current league | Crucible (absent in Mirage) |
| `nerfed` / `reworked` | Still present but materially changed | Assassin rework (3.27) |

> **Current context anchors (update at each league roll):** current challenge league = **3.30 Covens of Umbra**
> (`Covens`; launched **2026-11-13** PST; end date not yet announced). **POE_LEAGUE = Standard** (the user's
> main character is in Standard) → Covens `challenge-league` rows below do **not** apply to it; the 3.30 **core**
> changes do. ~~3.29 Curse of the Allflame~~ **ENDED 2026-11-09 1PM PST** — league mechanic **did not go core**
> (wiki League_mechanics); its block below is re-scoped per the 3.30.0 notes (2026-11-17). ~~3.28 Mirage~~ ended
> 2026-07-20 but was **made core in 3.30.0** — ex-Mirage block re-scoped. ~~event league Return of the
> Ancestors~~ **ENDED 2026-07-16** — its event-only mechanics `removed`. Sources: 3.30.0 notes (forum 4013680 /
> wiki Version_3.30.0); cache `leagues/covens_3.30.md`.

> **Canonical enumeration sources (two complementary views):**
> - Mechanic-keyed: [`League_mechanics`](https://www.poewiki.net/wiki/League_mechanics) — **every league
>   mechanic, active and removed, with its lifecycle** ("removed in X.Y.0", "not added to core", "replaced
>   in X.Y.0"). Seed new entries at league transitions (league-transition playbook Step 4.3) and audit this
>   file for missing removals — it's how we'd catch a mechanic that quietly left the game without an entry
>   here recording it.
> - League-keyed: [`League`](https://www.poewiki.net/wiki/League) — every league ever run, with **exact
>   start/end dates + release version**, each linking to a per-league detail page listing what was active
>   (mechanics, uniques, monsters) in that league. The authoritative source for the context-anchor dates
>   above and for reconstructing a past league's context (e.g. a Standard character built during Settlers).

---

## Active mechanics

| Mechanic | Scope | Introduced → lifecycle | Current state (one line) | Verify / detail |
|---|---|---|---|---|
| **Runegrafts** | `core` | 3.25 Runes → 3.26 Runegrafts → 3.27 (Recompense→Refraction rename) → live 3.28 | Currency applied to an allocated passive **Mastery** to replace it (one per type, no total cap); farmed via Kingsmarch shipments | `freshness_index.md` (3.26 row); wiki Runegraft page |
| **Recombinator** | `core` | League mechanic → cored 3.26 | Permanent mid-game crafting tool (combine two items' mods) | `leagues/secrets_of_the_atlas_3.26.md` |
| **Gold / Kingsmarch / shipments** | `core` | 3.25 Settlers → cored 3.26 | Semi-AFK gold income; town ops; shipments source Runegrafts | `leagues/settlers_3.25.md` |
| **Memory Strands** (Remembrance/Unravelling/Intention) | `core` ⚠verify | 3.26 | Mod-tier-upgrade crafting path on bases | ⚠ confirm it persisted past 3.26; `leagues/secrets_of_the_atlas_3.26.md` |
| **Shaper's / Elder's Exalted Orb** | `core` ⚠verify | 3.26 | Add influence + a new influenced mod to a rare | ⚠ confirm persistence; 3.26 cache |
| **Bloodline ascendancies / The Unseen Hand (3rd ring slot)** | `core` ⚠verify | 3.27 Keepers | Alt ascendancy classes; Unseen Hand grants a 3rd ring slot (seen on Mirage chars) | ⚠ confirm core vs league; `leagues/keepers_of_the_flame_3.27.md` |

> **Note — Legacy of Phrecia alternate ascendancies are NOT core.** The 19 "Phrecian" alternates exist
> *only* during Ancestor/Phrecia events — see the `event-only` row below. In normal/core play the standard
> 19 ascendancies are the only set.

## 3.30 Covens of Umbra — challenge-league mechanics (launched 2026-11-13; CURRENT league)
League-gated: these exist **only for characters in the Covens leagues**, not Standard. Re-scope at the 3.31 roll.
Source: 3.30.0 notes (forum 4013680) + wiki Wickerman / League_mechanics → cache `leagues/covens_3.30.md`.

| Mechanic | Scope | Current state | Verify / detail |
|---|---|---|---|
| **Fates** (covenite cauldron rites) | `challenge-league` (3.30) | Kill covenites → pick up to 3 Fates for the area boss (difficulty + reward); repeat copies triple rewards (0b HF3). Grim Fates on pinnacle/uber bosses. 0d: Divine/Annulment rewards need 2 copies; Depraved Trinity is the only boss with the Covens empowerment. 0c: empowerment damage reduced; Savage/Pestilent/Sadist extra bosses always drop their Viscera; new high-tier chase rewards | cache §League mechanic |
| **Viscera + Wickerman** | `challenge-league` (3.30) | Fate-empowered bosses drop Viscera (lesser/normal/greater; pinnacle; Coven Queen's Crown); 4 slots on a per-character town Wickerman, stats snapshot per instance. **Not equipped items** (0b HF4). Stash-tab affinity + vendor recipe (0c). Minion lines incl. +1–2 max Skeletons/Zombies, minion double damage, minions gain % of your res | cache §League mechanic; wiki Wickerman |
| **The Coven Queen** (boss; key: Cursed Poppet) | `challenge-league` (3.30) | League pinnacle; drops Coven Queen's Crown | cache §League mechanic |
| **Doedre's Tongue drop source** | `challenge-league` (3.30) for new drops | Now drops **only** from Covens encounters (buffed values; existing copies Divine-able) | cache §League mechanic |
| **11 new uniques / Mycelium Core / Arcane Link / Fireball of Radiation / Essence of Trickery** | `core`? ⚠verify | Notes add them under "New Content" without saying league-exclusive (gems/essence/jewel base read as core; uniques may be league-drop-only until cored) | cache §New items |

## 3.30 core changes (apply to ALL leagues incl. Standard — new 2026-11-13)

| Mechanic | Scope | Current state | Verify / detail |
|---|---|---|---|
| **Threads** (replace Scarabs) | `core` (new 3.30) | 10 types + Frayed Thread; ≤8 per map at the device; the 10 primary mechanics now **only** appear via Threads / Shaped Regions. 0c: per-league bonus stat at 3/6/8 Threads; guaranteed Thread mods 1/2/3 at 1–3/4–7/8+ Threads; Thread vendor recipe | cache §Core #1 |
| **Atlas passive tree** | `core` **reworked 3.30** | Centre-start, 150 pts, league clusters rebuilt, 6 keystones removed, Phantom Anomalies added | cache §Core #2 |
| **Shaped Regions / Astrolabes** | `core` **reworked 3.30** | 10 region types granting free Threads; Astrolabes place one; Templar/Fruiting/Deceptive astrolabes removed | cache §Core #3 |
| **Item generation (Item Tiers, Atlas Drops, rarity pools)** | `core` **reworked 3.30** | Tiered magic/rare drops; IIQ → Atlas Drops on maps; rarity picks better pools; tier-gated bases | cache §Core #4 |
| **Mirage** | `core` (cored 3.30) | Tertiary mechanic in maps (+ Act 9 desert/oasis); see ex-Mirage block below | cache §Core #5 |
| **Soul Cores** (Knowledge/Power/Skill + Finesse/Instability/Intellect/Might) | `core` (new 3.30) | Corrupt a lvl-20 gem → imbue a random support (may be a "bad" one); Temple of Atzoatl / Atziri sources | cache §Core #5–6 |
| **Atziri in the Temple of Atzoatl / Royal Visage / Twice Corrupted** | `core` **reworked 3.30** | Alluring Abyss + Sacrifice/Mortal fragments gone; Altar of Corruption & Lapidary Lens → Twice Corrupted | cache §Core #6 |
| **Harvest (Sacred Flora)** | `core` **reworked 3.30** | In-map flora, no Sacred Grove subarea | cache §Core #7 |
| **Beyond (Demonic Evocator, demonic realms)** | `core` **reworked 3.30** | — | cache §Core #7 |
| **Gwennen "Take a Chance"** | `core` (replaces gambling) | Pay Astragali + Broken Circle Artifacts for one of 3 crafting-option pairs on a rare | cache §Core #7 |
| **Delirium Orbs reforge maps** | `core` **reworked 3.30** | Delirious % map mod instead of enchant | cache §Core #7 |
| **Allflame Embers (3.24 item)** | `core` **reworked 3.30** | Map currency enchantments (not fragments); 3 new | cache §Core #8 |
| **Divine Vessels** | `core` **reworked 3.30** | Currency → "Deified" maps; stack 20 | cache §Core #8 |

## 3.29 Allflame — ex-challenge-league mechanics (❌ ENDED 2026-11-09; re-scoped 2026-11-17 from the 3.30.0 notes)
The 3.29 **league mechanic did not go core** (wiki [League_mechanics](https://www.poewiki.net/wiki/League_mechanics):
"Curse of the Allflame did not go core"; no GGG end-of-league post on this was found — 3.29.3d notes only mark the
end + migration). The 3.29 *core* changes (sockets, minions, Abyss/Legion/Talisman revamps, mercs, anomalies) stay.
Source of the original rows: patch notes 2026-07-16 → `leagues/Allflame.md`.

| Mechanic | Scope (post-2026-11-09) | Current state | Verify / detail |
|---|---|---|---|
| **Allflame seafloor Voyages** (Valerie/The Sovereign/Charts/Bathysphere) | `removed` (was `challenge-league` 3.29) | Wiki: did not go core. 3.30 notes only mention Sovereign hideout decorations. ⚠ NOT the 3.24 "Allflame Embers" item (that one is core and reworked in 3.30) | wiki League_mechanics; `leagues/Allflame.md` (historical) |
| **Allflame crafting bench / Dead Man's Sulphur / Ducats** | `removed` (league-gated) — **except Merrick's Ducat** | 3.30 notes: Merrick's Ducat now usable on Abyss jewels "without the need for Allflame Crafting" and has a new source (Abyss×Mercenary synergy, per wiki) → Merrick's Ducat `core`; other Ducats / the bench: `removed?` — notes silent, verify in-game | cache §Allflame crafting (historical) |
| **Gem socket colour system** | `core` **reworked 3.29** 🔴 | Unchanged by 3.30 apart from a new bench option to set all sockets White (Orb of Scouring) | `leagues/Allflame.md` §Gem sockets |
| **Minion attack pausing** | `core` **removed 3.29** (buff) | Non-spectre minions never pause while attacking — persists | cache §Minion balance |
| **Spectre life** | `nerfed` 3.29 (core) | Capped ~Meatsack level — persists | cache §Minion balance |
| **Abyss** | `core` **reworked 3.29 → again 3.30** | Now a Thread/Shaped-Region-only primary mechanic; Alluring Abyss removed from Atlas | covens cache §Core #1 |
| **Legion** (Enshrouding Crystals / Crystal of Permutation / Vestigial uniques) | `core` | Persists (wiki League_mechanics lists Enshrouding Crystals + Vestigial uniques as Legion rewards); 3.30 adds **Afarud Enshrouding Crystal** (quivers, from Miraged Legion); Thread-only spawning | cache §Vestigial uniques |
| **Talismans** | `core` (reworked 3.29) | Obtainable from Bestiary (red) beasts — persists | wiki League_mechanics §Talisman |
| **Mercenaries of Trarthus + Luminary (Scion)** | `core` | Persists; 3.30 merc nerfs (less late dmg/DR, res penalty by area level) + Luminary Golden Glory halved; Mercenaries now a "secondary" mechanic | covens cache §Balance |
| **Triad Grip** | `reworked` 3.29 (core) | Socketed-gem-colour conversion — persists | cache §Minion balance |
| **Atlas Anomalies** | `core` (new 3.29) | Persists; 3.30: Templar Vaults are now anomalies; spawn chance lowered by monsters left alive at boss kill; Phantom Anomalies keystone | covens cache §Core |
| **Nameless Seer + Reflecting Mists** | `reworked` 3.29 (anomaly-only) | Reflecting Mist now storable in the Currency tab (3.30); anomaly-only status otherwise unchanged ⚠verify | — |
| **Vestige uniques** (= Vestigial uniques, Legion) | `core` (new 3.29) | See Legion row; "Vestige" was the reveal-video term | cache §Reconciliations #2 |
| **Pact of X Exceptional gems** (Ghorr/Beidat/K'tash/Lycia) + Coursing Currents / Crystalfall supports | `core`? | 3.30 balances Pact of Beidat + fixes Ghorr's Magnificence → gems still exist. Whether new copies still drop outside the league: notes silent — verify in-game | covens cache §Balance |
| **3.29 Bloodline classes** (Saresh / Velka / Abyssal selection UI) | `core`? ⚠verify | 3.30 fixes the Saresh/Velka/Abyssal Bloodline selection UI → still selectable; which were league-exclusive: notes silent — verify in-game | `leagues/Allflame.md` |
| **Pearlescent Amulet** (base) | `removed?` | Notes silent — verify in-game | — |
| **Craicic Chimeral → Croaker rename** | `core` (permanent rename 3.29) | — | freshness 3.29 row |

## Ex-Mirage mechanics (league ended 2026-07-20 → ✅ **MADE CORE in 3.30.0**, re-scoped 2026-11-17)

> The July end-of-league post said Mirage would NOT go core; **3.30.0 reversed that** ("Mirage as a Core League").
> Mirage is now a *tertiary* core mechanic. Coins of Restoration/Desecration were deleted; the Knowledge/Power/
> Skill coins were rethemed as Soul Cores. Re-scope history: `challenge-league` (3.28) → `removed` (2026-07-20)
> → `core` (3.30.0).

| Mechanic | Scope | Current state | Verify / detail |
|---|---|---|---|
| **Mirage sub-zones** | `core` (cored 3.30) | Mirages now cover the whole map (tertiary; can be forced by a rare-map suffix); Black Barya in all leagues (area lvl 84); Saresh fight much harder | covens cache §Core #5 |
| **Djinn coins — Restoration / Desecration** | `removed` (deleted on login, 3.30) | Dual-form unique swap gone; Djinn wish Sigils re-purposed | covens cache §Core #5 |
| **Djinn coins — Knowledge / Power / Skill** | `core` as **Soul Cores** (3.30) | Same imbue effect, plus a chance of a "bad" support; sourced from the Temple of Atzoatl | covens cache §Core #5–6 |
| **Essence of Desolation** | `core` (3.30) | On the Currency Exchange + Essence tab | covens cache §Core #5 |
| **Screams of the Desiccated** (belt) & Maraketh dual-form uniques | `core` (3.30) | Mirage uniques required for Unique Stash completion; Restored Maraketh uniques drop from Astral monsters / Ridan in Mirages. Screams' shrine buffs no longer work on mercs | covens cache §Core #5 |
| **Volatile Vaal Orb** | `core`? ⚠verify | 3.30 removes the Beyond-in-Mirage source; other sources not stated | covens cache §Core #5 |
| **Heroic Tragedy** (timeless jewel — Kalguur line) | `core` (3.30, nerfed) | Drops from Olroth + Peaceful Moments / The Eternal War cards; Starlight Swig / Regenerative Runes / Celestial Mathematics nerfed | covens cache §Core #5 |
| **Transfusion Support** | `core`, **reworked 3.30** | Obtainable again from Exceptional-support div cards; now grants minion charges per 400 life spent | covens cache §Balance |

## Event-only mechanics (Return of the Ancestors — ❌ ENDED 2026-07-16, all `removed`)
> 🔴 **The event ended 2026-07-16 3PM PDT.** Every row below is now `removed` — it does NOT exist for any live
> character (Mirage, Standard, or 3.29). Event characters migrated to Standard **lose these** (Forbidden Tattoos
> deleted; the Scavenger/Phrecian ascendancy gone → an ascendancy-less Scion). Kept here as history + as the
> re-scope record. ⚠ ToTA is the one to watch: it's *recurred* before (base-game 3.22, this event) — if it
> returns to core or a future event, re-scope it then; don't assume "removed forever."

| Mechanic | Scope (post-2026-07-16) | Current state | Verify / detail |
|---|---|---|---|
| **Forbidden Tattoos** | `removed` (was `event-only`; event ended 2026-07-16) | Deleted on migration to Standard. Gone for all live characters. | `leagues/return_of_the_ancestors.md` (historical) |
| **Phrecian alternate ascendancies (the 19)** | `removed` (was `event-only`; event ended 2026-07-16) | Binary set-swap of the 19 ascendancies — **event-only, now gone**. Migrated Scions/etc. keep the char but lose the alternate ascendancy. Normal ascendancy set applies everywhere else. | `leagues/return_of_the_ancestors.md` (historical) |
| **Trial of the Ancestors (ToTA) return** | `removed` (was `event-only`; event ended 2026-07-16) | Silver Coins / Halls of the Dead gone with the event. ⚠ ToTA has recurred before — re-scope if it comes back. | `leagues/return_of_the_ancestors.md` (historical) |

> ⚠ **Event entries are fresh-start & time-boxed.** They apply ONLY to characters made inside the event and
> expire ~2026-07-16. **Nothing transfers in from Mirage or out to 3.29** — so existing Mirage characters and
> the 3.29 build plans must ignore this whole section.

## Removed / disabled / nerfed (do NOT recommend as if present)

| Mechanic | Status | When | Note |
|---|---|---|---|
| **Ancestral totems** (Protector/Warchief) | `removed` | 3.25 | Melee rescaled to gem level; don't recommend ancestral-totem buffing |
| **"increased Item Quantity" gear affix** | `removed` | 3.25 | IIQ no longer a gear mod; breaks old MF-gearing assumptions |
| **Crucible** | `disabled-this-league` | absent in 3.28 Mirage | No furnaces/atlas nodes; existing Crucible weapon mods can't be re-applied |
| **Runegraft of Recompense** | `reworked`→Refraction | 3.27 | Renamed; effect changed to fork/chain/+1 projectile |
| **Assassin / Raider** | `reworked` / replaced | 3.27 Assassin rework; 3.25 Warden replaced Raider | Old ascendancy intuition stale |
| **Scarabs** (incl. Veiled Scarabs, Maven's Chisel of Scarabs, Skittering Delirium Orb) | `removed` → Threads | 3.30 | Auto-converted to Threads / Frayed Threads; chisel + orb renamed to Thread versions |
| **Random spawning of the 10 primary league mechanics in maps** (Abyss, Bestiary, Betrayal, Breach, Blight, Expedition, Incursion, Legion, Ritual, Ultimatum) | `removed` | 3.30 | Only via Threads / Shaped Regions now. Smuggler's Caches + Sulphite only in marked maps |
| **Atlas keystones** Crop Rotation, Endless Tide, Lucid Dreams, Meticulous Appraiser, Refiner's Bargain, Synthesised Stability; Delve/Heist atlas clusters; Vaal-side-area atlas stats | `removed` | 3.30 | Atlas tree rebuilt |
| **Templar / Fruiting / Deceptive Astrolabes** | `removed` | 3.30 | Converted to Cryptic Astrolabe |
| **Alluring Abyss; Sacrifice & Mortal fragments; Vaal side areas in maps; Vial drops** | `removed` | 3.30 | Atziri moved into the Temple of Atzoatl; Mortal → Royal Visage; existing Vials/Sacrifice fragments inert |
| **Orb of Binding** | `removed` (unobtainable; existing still work) | 3.30 | Bestiary recipe now makes Orbs of Regret |
| **Gwennen gambling** | `replaced` → Take a Chance | 3.30 | — |
| **Yellow-beast capture** (Bestiary) | `removed` | 3.30 | Existing yellow beasts deleted; recipes no longer need them; lures useless |
| **Harvest Sacred Grove subarea** | `reworked` → in-map Sacred Flora | 3.30 | Tutorial quest removed |
| **Fragmented Delirium Orb** | `removed` | 3.30 | → Threaded Delirium Orbs |
| **Item Quantity on monster mods / map mods / IIQ corruption implicit** | `removed` / → "Atlas Drops" | 3.30 | Rarity raised to compensate |
| **Map corruption "reroll to 8-mod rare"** | `replaced` (+2 mods, max 9) | 3.30 | — |
| **Operative's Strongboxes; Labyrinth identified-items chests** | `removed` | 3.30 | — |
| **Memory Threads** | `renamed` → Memory Traces | 3.30 | Avoid confusion with the new Threads |
| **Divination cards disabled** (Her Mask, Last Hope, Sambodhi's Vow, Buried Treasure, Cameria's Cut, Man With Bear, More is Never Enough, The Card Sharp, The Deal, The Rabbit's Foot, The Silly Boy) | `disabled-this-league` | 3.30 | "Temporarily disabled" per notes |
| **Harbingers** | `removed` | 3.28 | Per wiki League_mechanics |

---

## Maintenance
- **At each league roll:** re-scope. Challenge-league mechanics of the outgoing league → either `removed`/
  gone or promoted to `core` (if cored). Add the incoming league's new mechanics. Update the "context anchors."
- **At event start/end:** add/expire `event-only` rows.
- **When a mechanic changes:** append to its lifecycle and update its current-state line + scope tag here
  (this file is the status source of truth); keep the freshness/league files pointing here.
- Resolve `⚠verify` tags by checking the wiki / live tools when the mechanic next becomes load-bearing.
