# Build Profile Format

The build profile is the handoff artifact between design mode and analysis mode. Every analysis playbook (gear-shopping, tree-analysis, build-optimization-sim, dps-analysis) loads this as a prerequisite before making any recommendations.

**Design goals:**
- Structured enough to be machine-readable by Claude in any session
- Compact enough that loading it is cheap (not a 5000-word essay)
- Ages well — stale sections are clearly marked, not silently wrong
- Doubles as community contribution format when anonymized

**Location:** `character_data/{Account}/{Character}/build-profile.md`  
For shared archetypes: `character_data/guides/{archetype}/build-profile.md`

---

## File format

YAML frontmatter for structured fields, markdown sections for content that benefits from prose. The frontmatter is machine-readable; the sections are human+Claude readable.

---

## Template

```yaml
---
# Identity
character: ""            # character name, or archetype name for shared profiles
account: ""              # account name with discriminator, or omit for shared profiles
class: ""
ascendancy: ""
level: 0                 # current level, or target level for design profiles
league: ""               # league name
patch: ""                # PoE patch version (e.g. "3.28")
last_validated: ""       # YYYY-MM-DD — when this profile was last verified against live game state

# Profile type
mode: ""                 # "design" (ideal, may not exist yet) | "analysis" (in-game character)
status: ""               # "active" | "archived" | "abandoned"

# Primary skill and archetype tags (for indexing and relevance matching)
primary_skill: ""
archetype_tags: []       # e.g. ["cyclone", "slayer", "leech", "phys-conversion", "crit"]
---
```

---

## Section 1: Core Mechanics

*How this build actually works. Precise enough that someone unfamiliar with the build can evaluate gear and tree decisions correctly.*

### Damage chain
Trace how damage flows from source to final hit. Include conversion steps, key multipliers, and what damage type(s) the output actually is. This determines which stats scale DPS and which don't.

Example format:
```
Source: [primary skill] deals physical damage
Conversion: [X]% physical → random element (Winds of Fate); [Y]% physical → chaos
Output: mostly elemental + chaos; effectively 0% physical reaching enemies
Key multipliers: critical strike multiplier (non-crits deal 0 damage), elemental damage, crit chance
Does NOT scale with: added flat physical damage bonuses, physical damage taken debuffs on enemies
```

### Sustain source
What keeps the character alive during combat. Be specific about the mechanic and its conditions.

Example format:
```
Primary: life leech from attacks (Slayer ascendancy: elevated leech cap, leech continues on full life)
Condition: must be hitting enemies — leech stops when not attacking
Secondary: life regeneration (Vitality aura, X/sec)
Flask recovery: Seething instant flasks only (belt constraint — see Hard Constraints)
```

### Defensive layers
List defensive mechanics in priority order (most important first).

### Trigger conditions / special states
Any mechanics that only work under specific conditions, or that change the build's behavior when active.

---

## Section 2: Anchor Items

Items the build cannot function without, or that fundamentally define the build's character. Losing these items means the build concept changes, not just that DPS drops.

For each anchor item:
- Name and base type
- Why it's mandatory (what mechanic it enables or enables uniquely)
- What breaks if it's removed
- Whether it can be replaced and with what

---

## Section 3: Stat Priority

Ordered list of stats from most to least important for this build. Used to evaluate gear upgrades — a higher-priority stat is worth more than a lower-priority stat even if the numbers look similar.

Format: ranked list with brief rationale for each.

Example:
```
1. Critical strike multiplier — non-crits deal zero damage; crit multi scales everything
2. Accuracy rating — misses deal zero damage and generate zero leech
3. Life — primary buffer against one-shots
4. Chaos resistance — weakest elemental coverage, only 37%; highest marginal value
5. Elemental damage — scales the entire converted output
6. Attack speed — more hits = more leech = more sustain
7. Fire/cold/lightning resistance — already near cap; marginal overcap has low value
8. Physical damage — already high from staff; marginal value lower than elemental
9. Energy shield — incidental; build is life-based
```

---

## Section 4: Mod Value Overrides

Mods that are worth significantly more or less than generic for this build. Used to correct tier-based upgrade analysis for build-specific reality.

### Worth more than tier suggests
Mods where build mechanics amplify their value beyond what a generic evaluation would show.

### Worth less than tier suggests
Mods that seem valuable by tier but don't actually move the needle for this build.

