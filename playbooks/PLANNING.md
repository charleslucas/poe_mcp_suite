# Playbook Architecture Planning

Captures the design decisions and concepts agreed on in the 2026-06-09 session, before implementation begins. Read this before making structural changes to playbooks, character data formats, or knowledge storage.

---

## 1. The Design Loop

Every meaningful decision in PoE — building a character, gearing a character, planning atlas strategy — follows the same iterative pattern. This is not a linear pipeline. It is a convergence loop.

**Activities** (not sequential steps — you return to them):
1. Anchor identification — what is the core concept or goal?
2. Constraint bootstrapping — derive hard requirements and conventional wisdom from the anchor
3. Research — find what's known about this space
4. Decision points — class, mechanics, milestones, gear targets
5. Validation — does the current design survive constraint checks?

**Backtrack triggers** — findings that send you to an earlier activity:
- Concept requires budget-prohibitive item → back to anchor
- Class has no viable passive path for the mechanic → back to research or anchor
- Build doesn't come online until unacceptably late → back to mechanics or anchor
- Concept is theoretically valid but not fun → back to anchor
- Cascade analysis shows a gear change breaks too many constraints → don't make the change

**Carry-forward state** — backtracking is not starting over. Each pass accumulates:
- Eliminated paths (with documented rationale — "we tried X, it failed because Y")
- Derived hard constraints (things that started as conventional wisdom but were tested and confirmed as requirements)
- Research already done (don't re-fetch what you've already loaded)

**Convergence condition** — done when the constraint set defines something specific enough to execute: class, primary skill, rough passive direction, gear tier targets, sense of playstyle.

**Abandon condition** — explicit outcome when multiple passes can't find a viable path within the user's constraints. Document the rationale. This is valuable knowledge, not failure.

---

## 2. Design Mode vs Analysis Mode

Two fundamentally different session types. Always establish which mode applies before loading data or running tools.

### Design Mode
- Goal: produce a build that doesn't exist yet
- Constraint source: derived from the concept + research + user preferences
- Outputs: build profile document, build plan (milestones), open questions
- Tools: research (wiki, guides, YouTube), PoB simulation for theoretical builds
- Sub-modes:
  - **Goal-first**: "I want a build that does X" → derive class/mechanics
  - **Mechanic-first**: "I want to use mechanic Y" → find what that enables
  - **Item-first**: "I want to build around item Z" → derive everything from the item
  - **Ascendancy-first**: "I want to play X ascendancy" → find what it does best

### Analysis Mode
- Goal: improve or understand a character that already exists in-game
- Constraint source: current PoB state + constraint margin table
- Outputs: specific recommendations, updated build profile, journal entries
- Tools: live PoB (TCP), gear audit, trade search, PoB simulation for proposed changes
- Sub-modes: gear upgrade / tree reallocation / gem optimization / budget allocation / specific item evaluation

**Handoff point**: the build profile document. Design mode produces it. Analysis mode consumes it. It must be kept current as the character evolves.

---

## 3. Constraint System

### Constraint tiers
- **Critical** — character is broken or dead if violated. No exceptions at any level. Examples: leech source must exist on a leech build; hit chance cannot be low when non-crits deal zero damage; flask type must be compatible with belt.
- **Important** — should be met by end of milestone, can be temporarily violated during a transition. Resistances are the standard example. Transition violations must be explicit and planned.
- **Preferred** — directional targets. Being below them is not an emergency. Examples: chaos resistance floor, life overcap margin, mana headroom.

### Constraint margins
For any analysis session, compute the margin table before touching anything:

| Stat | Current | Minimum | Margin | Notes |
|------|---------|---------|--------|-------|
| Fire res | 78% | 75% | +3% | near floor |
| Cold res | 77% | 75% | +2% | near floor |
| Dexterity | 142 | 120 | +22 | some slack |
| etc. | | | | |

Margins are **spendable budget**. When a proposed change costs margin, check if the remaining margin stays non-negative. When margin goes negative, compensation is required before the change is valid.

### Cascade analysis
Before committing any change:
1. What does removing/replacing this item cost across all constrained stats?
2. Which margins go negative?
3. For each negative margin, what is the cheapest/best compensation path (gear, tree node, gem)?
4. Sum total cost: anchor change + all compensations
5. Is the net delta worth the total cost?

"Don't make this change" is an explicit valid output. Knowing what not to do is as valuable as knowing what to do.

### Constraint evolution
Constraints change with level and game state:
- Design mode: constraints are declared per milestone (Critical / Important / Preferred at each stage)
- Analysis mode: constraints are the current snapshot, margins computed from live PoB state
- Same vocabulary, different application

---

## 4. Session Prerequisites

Establish these at the start of every session. Skip only if already clear from context.

