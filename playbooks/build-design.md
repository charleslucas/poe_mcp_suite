# Playbook: Build Design

For designing a Path of Exile character build from a concept or anchor — before the character exists, or when fundamentally rethinking an existing one. This playbook runs a **convergence loop**, not a linear pipeline. You will return to earlier activities as you learn more. That is expected and correct.

Read `playbooks/README.md` first (meta-framework: cursory gate, league pre-flight, trust hierarchy, narration norms). Then follow this playbook.

---

## Implementation note: context windowing

This playbook is intentionally structured so Claude can focus on a narrow window of activities rather than holding the full playbook in context simultaneously. When working through the loop:
- Load the **current activity** in full
- Hold the **immediately adjacent activities** (previous and next) for backtrack triggers and forward conditions
- The remaining activities can be re-read when reached

This keeps context cost manageable on long design sessions. In practice: read the full playbook once at the start to understand the loop shape, then re-focus on the active activity as you work. This is aspirational for now — actual behavior will be refined through use.

---

## Before you begin: session prerequisites

Establish these explicitly. Do not assume.

**Mode** — is this design mode (building something that doesn't exist yet) or analysis mode (improving an existing in-game character)? If analysis mode, use the gear-shopping, tree-analysis, or build-optimization-sim playbooks instead. This playbook is design mode only.

**Design entry point** — how are we starting?
- **Goal-first**: "I want a build that achieves X" (clear outcome, open path)
- **Mechanic-first**: "I want to use mechanic Y" (anchor is a skill, interaction, or system)
- **Item-first**: "I want to build around item Z" (anchor is a specific item)
- **Ascendancy-first**: "I want to play ascendancy A" (anchor is a class/ascendancy)
- **Concept-first**: "I want something like X but different" (anchor is a feeling or playstyle)

**Effort level** — how deep do we go?
- **Adopt**: find an established guide and follow it. Fast, low creativity, proven.
- **Adapt**: use a guide as a starting point, customize to the concept. Medium effort.
- **Original**: design from the anchor up with fresh research. High effort, high creativity.

**Originality pressure** — only relevant at Original effort level:
- **Conventional**: accept consensus choices (best class, best support gems, etc.)
- **Challenge specific**: flag one or two assumptions to actively explore alternatives for
- **Challenge broadly**: treat all conventional wisdom as soft priors, actively seek non-obvious approaches

**Budget** — league-start (limited, only accessible items), established economy (divines available), or unconstrained (theory only).

**League context** — load `reference_data/leagues/{current-league}.md` if it exists. Affects item availability, mechanic presence, economy.

---

## The design loop

The activities below are not sequential steps. They are a loop. You advance when the constraint set tightens. You backtrack when a finding invalidates an earlier decision. You carry forward everything you've learned on each pass — backtracking is not starting over.

### Convergence condition
Done when the constraint set defines something specific enough to execute: class, ascendancy, primary skill, rough passive direction, gear tier targets, sense of playstyle, and enough milestone structure to start playing.

### Abandon condition
After multiple passes, if no viable path exists within the user's constraints (budget, effort, fun), document why and stop. This is a valid and valuable outcome — it eliminates the concept from future consideration with documented rationale.

---

## Activity 1 — Anchor identification and constraint bootstrapping

**Goal**: turn the starting concept into an initial constraint set.

### 1a. Capture the anchor precisely
Write out exactly what the build is trying to do or feel like. Vague anchors produce vague designs. "Lightning spectre minions" is specific enough to bootstrap from. "I want to be tanky" is not.

Also capture **why it's interesting** to the user — this becomes the tiebreaker when tradeoffs arise later. If the appeal is the visual of lightning bolts everywhere, that's different from the appeal of high minion count, which is different from the appeal of a specific spectre's AI.

### 1b. Derive the constraint set
From the anchor, derive two categories:

**Mechanical requirements** (hard constraints — cannot be challenged without breaking the concept):
- Skills or items the mechanic literally requires
- Game systems that must be active for the concept to function
- Interactions that only work one specific way

**Conventional wisdom** (soft priors — label these explicitly):
- Class/ascendancy choices ("Necromancer is best for minions")
- Support gem choices ("Minion Damage is always in the 6L")
- Stat priorities ("minion builds need +max minion count above all else")
- Item choices ("Victario's Influence is the go-to for this")

**Label conventional wisdom clearly.** This is where creative builds are born — by identifying which conventions are actually requirements vs which are just habits.

### 1c. User reviews the constraint set
Present the derived constraints. User confirms mechanical requirements, and decides which conventional wisdom items to:
- Accept as constraints (treat like requirements for this design)
- Challenge (actively research alternatives)
- Ignore (exclude from consideration)

### Backtrack triggers from Activity 1
- None — this is the starting point. But revisit here if research (Activity 2) reveals the anchor is unfeasible or uninteresting.

---

## Activity 2 — Research

**Goal**: find what's known about this design space. Depth controlled by effort level.

### What to look for
- Existing builds / guides around the anchor mechanic or concept
- Community consensus on what works and why
- Known failure modes ("this doesn't work because X")
- Non-obvious approaches (especially if originality pressure is high)
- Budget checkpoints ("this version works at 10 div; this version needs 100 div")

### Effort level controls research depth
- **Adopt**: find one established guide, extract its constraint set, adopt it. Stop.
- **Adapt**: find 2–3 guides, synthesize consensus, identify where they diverge and why.
- **Original**: research breadth first (what archetypes exist around this concept?), then depth on the promising paths. Explicitly search for non-obvious approaches if originality pressure is high. Use `fetch_wiki_page`, Reddit searches, YouTube transcripts.

### If originality pressure is high
Don't just confirm the conventional path — specifically look for:
- Builds that use the anchor mechanic with an unexpected class
- Items that interact with the mechanic in non-obvious ways
- Passive tree paths that enable the mechanic from an unusual direction
- Community discussions of "why doesn't this work?" — sometimes the answer is "it actually does"

### Research tools
- `mcp__poe-data-mcp__fetch_wiki_page` — mechanic descriptions, item stats, skill data
- `mcp__poe-data-mcp__fetch_youtube_transcript` — guide video content
- `mcp__poe-data-mcp__fetch_reddit_post` — community discussion and theory
- `mcp__pob__get_tree_node` — passive node stats (current data)
- `mcp__poe-data-mcp__get_gem_detail` — skill gem data
- `mcp__poe-data-mcp__get_item_detail` — item stats

### After research: update the constraint set
- Confirm or refute conventional wisdom items from Activity 1
- Convert confirmed conventional wisdom to accepted constraints
- Add new derived constraints discovered through research
- Add any budget-blocking items to the constraint set as budget requirements
- Record eliminated paths with rationale (this feeds design attempt knowledge)

### Backtrack triggers from Activity 2
- Research reveals the core mechanic requires a budget-prohibitive item → back to Activity 1 to relax the concept, adjust scope, or change the anchor
- Research shows the concept is fundamentally non-viable (not a convention issue — a hard mechanical limit) → back to Activity 1
- Research reveals a more interesting version of the concept → back to Activity 1 to re-anchor

---

## Activity 3 — Class and ascendancy selection

**Goal**: choose class and ascendancy, with documented rationale.

### Conventional path
Present the conventional choice and why it's conventional. If the user accepted it as a constraint in Activity 1, record it and move on.

### Challenge path
If the conventional choice is flagged for challenge:
1. Enumerate alternative classes that can access the required mechanics
2. For each alternative: what does it gain vs the conventional choice? What does it lose?
3. Evaluate fit against the constraint set — does the alternative satisfy hard constraints?
4. Does any alternative enable something the conventional choice can't?

Be explicit about what "losing" the conventional ascendancy actually costs in numbers, not just "it's weaker." Sometimes the cost is small. Sometimes it's prohibitive.

### Record the decision
State the chosen class/ascendancy AND the rationale. If a path was considered and rejected, record why. This is design attempt knowledge.

### Backtrack triggers from Activity 3
- No available class satisfies the hard constraints → back to Activity 2 (research alternatives) or Activity 1 (relax the concept)
- The challenge exploration reveals the conventional choice is better by a prohibitive margin → accept the convention and record why

---

## Activity 4 — Core mechanics selection

**Goal**: define the primary skill, key supporting mechanics, and the damage/sustain/defense chain.

### Primary skill
Confirm or derive the primary skill from the anchor and class choice. Check:
- Does this skill exist on this class's accessible gem list or via vendor?
- What does it require to function (specific item types, trigger conditions, etc.)?
- What supports it best at the effort/budget level?

### Damage chain
Trace how damage actually flows for this build:
- Source (what generates the hit or damage event)
- Conversion / modification chain (what changes the damage type or scales it)
- Key multipliers (what increases the final number most)

This is the core of the build profile's mechanics summary. Be precise — "scales with physical damage" is different from "scales with elemental damage" which is different from "scales with damage over time."

### Sustain source
What keeps the character alive?
- Leech (what type, what percentage, what recovery rate cap applies)
- Life regeneration (flat vs percentage, conditions)
- Block/evasion/armour (mitigation layer)
- Unique mechanics (Slayer Brutal Fervour, Occultist ES recovery, etc.)

### Key supporting mechanics
Identify 2–4 mechanics that the build depends on beyond the primary skill. These are load-bearing — removing them significantly changes the build's function or viability.

### Backtrack triggers from Activity 4
- Primary skill doesn't synergize with class choice as expected → back to Activity 3 or Activity 2
- Damage chain requires an item or passive cluster that's out of budget or unavailable → back to Activity 1 or 2
- No viable sustain source exists for this combination → back to Activity 3 or 1

---

## Activity 5 — Passive tree direction

**Goal**: identify the passive tree path that supports the mechanics at the chosen effort/budget level.

### What to establish
- Starting zone and primary path direction (don't need every node — need the arc)
- Key notables that the build depends on
- Keystones (if any) — these often define the build's character
- Jewel sockets worth targeting
- Mastery selections

### Check feasibility
- Does the path connect? Can you reach the key notables from the starting class node with a reasonable point count?
- Does the path conflict with anything? (A keystone that disables a required mechanic, a node that requires a weapon type the build can't use, etc.)
- What's the point cost to reach the key nodes? Is it within the level range where it matters?

### Backtrack triggers from Activity 5
- Key notables are unreachable without prohibitive point cost → back to Activity 4 (choose different supporting mechanics) or Activity 3 (different class with better access)
- Required keystone conflicts with the build mechanic → back to Activity 4

---

## Activity 6 — Milestone planning

**Goal**: break the build into level-range milestones with constraint tiers at each stage.

### Standard level ranges
Adjust based on the build's actual progression inflection points:
- Acts 1–3 (approx. levels 1–28): leveling setup, first skills online
- Acts 4–6 (approx. levels 28–50): transition build, primary skill typically available
- Acts 7–10 (approx. levels 50–70): approaching maps, resistances critical
- Early maps (approx. levels 70–85): mapping viability, defensive layers in place
- Mid-late maps (approx. levels 85–95): optimization, upgrade targets
- Endgame (level 95–100): final form

### Per-milestone define
- **Active skills** and key supports
- **Passive direction** (which cluster or keystone is the priority for this range)
- **Gear tier target** (what quality of gear is needed/expected)
- **Constraint tiers at this stage**:
  - Critical: must be satisfied or the character is broken/dead
  - Important: should be met by end of this milestone, can be temporarily violated
  - Preferred: directional target
- **Transition violations**: explicitly mark any Important constraint that is intentionally relaxed during this milestone and why (e.g., "cold resistance drops to 60% at level 38 while transitioning gem setup — acceptable for 5 levels")

### Backtrack triggers from Activity 6
- Build doesn't come online until an unacceptably late milestone → back to Activity 4 (different primary skill with earlier availability) or Activity 1 (reconsider the concept)
- A key item required for early milestones is budget-prohibitive → back to Activity 4 or 1

---

## Activity 7 — Outputs

**Goal**: produce the two artifacts that this playbook creates.

### Output 1: Build Profile document

The structured, machine-readable summary that all analysis playbooks will load as a prerequisite. See `playbooks/build-profile-format.md` for the exact format and required fields.

The build profile is NOT a narrative — it is structured data. Keep it compact. The journal and build plan carry the narrative.

### Output 2: Build Plan document

The narrative milestone breakdown. Lives at `character_data/{Account}/{League}/{Character}/build.md` or, for a design that hasn't started play yet, at `character_data/guides/{archetype}/build-plan.md`.

**Trunk-and-branch semantics** (library README → "League lifecycle"): the archetype-dir
copy is the league-spanning **trunk** — league-stamped, revised each league (see
[`league-transition.md`](league-transition.md) Step 8). Creating a character **forks a
copy** into the character dir as its `build.md` baseline; never move the trunk. Multiple
characters (even in one league) can branch from the same trunk state, and character-side
learnings that generalize flow back to the archetype's README/synthesis.

**A matured trunk can be published back to the community** (pobb.in via
`lua_share_pobb`, analysis baked into the Notes tab, sources credited) — workflow in the
library README → "Publishing back to the community". Contribute upstream, not just to
suite users.

Contents:
- One-paragraph concept summary (why this build, what makes it interesting)
- Per-milestone breakdown (passive direction, skills, gear tier, key purchases)
- Known weak points and how they're addressed (or accepted)
- Open questions — things that need in-game verification or future research
- Design attempt log — paths explored and rejected, with rationale

### Knowledge capture
Before closing the session, identify what was learned that generalizes beyond this character:
- Any design attempt knowledge (paths explored and eliminated) worth persisting to `character_data/design_attempts/`
- Any archetype findings worth adding to `character_data/guides/{archetype}/`
- Any game mechanic corrections or discoveries worth adding to `reference_data/`

---

## Pitfalls

### Convention vs requirement confusion
The most common error: treating conventional wisdom as a hard constraint without verifying it. "You need Necromancer for minions" is a prior, not a law. Always label which is which.

### Stopping at the first viable path
Especially at Original effort level: the first viable design you find may not be the most interesting one. Keep the originality pressure active until you've deliberately checked at least one non-obvious alternative.

### Ignoring the fun criterion
A build can be theoretically viable and mechanically sound but not enjoyable to play. The user's stated reason for the concept's appeal (from Activity 1b) is the tiebreaker for this. If the design drifts away from what made it interesting, backtrack.

### Treating the milestone plan as fixed
The milestone plan is a navigation aid, not a contract. Real play will deviate. The plan's value is in establishing the constraint tiers per stage — those survive deviation better than specific item recommendations.

### Budget creep
As the design gets more detailed, item recommendations tend to drift toward optimal. Periodically check that the current design is still achievable at the stated budget. If not, either adjust the design or explicitly upgrade the budget requirement.

### Skipping knowledge capture
The design loop generates knowledge at every pass. If you don't capture it at the end of the session, it's lost. The design attempt log in the build plan is the minimum; persist generalizable findings to the appropriate shared location.
