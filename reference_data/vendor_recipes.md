---
fetched: 2026-07-24
patch: "3.29"
source: poewiki.net/wiki/Vendor_recipe_system (page version-history to 3.28.0) + community survey 2026-07-24
scope: core
---

# PoE Vendor Recipes — curated reference

**Why this file exists / where the data comes from:** vendor recipes are **server-side game logic** — the
"these items → this output" table is NOT in the client `Bundles2`, NOT in PoB, and NOT in the text lake
(unlike mods/skills/tree, which are datamined from the client). GGG has never published the recipe table, so
the **PoE Wiki** ("Vendor recipe system"), community-tested in-game, is the authoritative source. This is a
curated subset of it — committed (gitignore exception) because it's useful to every clone and barely changes.
Re-verify against the wiki + patch notes at each new league.

> ⚠ **STALE-KNOWLEDGE WARNING — the old "+1 gem" ring recipe is GONE.**
> The recipe many guides *still* cite — `magic/rare weapon + coloured ring + Alteration/Transmute → +1 to Level
> of all [element] Skill Gems` — **no longer grants gem levels.** 3.8.0 changed it to *added elemental damage to
> spells* (and removed the Chaos variant); 3.21.0 **deleted that too**. There is no ring-based gem-level recipe
> and no "add increased elemental damage" vendor combo. Use the quality-gem recipes below.

---

## ⭐ Leveling-relevant (the ones you actually use in the campaign)

### +1 gem levels (current, quality-gem based)
"Modify existing item" recipes — add the mod to an existing item, keeping its sockets/links/quality/ilvl.
**Fractured and corrupted items can't be used.** Two-hand versions *can* roll +2 but the recipe always yields
+1 (Divine-reroll upward). Result is always **+1**.

| Output mod | Inputs |
|---|---|
| ⭐ **"+1 to Level of all Minion Skill Gems"** (helmet) | `Normal Helmet` + `2+ quality gems, combined ≥40% quality, all with the **Minion** tag` |
| **"+1 to Level of all Fire Spell Skill Gems"** (weapon) | `Normal Rune Dagger / Sceptre / Staff / Wand` + `2+ quality gems, ≥40% combined, all **Fire** tag` |
| "+1 to Level of all Cold Spell Skill Gems" | same weapon + `2+ quality gems ≥40%, **Cold** tag` |
| "+1 to Level of all Lightning Spell Skill Gems" | same weapon + `2+ quality gems ≥40%, **Lightning** tag` |
| "+1 to Level of all Physical Spell Skill Gems" | same weapon + `2+ quality gems ≥40%, **Physical** tag` |
| "+1 to Level of all Chaos Spell Skill Gems" | same weapon + `2+ quality gems ≥40%, **Chaos** tag` |

- Weapon must be a **Rune** Dagger (not a generic dagger), Sceptre, Staff (not warstaff), or Wand.
- The weapon variants grant "**Spell** Skill Gems" (spell-only); the **helmet** variant grants "**Minion** Skill
  Gems" (all minion gems, not spell-restricted). **For a minion build the helmet is the money recipe.**
- 💡 *For this SRS build:* SRS is a **Fire Spell** *and* a **Minion** gem, so it benefits from **both** the
  Minion helmet and the Fire-Spell weapon. Bank a few 20%-quality junk gems of the Minion / Fire tags to feed these.

### Early leveling utility
| Output | Inputs |
|---|---|
| ⭐ **Ruby / Sapphire / Topaz Ring** (res rings) | `Iron Ring` + `1 red / green / blue gem` (respectively) |
| ⭐ **Onyx Amulet** (all-attributes) | `any Amulet` + `1 red + 1 green + 1 blue gem` (works on a corrupted amulet; result uncorrupted, keeps influence) |
| **Movement-speed boots** (10%, or +5% tier upgrade) | `Normal boots (or Magic/Rare with a MS mod) + Quicksilver Flask + Orb of Augmentation` → Magic boots, MS one tier up (max Tier 2 = 30%) |
| **%increased Physical Damage** on a weapon | `Weapon + Blacksmith's Whetstone + Rustic Sash` (Magic sash = higher tier, Rare = highest) |
| Amulet base swaps | Amber+Lapis+Transmute→Agate; Jade+Lapis+Transmute→Turquoise; Amber+Jade+Transmute→Citrine |

---

## Gem quality & level
| Output | Inputs |
|---|---|
| **Gemcutter's Prism** | `1 gem ≥20% quality` **OR** `several gems (any rarity) ≥40% combined quality` (each 40% set = 1 GCP) |
| **20% quality Level 1 support gem** | `1 Level-20 non-Awakened support gem + 1 Gemcutter's Prism` (⚠ 3.23: no longer works with **skill** gems — supports only) |
| Decrease gem level by 1 | `1 gem + 1 Orb of Scouring` (not corrupted) |
| Reset gem to level 1 | `1 gem + 1 Orb of Regret` (not corrupted) |