### Always required
- **Mode**: design or analysis?
- **Session goal**: what are we trying to accomplish?
  - Design: new build concept / adapt existing build / evaluate originality
  - Analysis: upgrade specific slot / fix constraint violation / allocate budget / evaluate found item / tree reallocation / gem optimization
- **Optimization objective**:
  - Cheapest valid path (satisfy constraints, minimize cost)
  - Sweet spot (willing to spend more for meaningful threshold gains)
  - Threshold (trying to hit specific target: "4000 life", "Uber-ready")
  - Budget allocation ("5 div to spend, where does it go furthest?")

### Design mode additional
- **Effort level**: guide adoption / guide adaptation / original research
- **Originality pressure**: conventional / challenge specific assumptions / challenge all assumptions
- **Budget ceiling**

### Analysis mode additional
- Load build profile (see section 5)
- Compute constraint margin table from live PoB state
- **Budget** for this session

---

## 5. Knowledge Taxonomy

Three dimensions classify every piece of knowledge in the system.

### Type
- **Game mechanics** — how a skill, modifier, or system works. Timeless unless GGG changes it.
- **Archetype consensus** — what the community has learned about a build archetype. Changes with patches and metas.
- **Design attempt** — the result of a design loop pass. "We explored X, it doesn't work because Y." See section 6.
- **Character-specific** — data about a specific character in a specific account. Not generalizable.
- **Session output** — ephemeral findings from a single session. Promoted to a higher type or discarded.

### Freshness
- **Timeless** — safe to trust indefinitely (core game mechanics, math)
- **Patch-dependent** — valid for a specific PoE version, must be revalidated on major patches
- **League-specific** — valid only for a specific league (economy, mechanic availability)
- **Ephemeral** — conversation context, current session only

### Scope
- **Game-wide** — applies to all characters and builds
- **Archetype** — applies to a class of builds (e.g., "all Slayer leech builds")
- **Character** — specific to one character
- **Session** — relevant only to the current task

### Where each type lives currently
| Type | Location | Committed? |
|------|----------|-----------|
| Game mechanics | `reference_data/` | Yes |
| Archetype consensus | `character_data/guides/{archetype}/` | Yes |
| Design attempt | **No formal home yet** | — |
| Character-specific | `character_data/{Account}/{League}/{Character}/` | No (junction) |
| Session output | Conversation context + journal | Partially |

The gap is **design attempt knowledge**. Needs a home. See section 6.

### Loading strategy
- Always-loaded: MEMORY.md index, playbooks/README.md, active character build profile
- On-demand: specific playbooks, reference_data files, guide research
- Relevance determination: index entry must be expressive enough to decide whether to load without reading the full file
- Cost scales with scope: character-specific is cheap; game-wide is expensive; load narrower first

---

## 6. Design Attempt Knowledge (Gap to Fill)

When a design loop pass explores a concept and discovers it doesn't work (or doesn't work within constraints), that finding has value beyond the current session. It should be captured so future sessions don't repeat the same exploration.

**Properties**:
- Not tied to any specific character (the character may not exist yet)
- More specific than archetype consensus (not "here's how spectres work" but "here's why spectres on Chieftain fail for reason X")
- Includes: what was tried, what constraints were violated, what the blocking factor was, whether it's a hard limit or a budget/effort limit
- Patch-stamped (a finding from 3.28 may not hold in 3.30)

**Proposed home**: `character_data/design_attempts/{concept-slug}/` with:
- `README.md` — concept summary, verdict (abandoned / viable / viable-with-budget-X), blocking factors
- `research.md` — what was found during research passes
- `iterations/` — dated snapshots of each loop pass

**Shareable**: yes, with anonymization. Design attempt knowledge is exactly the kind of thing other users can benefit from.

---

## 7. Build Profile Document

The handoff artifact between design mode and analysis mode. Every analysis playbook should load this as a prerequisite.

**Required fields** (to be finalized when we design the format):
- Character identity: class, ascendancy, primary skill(s)
- Core mechanic summary: how the build actually works (damage chain, sustain source, defensive layers)
- Mandatory anchor items: items the build cannot function without
- Stat priority order: what to maximize, in order
- Mod value overrides: mods worth more than generic (crit multi for a crit build), mods worth less (added flat damage on a conversion build), mods that are irrelevant or detrimental
- Hard constraints: build-specific rules that override general rules (flask type, hit chance floor, leech source requirement)
- Current constraint margins: snapshot updated each session (computed, not manually maintained)
- Patch/league stamp: when this profile was last validated

**Design goals**:
- Structured enough to be machine-readable by Claude in any session
- Lightweight enough that reading it is cheap (not a 5000-word essay)
- Ages well: stale sections are clearly marked, not silently wrong
- Doubles as contribution format for community sharing (see section 8)

