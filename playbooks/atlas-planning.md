# Playbook: Atlas Planning

For Claude sessions where the user wants to optimize their Atlas passive tree allocation, choose which mechanics to run, identify which map modifiers to avoid, and select best map layouts. Load this playbook in full at the start of the task.

Triggers: "atlas advice", "what atlas nodes should I run", "which mechanics should I farm", "what maps should I avoid", "map mod blacklist", "which maps are good for my build".

---

## Step 0 — Frame the work for the user

One sentence: *"Using the Atlas Planning playbook — I'll check the build for dangerous mods, then cross-reference with your farming goal to recommend atlas nodes and map layouts."*

Narration norms:
- State which data sources you're loading and why before fetching them.
- When the atlastree export is stale or missing the current league cluster, say so explicitly and note the gap in `reference_data/leagues/{league}.md`. Do not silently skip it.
- If the Mirage (or any current-league) cluster is absent from the export, tell the user: *"The atlas export doesn't have the [league] cluster yet — I can recommend the permanent nodes that synergize with it, but you'll need to check the league cluster in-game."*

---

## Step 1 — Triage

Deliver these via `AskUserQuestion` before loading any data. Skip questions answerable from prior conversation context.

**Q1 — Farming goal** (gates which mechanics to prioritize)
- Juiced T16 mapping (raw drops / div)
- Specific mechanic (Breach, Delirium, Essence, Expedition, Ritual, etc.)
- Bossing / Uber progression
- General / willing to reallocate

**Q2 — Dangerous mod awareness** (gates build analysis depth)
- User lists known mods to skip → skip the build analysis, go straight to cross-reference
- "Not sure — figure it out from the build" → do the full build analysis (Steps 2a + 3a)

**Q3 — Juicing level** (gates atlas node depth)
- Actively juicing (scarabs + sextants) → include synergy nodes for juicing setup
- Not yet / minimal → focus on base mechanic nodes only

---

## Step 2 — Data loads

### Always load
| Source | Tool | Why |
|---|---|---|
| Character meta + build | `Read character_data/{account}/{char}/meta.json` + `mcp__pob__lua_get_stats` (category='all') | Core mechanic, damage type, leech reliance, resistances |
| League reference | `Read reference_data/leagues/{league}.md` | Mirage (or current league) mechanic interactions, Mirage cluster gap status |
| Atlas tree (permanent nodes) | `python3` script against `reference_data/atlastree/league.json` — filter by mechanic keywords | Exact node names and stat lines |

### Add if Q1 = specific mechanic
Load the targeted mechanic's node cluster from `atlastree/league.json`. Pull ALL notables + smalls for that mechanic so you can give point-cost breakdowns.

### Add if Q2 = "figure it out from the build"
Pull `mcp__pob__analyze_defenses` for detailed leech/recovery breakdown. Cross-reference damage type against reflect variants.

### Add if Q3 = actively juicing
Also pull current scarab prices via `mcp__poe__ninja_lookup` for the relevant scarab types to assess which mechanic's scarabs are most valuable.

---

## Step 3 — Analysis pattern

### 3a — Build-derived mod blacklist
Work through these categories in order:

1. **Reflect** — What damage type does the build deal? Physical reflect is safe if the build converts phys to elements (like Winds of Fate). Elemental reflect is lethal for elemental builds. Chaos reflect matters if chaos damage is significant.
2. **Leech** — Is the build leech-dependent for life? For mana? A channeled skill (Cyclone, Blade Flurry) that leeches mana is doubly exposed to No Leech.
3. **Max resistance** — Check actual resist values from `lua_get_stats`. Fire < 75%, chaos < 60% → those elements' "extra damage" mods are amplified danger.
4. **Flask reliance** — Does the build rely on flasks for immunity (rather than passive immunity from gear/ascendancy)? "Reduced flask effect" shortens that window.
5. **Damage output gating** — Any mechanic that disables the core skill (e.g., "Cannot deal non-Chaos damage" for a physical build) is a hard skip.

Output: two lists — **Hard Skip** (cannot survive or deal 0 damage) and **Caution** (survivable but risky, manage carefully).

### 3b — Mechanic × build synergy matrix

