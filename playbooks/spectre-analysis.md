# Playbook: Spectre Analysis

Choose, measure, and correctly *model* spectres for a minion build. Exists because PoB's spectre handling
has one non-obvious behaviour that silently invalidates the naive approach — measuring a spectre by adding
it and re-reading DPS gives **zero change**, which reads as "no effect" but usually means "not selected".

**Triggers:** "which spectre should I use", "what spectres help my build", "is spectre X worth buying",
"my spectres aren't doing anything in PoB", any minion build whose PoB numbers look lower than in-game.

---

## Step 0 — Frame the work

*"Spectre analysis — data sweep → model correctly → measure → price. PoB models only ONE spectre's buffs
by default, so the first job is making the model honest."*

Cursory when it's one lookup ("what does a Perfect Guardian Turtle grant?" → text lake, done).
**Detailed** when it decides a purchase or a loadout.

## Step 1 — The two facts that govern everything

1. **Imports NEVER set spectres.** The PoE character API doesn't report raised spectres, so an imported
   build simulates *generic* spectres and misses every buff. Set them with `set_spectres`.
2. **PoB applies a spectre's buffs only when it is the selected minion of a Raise Spectre skill instance**
   ([`CalcPerform.lua:2169`](../PathOfBuilding/src/Modules/CalcPerform.lua#L2169) — it collects
   `activeSkill.minion.type` per Raise Spectre instance, then applies buffs only for spectres in that list).
   One Raise Spectre gem ⇒ **exactly one** spectre modeled, whichever is selected (the first by default).
   Every other raised spectre is inert in the calc.

   ⚠ **A null result therefore means nothing.** Adding a spectre and seeing no change (to seven decimals)
   is the expected output for a *non-selected* spectre — it is indistinguishable from a broken mod. This
   cost a wrong "the MonsterTag condition is broken" conclusion on 2026-08-09 before the position test.

## Step 2 — Data loads

| Load | Purpose |
|---|---|
| `rg --no-ignore "grants:" reference_data/text_lake/spectres.txt` | 268 spectres, tags + skills + granted mods |
| `PathOfBuilding/src/Data/Spectres.lua` (raw entry) | **conditions the lake's `grants:` column drops** |
| `PathOfBuilding/src/Data/Minions.lua` | your minions' `monsterTags` — decides which tagged buffs apply |

⚠ **The lake's `grants:` column is lossy in both directions.** It flattens away conditions
(`MonsterTag`, `PerStat`) — making mods look better than they are — and it omits **auras, which live in the
`skills:` column**. The Perfect Guardian Turtle's Determination (+2,761 armour on a live build) is a skill,
not a mod: `grants:` shows only its 5% phys reduction. Read the raw Lua entry before believing either column.

## Step 3 — Model it correctly (the modeling group)

To model N spectres at once, give PoB N Raise Spectre instances, each pinned to a different spectre via the
per-gem XML attribute `skillMinion` (GUI: Skills tab minion dropdown; no MCP tool sets it).

1. `set_spectres([...])` — every spectre you want modeled must be in the list (the buff loop checks
   membership).
2. Add an **unassigned** socket group (no `slot=`), `includeInFullDPS="false"`, holding one Raise Spectre
   gem per *additional* spectre, each with `skillMinion` **and** `skillMinionCalcs` set to its metadata id.
   - **Unassigned matters**: weapon-swap groups are inactive while the main weapon set is live, so gems
     parked there contribute nothing (a build carrying spare Raise Spectre gems in a swap slot is not
     already doing this).
   - **`includeInFullDPS="false"` matters**: it keeps the fake instances from adding spectre *damage*.
     Verify with `minion_dps_breakdown` — there must be exactly **one** Raise Spectre row.
3. `lua_save_build` → edit XML → `lua_load_build`.
   Reference implementation: `scripts/pob_spectre_modeling_group.py`.

⚠ **Character import destroys the modeling group** (import replaces skill gems). Re-add it after every
import — it belongs in the post-import checklist alongside Full-DPS flags and SRS count.

⚠ **Metadata ids are not guessable.** "Perfect Hulking Miscreation" is `.../SpecialCorpses/RobotArgusHigh__`
— trailing double underscore. Always copy the id from the text lake, never construct it.

## Step 4 — Measure

- To value **one** spectre: list it **first**, measure, then compare against a run with a *different*
  spectre first. Never compare against "absent", which conflates the buff with the selected spectre's own
  damage.
- Confirm the gain landed on the **buffed minion's row** in `minion_dps_breakdown`, not the spectre's own
  row. (Worked example: the Miscreation's own damage was 5,846 = 0.27%, so a +658k jump was genuinely the
  SRS buff.)
- Defensive buffs need `lua_get_stats` on *defence*, and minion life/ES/res appear in **no readout** —
  in-game observation only.

## Step 5 — Gate and price

- Obtainability: league corpse spectres (`LeagueAzmeri/SpecialCorpses/`) are **tradeable items**, searched
  by `base_type` — **not** `name` (that's for uniques, and it silently returns an unfiltered 10,000).
  poe.ninja does not track them, so `price_check` returns nothing; bracket with `search_trade`'s
  `max_price` instead. Non-corpse spectres must be found and raised in a map — free but not purchasable.
- Judge fit by what the build actually scales: a `PlayerModifier` boosting *player* attack damage is
  worthless to a minion build, while a tagged `MinionModifier` may be enormous — check the tag against your
  minions' `monsterTags` first (SRS are `construct` **and** `skeleton`; zombies are `undead`).

## Step 6 — Pitfalls (all field-hit 2026-08-09 unless noted)

- **Null result ≠ no effect** — see Step 1. The single most expensive trap here.
- **PoB can over-credit too.** With the Judgemental Spirit modeled, PoB gave the player +529 ES from its
  Discipline; the character sheet in game read the *unbuffed* value. Trust hierarchy: in-game beats PoB.
  Treat a modeled total as an **upper bound** until spot-checked against the character sheet, and remember
  PoB assumes permanent aura uptime while the game needs the spectre alive and in range.
- **"It does nothing" claims must be re-tested after correct modeling.** The Judgemental Spirit was written
  off as contributing nothing measurable; once selected it turned out to grant flat fire/chaos damage to
  `Skeleton`-tagged minions — a large SRS buff, and chaos feeds poison.
- **PoB models one spectre's damage, not the swarm's** — the Raise Spectre row shows the *selected*
  spectre only. A mixed zoo's real damage is higher than any single number PoB will show.