### Irrelevant or detrimental
Mods that are worthless or actively counterproductive. Don't spend affix slots on these.

---

## Section 5: Hard Constraints

Build-specific rules that override general rules. These are non-negotiable — any recommendation that violates them is invalid regardless of what it does for DPS or EHP.

Format: state the rule, then the reason, then what breaks if violated.

General rules that apply to every character (don't repeat here unless there's a build-specific threshold):
- Elemental resistances ≥ 75% (or applicable cap)
- All gem and gear attribute requirements met
- Mana unreserved > 0

Build-specific hard constraints go here. Examples:
```
- Flask types: Seething (instant) only. Reason: Screams of the Desiccated grants Diamond Shrine
  buff only while no flask effects are active. A duration flask removes the buff for its entire
  runtime. Breaks: the build loses forced 100% crit chance during mapping.
  
- Leech source: at least one life leech mod must be present on gear or tree. Reason: Slayer
  sustain is entirely leech-based. Without a leech source, the character cannot recover life
  during combat. Breaks: character dies to any sustained damage.
  
- Hit chance: must be 100%. Reason: non-crits deal zero damage (Winds of Fate). A miss is
  also zero damage AND zero leech. Below 100% hit chance, damage and sustain both degrade
  simultaneously. Breaks: effective DPS and leech both drop linearly with missed hits.
```

---

## Section 6: Constraint Status

**Tier** defines the threshold and how strictly it must be maintained. **Margin** is the measured distance from that threshold. Together they tell you how much budget is available to spend on a stat, and how badly a negative margin matters.

Tier definitions:
- **Critical** — character broken or dead if violated. Any negative margin requires immediate compensation before any change is valid.
- **Important** — must be met by end of a milestone; can be temporarily violated during planned transitions. Negative margin flags a gap to address.
- **Preferred** — directional target. Negative margin is noted, not urgent.

**The margin column is a computed snapshot — update at the start of each analysis session from live PoB (`lua_get_stats`).** In design mode, leave Current and Margin as "—" until the character exists in-game.

Margins are **spendable budget** for cascade analysis. A positive margin means you can afford to lose that amount of the stat if a gear swap demands it. A zero margin means any loss requires compensation before the swap is valid.

| Stat | Tier | Threshold | Current | Margin | Notes |
|------|------|-----------|---------|--------|-------|
| Fire resistance | Important | 75% | | | |
| Cold resistance | Important | 75% | | | |
| Lightning resistance | Important | 75% | | | |
| Chaos resistance | build-specific | build-specific | | | |
| Life (unreserved) | build-specific | build-specific | | | |
| Mana (unreserved) | Critical | >0 | | | |
| Strength | Important | gem/gear req | | | |
| Dexterity | Important | gem/gear req | | | |
| Intelligence | Important | gem/gear req | | | |
| Hit chance | build-specific | build-specific | | | |
| Leech source | build-specific | build-specific | | | |

Add or remove rows to match the build. Tiers and thresholds are stable (set during design, updated only when the build concept changes). Current and Margin are recomputed each session.

---

## Section 8: Known Weak Points

Identified vulnerabilities that aren't constraints to be fixed, but risks to be aware of. Informs which content to avoid and which defensive upgrades have the highest marginal value.

Format: state the weak point, its practical consequence, and current mitigation (if any).

---

## Section 9: Design Attempt Log

Record of design paths explored and eliminated for this character or archetype. Prevents repeating failed explorations in future sessions.

Format per entry:
```
[Date] [What was tried]: [Why it was rejected]
```

---

## Filling out the profile

### For a new design (design mode)
- Sections 1–5 and 9 are filled during the build design playbook
- Section 6 (Constraint Status): fill in Tier and Threshold during design; leave Current and Margin as "—" until the character exists in-game
- Section 7 is initially populated from known archetype weaknesses; updated from play experience

### For an existing character (analysis mode)
- Sections 1–5 should be stable once established; update only when the build concept changes
- Section 6 (Constraint Status): Tier and Threshold are stable; recompute Current and Margin from live PoB (`lua_get_stats`) at the start of each analysis session
- Section 7 grows as the player discovers weaknesses in practice

### Staleness
If the patch version in the frontmatter is more than one major patch behind the current game version, treat Sections 1, 3, and 4 as potentially stale. Revalidate against current game data before relying on them for analysis.