| Mechanic | Synergy with fast AoE clears? | Mirage interaction? | Risk profile? |
|---|---|---|---|
| Breach | High (AoE into dense packs) | None | Low |
| Delirium | High IF fog persists (The Singular Eternity is mandatory for fast builds) | Refracting Fog (cluster jewel enchant rerolls) | Medium (can spike) |
| Essence | Any build | Essence of Desolation (type-specific bonus mod reforge) | Very low |
| Expedition | Medium (need to manage logbooks) | None confirmed | Low-medium |
| Beyond | High (extra mobs) | Coin of Desecration + Volatile Vaal Orb | Medium-high (beyond bosses) |
| Ritual | Medium (stop-and-fight) | Corpse items | Medium |
| Blight | Low for fast builds (tower placement) | None | Low |

### 3c — Atlas node selection

For each prioritized mechanic:
1. Pull notables from the atlastree export — name them explicitly, include stat lines
2. Identify the 2-3 highest-value notables (density/quantity/unique drops)
3. Note which smalls are on the path
4. Flag any anti-nodes (nodes that explicitly DISABLE the mechanic like Dimensional Barrier, Ominous Silence) — these look like they return points, but take them only if deliberately opting out of a mechanic

### 3d — Best map layouts

Two axes:
- **Tight vs open**: Tight layouts copy more content into Mirage (Dungeon, Cells, Tower, Spider Lair). Open layouts copy less (Beach, Strand, Desert).
- **Pack density for clearing style**: Fast AoE (Cyclone, TS) wants compact layouts with many packs close together. Slow AoE (Spellslinger, RF) can work in more open layouts.

Recommended approach: cross the two lists to find maps that are BOTH tight AND dense. These are the maps to target and sustain.

---

## Step 4 — Output shape

Append to `character_data/{account}/{char}/journal.md` under a new `## YYYY-MM-DD (cont.) — Atlas & Map Analysis` heading. Structure:

```markdown
### Map modifier blacklist
**Hard skip:** [list with one-line reason each]
**Caution:** [list with one-line reason each]
**[Damage type] reflect is [SAFE/LETHAL] because [reason]**

### Atlas node changes
**KEEP — [Mechanic]:** [notable list]
**ADD — [Mechanic] ([why]):** [notable list]
**SCALE BACK — [Mechanic]:** [reason]

### Best map layouts
**Run:** [list]
**Avoid:** [list]
```

Also update `reference_data/leagues/{league}.md` → Atlas tree section with any new node data pulled from the export (fill gaps, add synergy tables).

---

## Step 5 — Pitfalls

**Data source pitfalls**
- The atlastree export at `reference_data/atlastree/` is typically a preview (pre-release). League-specific clusters are often absent until GGG publishes the full release export weeks after league launch. Check `git log --oneline` in the atlastree dir to confirm which version you have. If the league cluster is missing, say so — do not hallucinate node names.
- Always pull node stat lines from the actual export data, not from memory. Node effects change between leagues. The stat lines in the export are authoritative.
- Screaming Whispers is a Breach notable that boosts **Simulacrum Splinters**, not breach monster density. Don't confuse it with Breach DPS nodes.
- Torn Veil and Dimensional Barrier are anti-nodes (Torn Veil = Beyond, Dimensional Barrier = disable breach). Both look like "Breach" nodes by keyword but are not density nodes.

**Build analysis pitfalls**
- Physical reflect safety depends on HOW the damage conversion happens. Winds of Fate converts phys → element at the SOURCE (before hit). Other conversion mechanics may differ — always verify the conversion point.
- A build with "cannot be leeched from" ascendancy or keystone (e.g., Iron Will, specific uniques) is immune to No Leech maps IF the build doesn't rely on leech. Check ascendancy before flagging No Leech as a hard skip.
- Chaos resistance below 60% combined with Chaos damage map mods + Chaos-damage league monsters is underrated danger. Note chaos res from `lua_get_stats` and mention it.

**Mechanic pitfalls**
- Delirium fog and fast-moving builds: Cyclone, Tornado Shot, and other movement-heavy skills can literally outrun the fog, losing all delirium progress. **The Singular Eternity** (fog persists longer) is mandatory before investing heavily in Delirium for fast builds.
- Breach Hives require a different sub-strategy than standard Breaches (Hive Fortress objectives, Ailith waves). Don't recommend Hive-specific notables (Protracted Siege, Fortified Dominance) unless the user is specifically farming Hive content.
- MapStash API (as of 2026-05-21): GGG has not finished the API for reading MapStash contents. `get_tab` returns `mapLayout: {}` and `items: []` regardless of actual contents. Cannot programmatically read the user's map inventory. Confirmed in GGG dev Discord. See `reference_data/poe_api.md`. Check back ~2026-11.