**Build profile as scoring function and constraint reduction:**
Sections 3 (Stat Priority) + 4 (Mod Value Overrides) serve double duty beyond being a structured data store:
1. *Scoring function* — they define "better" in build-specific terms. Generic tier analysis is wrong for any build with non-standard scaling (conversion, leech mechanics, forced-crit engines, etc.). The profile makes the correct scoring function available in every session without reconstruction.
2. *Constraint reduction mechanism* — they collapse large search spaces to tractable ones. A mod pool of 30-40 candidates narrows to 6-10 relevant ones once filtered through the build's actual priorities. A passive tree candidate list of 50 nodes collapses to the handful that move the build's actual levers.

This second property is especially important for systematic optimization: single-slot mod selection becomes a small enumerable problem (15-25 craftable candidates → sim each in PoB → rank by Section 3); full item design becomes tractable because the profile reduces the effective search space before any brute-force enumeration begins. Without the profile, exhaustive evaluation is computationally infeasible or produces wrong rankings. With it, it's a bounded search over a meaningful subset.

---

## 8. Community Knowledge Sharing

The system is designed so that accumulated knowledge can be contributed back via pull request.

**Shareable** (goes in the repo):
- `reference_data/` — game mechanics, mod pools, shrine data, tree exports
- `character_data/guides/{archetype}/` — build guide research and synthesis
- `character_data/design_attempts/` — design loop findings (once the home exists)
- Playbooks (`playbooks/`) — improved procedures
- Build profile templates

**Not shareable** (stays in the external junction, never committed):
- `character_data/{Account}/{League}/{Character}/` — specific character data, journal, snapshots
- Any file containing account names, session IDs, or personal economy data

**Contribution metadata requirements** (every shared file must have):
- League and patch version when created/last validated
- Tested-in-game vs theoretical flag
- Scope tag (game-wide / archetype / mechanic-specific)
- Author optional (can be anonymous)

**Conflict resolution**: patch-stamped recency wins. Conflicting findings from the same patch get a "disputed" flag and both are preserved until resolved.

**Contribution guide**: needs to be written. Should live at `CONTRIBUTING.md` in the repo root.

---

## 9. Playbooks to Create / Revise

### New: `playbooks/build-design.md`
The design loop formalized. Covers all design modes (goal-first, mechanic-first, item-first, ascendancy-first). Includes: constraint bootstrapping, convention vs challenge labeling, research depth controlled by effort level, backtrack triggers per activity, convergence and abandon conditions. Produces: build profile + build plan.

### Revised: `playbooks/gear-shopping.md`
Add upfront gear audit phase (run `analyze_item_mods` on all slots, classify mods as load-bearing / resistance budget / attribute budget / weak / wasted with build-aware value weighting). Add constraint margin table computation. Add cascade analysis step between "identify anchor upgrade" and "search trade." Prerequisite: build profile loaded.

### All analysis playbooks
Add build profile as a standard prerequisite. The build profile's mod value overrides and build-specific constraints should inform every recommendation made by any analysis playbook. Formalize the shared pattern as Section 2d in `playbooks/README.md` so each playbook references it rather than duplicating the logic.

### New: `playbooks/crafting-optimization.md`
Systematic mod selection using the build profile as scoring function and constraint reduction. Two sub-cases: (1) single-slot — enumerate all craftable mods for the target slot via `list_craftable_mods_for_base`, sim each in PoB, rank by build profile Sections 3+4; (2) full item design — profile filters the mod pool to the relevant subset (typically 6-10 from 30-40), then enumerate combinations over that reduced space. Prerequisite: build profile loaded and constraint margins computed (README.md §2d).

### `playbooks/README.md`
Add: design vs analysis mode classification as a third gate alongside cursory vs detailed and freshness. Add: knowledge taxonomy overview with pointers to where each type lives.

---

## 10. Implementation Order

Status as of 2026-07-07:

1. ✅ Design the build profile document format — done: [`build-profile-format.md`](build-profile-format.md), consumed by README §2d
2. ✅ Write `playbooks/build-design.md` — done; wrapper skill `.claude/skills/build-design/` added 2026-07-07
3. ✅ Revise `playbooks/gear-shopping.md` with audit + cascade analysis phases — done
4. ✅ Update `playbooks/README.md` with mode classification and knowledge taxonomy overview — done 2026-07-07 (§1 mode gate + taxonomy pointer; §2d was already in place)
5. ⬜ Create `character_data/design_attempts/` directory structure — **not done**; design-attempt knowledge (§6) still has no home
6. ✅ Revise other analysis playbooks to load build profile as prerequisite — done via README §2d (gear-shopping, tree-analysis, dps-analysis, build-optimization-sim required; build-comparison conditional)
7. ⬜ Write `CONTRIBUTING.md` — **not done**; §8's contribution metadata requirements still live only in this file
