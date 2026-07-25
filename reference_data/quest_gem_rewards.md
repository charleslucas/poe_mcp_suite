---
fetched: 2026-07-24
patch: "3.29"
scope: core
verification: in-game observations (top of trust hierarchy) accreted as characters level
---

# PoE Quest → Gem Rewards & Vendor Unlocks (verified-as-we-go)

**Purpose:** the objective, **class-general** fact of *which quest unlocks which skill gems* — as a quest
**reward** (offered once, from a town NPC) and/or a **vendor** unlock (purchasable afterward). This is the
game-data layer that per-character leveling plans (`character_data/**/progression.md`) reference, so a plan
never again says "buy X at level N" when X is actually **quest-gated**.

**Why this file exists:** gem availability is gated by **quest completion, not character level** (a gem's level
number is only its *use* requirement). This trips up leveling plans built from memory — e.g. SRS is a lvl-4 gem
but does **not** appear until you finish *Breaking Some Eggs*. Quest reward gems aren't cleanly in PoB/the client
export we mirror, so — like [`vendor_recipes.md`](vendor_recipes.md) — this is curated from **in-game
observation + wiki**, committed (useful to every clone), and **accreted as we verify each quest live**.

**Trust marking:** ✅ = confirmed in-game (char · class · patch · date). ◐ = from wiki/web, not yet seen live
(verify when you hit that quest). Reward pools are **class-specific** — always record the class.

**Global shortcut — Siosa (Act 3, The Library):** after the quest *A Fixture of Fate*, **Siosa sells every gem
available up to your level**, regardless of class or which rewards you took. **After Act 3, gem *availability*
stops being a constraint** — buy anything you missed. So this file matters most for **Acts 1–2**.
⚠ **But not *literally* everything** — a few supports unlock only via a *later*-act quest and are absent from
Siosa's Act-3 stock (verified 3.29): **Unleash Support** requires the **Act 4 *Eternal Nightmare*** quest.

---

## Act 1

| Quest | Location | Reward NPC | Class | Gems it unlocks (reward and/or vendor) | Verified |
|---|---|---|---|---|---|
| **Breaking Some Eggs** | Mud Flats | **Tarkleigh** | Witch | **Summon Raging Spirit**, **Frostblink** | ✅ AfWednesdayWeatherwax · Witch · 3.29 · 2026-07-24 |
| Enemy at the Gate | Twilight Strand (kill Hillock) | Tarkleigh / Nessa | Witch | level-1 starters (incl. **Raise Zombie**) | ◐ web — verify |
| The Caged Brute (**Brutus**) | Prison | Tarkleigh / Nessa | Witch | level-8 **supports** (incl. **Minion Damage**, **Melee Splash**) | ✅ AfWednesdayWeatherwax · Witch · 3.29 · 2026-07-24 |
| *(other Act 1 quests — The Dweller of the Deep, The Marooned Mariner, The Siren's Cadence …)* | | | | *add as verified* | — |

## Act 2
| Quest | Location | Reward NPC | Class | Gems it unlocks | Verified |
|---|---|---|---|---|---|
| *(Intruders in Black, Sharp and Cruel, The Root of the Problem …)* | | Yeena / Greust | Witch | *add as verified* | — |

## Act 3
| Quest | Location | Reward NPC | Class | Gems it unlocks | Verified |
|---|---|---|---|---|---|
| **A Fixture of Fate** | The Library | **Siosa** | all | **buy MOST gems up to your level** (see shortcut + Unleash caveat) — verified by buying Feeding Frenzy / Anger / Desecrate here | ✅ AfWednesdayWeatherwax · Witch · 3.29 · 2026-07-25 |
| *(Lost in Love, Sever the Right Hand, A Fixture of Fate …)* | | Clarissa / Siosa | Witch | *add as verified* | — |

## Acts 4–10
| Quest | Location | Reward NPC | Class | Gems it unlocks | Verified |
|---|---|---|---|---|---|
| **Eternal Nightmare** | Act 4 (Highgate) | Petarus & Vanja / reward | all | **Unleash Support** — gated here; **NOT** in Siosa's Act-3 stock | ✅ AfWednesdayWeatherwax · Witch · 3.29 · 2026-07-25 |

*After Act 3 / Siosa, availability is mostly moot — but record later-quest-gated gems (like Unleash above) that
surprise the plan.*

---

## Objective campaign milestones (class-independent — handy alongside gem timing)
- **Skill points from quests:** Acts 1–2 ≈ 4 · full campaign ≈ 18–24 (plus 2 from the bandit quest). *(exact
  per-quest breakdown — add as verified)*
- **Bandits** (Act 2, *The Deal with the Bandits*): Kill All = **2 passive points**.
- **Labyrinth / Ascendancy:** Normal ~lvl 33 (after 6 Act 1–3 trials) · Cruel ~55 · Merciless ~68 · Uber ~75+.
- **Resistance penalties:** **−30% all res on completing Act 5** (Kitava) and **another −30% on Act 10** (Kitava).

## How to extend
When a character completes a quest and sees its gem reward list, add/confirm the row here with a ✅ and the
char·class·patch·date. Flip ◐ → ✅ as each is seen live. Cross-referenced from `progression.md` and
`playbooks/character-leveling.md`.