## Sockets & links
Single item with the socket pattern; **listed in priority order** (highest applies if multiple match):
| Output | Condition | Priority |
|---|---|---|
| **20× Orb of Fusing** | 6 linked sockets | 1 |
| **1× Chromatic Orb** | one link containing R + G + B | 2 |
| **7× Jeweller's Orb** | 6 sockets (any links) | 3 |
| **1× Jeweller's Orb** (downgrade) | `1 Orb of Fusing + 1 Chromatic Orb` | — |

## Quality → currency (each 40%-combined set yields exactly 1)
`1 Normal item ≥20% quality` **OR** `several items (any rarity) ≥40% combined quality`, of one category →
Armour→**Armourer's Scrap**, Weapon→**Blacksmith's Whetstone**, Jewellery→**Catalyst**, Flask→**Glassblower's
Bauble**, Gem→**Gemcutter's Prism**. *(Map quality / Cartographer's Chisel recipe was **removed** in 3.28.)*

## Currency — full rare sets (currency = LOWEST ilvl in the set)
A full set = every equipment slot (helmet/body/gloves/boots/belt/amulet/2 rings + weapon config; no flasks/quiver).
Unided **or** all-20%-quality doubles output; both triples it.
| Output | Lowest ilvl |
|---|---|
| 1× Orb of Chance | 1–59 |
| ⭐ **1× Chaos Orb** | **60–74** |
| 1× Regal Orb | 75–100 |

Other set recipes: **Exalted Orb** = full set of same-influence rares (1 ided / 2 unided); **2 same-name rares**
→ Chance, **3** → Alchemy (all-quality → Regal); **Straight Flush** (normal+magic+rare same base) → Augmentation
(unided/quality scale to Alchemy); +unique → 5× Chance.

## Other useful currency
| Output | Inputs |
|---|---|
| **Vaal Orb** | `7 Vaal skill gems + 1 Sacrifice fragment` (or any Uber-Atziri unique) |
| **Orb of Augmentation** | `1 rare with six affixes` |
| **Orb of Scouring** | `1 rare with exactly 2 affixes` |
| **Essence upgrade** | `3 Essences same type & tier` → 1 of next tier up |
| **Transmutation Shards** | magic unided item → 2; rare unided → 5 (20 = 1 Transmute) |
| **Divine Orb** | `1 Mirror of Kalandra` (the only Mirror "recipe") |
| Tier-up stacks | `3× same {map / oil / catalyst / net / tattoo(same tribe) / idol}` → 1 tier up / random of type; `3× scarab` → 1 random *different* scarab |

## Flasks
- **Hybrid Flask:** `1 Orb of Fusing + 1 Life Flask + 1 Mana Flask`.
- **Upgrade flask base:** `3× same-base Life/Mana/Hybrid Flask` → next base type (up to Sanctified L50; not Divine/Eternal).
- **Jade / Granite Flask:** `3× Ruby/Sapphire/Topaz Flask each with a "%inc Evasion (Jade) / Armour (Granite) during Effect" mod`.

---

## 3.29 changes (Curse of the Allflame)
- **Socket colours reworked** (verified — see [`leagues/curse_of_the_allflame_3.29.md`](leagues/curse_of_the_allflame_3.29.md) §Gem sockets): any gem fits any colour; sockets default White; matching colour only = +10% quality. **Bench R/G/B socket options & Harvest "reforge → White" REMOVED; Vorici benches repurposed; Omen of Blanching → Omen of Trichromatism.**
- **Chromatic Orb no longer purchasable from a town vendor** for 3 Jeweller's Orbs *(community-reported, survey 2026-07-24 — ⚠ verify vs official notes; not in the wiki page whose history ends at 3.28)*. The **RGB-linked-socket recipe still yields a Chromatic** and (per 3.28) sits above the 6-socket Jeweller's recipe in priority, so you don't accidentally lose it.
- **6-socket (7× Jeweller's) and 6-link (20× Fusing) recipes: unchanged.** **Chaos recipe (60–74 rare set): unchanged.**

## Provenance / re-verify
Primary: poewiki.net/wiki/Vendor_recipe_system (Anubis-walled — fetch via Playwright, not plain WebFetch).
The Minion-helmet form dates to 3.19; the old ring→gem-level recipe removed 3.8/3.21. Re-verify the 3.29
chromatic-purchase line against the official patch thread once the wiki updates past 3.28.
