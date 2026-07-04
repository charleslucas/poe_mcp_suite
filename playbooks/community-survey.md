# Community Survey Playbook

Use this playbook when the task is to gather **community-discovered pitfalls, improvements, or consensus**
for a build archetype — typically run as a post-deep-analysis pass on a build-plan.md, or on request.

This is a **cursory-scope tool** by default (two queries, minimal synthesis). It becomes detailed only if
the results reveal something that needs cross-checking against PoB or the wiki.

---

## When to use this

**Use case 1 — Archetype pitfall pass (any time)**
After an initial guide analysis: "did the community find anything the guide missed?" Run the two
standard queries in parallel with the guide read. Highest yield on stable archetypes with an active
community. See standard queries below.

**Use case 2 — Pre-league-start sanity check**
Before committing to a league-start build, check whether the community has surfaced problems with the
archetype in the most recent league. Often catches "this used to work but was nerfed" situations that
training knowledge misses.

**Use case 3 — Early-league community sweep (highest value window)**
In the first 1–4 weeks of a new league, Google AI Mode is the best available source for:
- League mechanic interactions with specific builds ("does [new mechanic] work with [archetype]?")
- Player-discovered bugs, unintended synergies, or gotchas with new content
- Early-league economy observations ("what's actually valuable this league?")
- Which league-start builds are performing vs. underperforming relative to pre-launch expectations

This window has the **lowest cross-version blending risk** of any use case: the current league is
recent enough that fresh posts dominate search results, and there's little old conflicting content yet.

Training knowledge and Google AI Mode cover different gaps here — they're complementary, not redundant:
- **Training knowledge is good for:** the foundation of returning mechanics (how Tattoos work, what
  Sanctum rewards do, Heist blueprint logic). If a mechanic ran before, training knowledge covers its
  rules well.
- **Google AI Mode fills the delta:** whether a returning mechanic was modified since its last
  appearance, current pricing and availability, newly discovered interactions with this patch's skills
  and items, and which community strategies have emerged as best-in-slot this time around.

The practical split: use training knowledge to explain *how a mechanic works*, reach for Google AI
Mode to find out *what changed, what's different, and what the community discovered this run*. For
a truly new mechanic with no prior appearance, both gaps open up simultaneously — that's when the
early-league sweep is most valuable.

Query cadence for early-league sweeps: run once at launch + patch notes, again after ~1 week (first
wave of player experience), again at ~3–4 weeks (economy stabilized, meta solidifying). After that,
community knowledge is well enough indexed that targeted queries are better than sweeps.

**Use case 4 — On-demand community lookup**
User asks: "what does Reddit say about X", "common mistakes", "community pitfalls", "any improvements
people found", "what's wrong with this build in practice."

**Not for:**
- Verifying mechanical interactions (use PoB or `fetch_wiki_page`)
- Resistance/attribute math or breakpoint calculations (use PoB)
- Current prices (use `ninja_lookup`)
- Anything requiring a single authoritative answer — community consensus is noisy
- **Character-specific gear or tree recommendations** — see "Query framing" section below

---

## Standard queries

### Archetype pitfall pass (use cases 1, 2, 4)

Run both in parallel via `mcp__google-ai-mode__search_ai`:

```
Query A (pitfalls):
"[Archetype Name] Path of Exile common mistakes weaknesses complaints community reddit"

Query B (improvements):
"[Archetype Name] Path of Exile community improvements modifications alternatives reddit [current year]"
```

Add the current year to Query B to bias toward recent league experience over old posts.

**Example (Holy Relic Necromancer):**
- A: `"Holy Relic Necromancer Path of Exile common mistakes weaknesses complaints community reddit"`
- B: `"Holy Relic Necromancer Path of Exile community improvements modifications alternatives reddit 2026"`

### Early-league community sweep (use case 3)

Run at league launch and again at ~1 week and ~3–4 weeks. Queries are broader — the goal is
discovery, not targeted pitfall-finding.

```
Query A (league mechanic + build):
"[Archetype Name] [League Name] league Path of Exile reddit [year]"

Query B (league mechanic standalone):
"[League Name] league Path of Exile best builds mechanics community reddit [year]"

Query C (league mechanic + specific interaction, if relevant):
"[League Name] [specific mechanic or currency] interaction [archetype] reddit"
```

**Example (Holy Relic Necromancer at 3.29 launch):**
- A: `"Holy Relic Necromancer 3.29 league Path of Exile reddit 2026"`
- B: `"3.29 Path of Exile best league start builds mechanics community reddit 2026"`
- C: (only if a specific mechanic is known) `"[new mechanic name] minion build interaction reddit"`

These queries have a natural expiry — they're most useful in the first month. After that, switch back
to the standard archetype pitfall queries which will have absorbed the league-specific discoveries.

---

## Query framing — the most important rule

**Google AI Mode has two distinct operating modes depending on how the query is phrased:**

| Query style | What Google does | Result quality |
|---|---|---|
| Open-ended search ("common pitfalls for X", "what does Reddit say about Y") | Fetches and synthesizes community forum content; cites Reddit/YouTube sources | **High** — surfaces real player discoveries |
| Direct advice ("here's my gear, what should I upgrade?") | Answers from its own training knowledge; no sources cited | **Low** — same staleness issues as Claude's training; makes build-specific errors |

**The tell is whether sources are cited.** If the response returns with Reddit URLs, it searched. If there are no sources, it answered from training — treat it like any other training-knowledge response (verify everything, check dates).

**Practical implication:** Google AI Mode is a *community document retrieval tool*, not a build advisor. Providing character-specific gear data and asking for suggestions produces a training-knowledge response with generic, often incorrect advice (tested 2026-07-03 on MirageSixFingeredMan: incorrectly dismissed the three-ring slot as an error, suggested wrong uniques, recommended a totem anoint on a non-totem build).

**For character-specific community input, reframe as a search query:**

Instead of: *"Here's my gear — what should I upgrade?"*
Use: *"[Archetype] best [slot] upgrade community reddit"* or *"[Archetype] [item] worth it reddit 2026"*

These search for community discussions about that slot/item, which is what Google AI Mode does well.

**Where to use community survey in the workflow:**

- ✅ **During archetype/guide analysis** (before you have a character): run in parallel with the guide read. Finds edge cases and player-discovered fixes the guide author never documented. High yield.
- ✅ **Pre-league-start**: sanity-check a build plan against real player experience.
- ⚠️ **During character gear optimization**: lower yield. PoB simulation is the right primary tool; community survey can add slot-specific search queries ("best body armour for [archetype]") as supplementary input, but not "analyze my specific gear."
- ❌ **As a replacement for PoB math**: it cannot simulate your actual character.

---

## Interpreting results

Google AI Mode synthesizes Reddit/YouTube community content. It is good at:
- Surfacing the **most-repeated complaints** (high signal — if it shows up, many people hit it)
- Naming **concrete item/gem substitutions** the community discovered post-guide
- Identifying **new spectres, Forbidden Jewel combos, or league-mechanic interactions** that emerged
  after the original guide was written

It is **unreliable** for:
- Exact numbers (CDR values, DPS figures, breakpoint math) — always verify in PoB
- Citation accuracy — it attributes claims to Reddit threads; the threads are real but the specific
  claim may be a synthesis artifact. Treat numbers as leads to verify, not facts
- **Cross-version blending** — Reddit posts span many patches; Google AI synthesizes them without
  version-tagging the advice. A recommendation correct in 3.21 may be wrong in 3.28 if the build
  evolved. The Trinity vs MPD conflict for Diamond Shrine Cyclone Slayer is the canonical example:
  Trinity is correct advice for the standard General's Cry variant across many patches, but Google
  surfaced it for a variant where PoB showed 0 DPS contribution. The synthesis didn't distinguish.
- **Variant blending** — if an archetype has multiple popular versions (e.g. General's Cry vs Cyclone
  of Tumult Slayer, or auras-on vs map-mod-immune Holy Relic), advice for one variant will bleed into
  results for another without flagging it. High risk when the build being analyzed is a niche or
  recent variant of a well-documented archetype.

**When cross-version / variant blending risk is highest:**
- The archetype has changed significantly across recent patches (new transfig gems, ascendancy reworks)
- Core mechanics were added recently (e.g. Void Shockwave as a transfig, Imbued Supports)
- The specific variant is niche relative to the broader archetype's community presence

**When it's lowest:** archetype is mechanically stable across the patches those Reddit posts cover —
the advice stays valid regardless of which version the poster was playing.

**Evaluation filter — before writing anything to a build plan:**
1. Is this mechanically plausible? (Does it make sense given how the skill/stat works?)
2. Is it concrete enough to act on? (A named item, gem, or stat — not vague advice)
3. Is it new relative to the existing plan? (Don't duplicate what's already documented)
4. For numbers: verify in PoB before adding as a hard target

---

## Output format

For each finding that passes the filter, add it to the relevant section of `build-plan.md`:

- **New pitfall** → add to (or create) a "community-identified pitfalls" quick-fail checklist section
- **Improvement / optimization** → add to the appropriate progression phase
- **Endgame optimization** → Phase 3 or a dedicated "high-investment" section
- **Build variant / alternative** → note it without expanding into a full sub-plan unless requested

End the session entry in `§ Design attempt log` with the date and a one-line summary of what was added.

---

## Limitations to note inline

When adding community-sourced content to a plan, mark the finding's origin if it's not yet PoB-verified:

> *(community-sourced; verify in PoB before committing)*

This distinguishes "the guide says" (authoritative) from "Reddit says" (probable but worth a check).
Remove the tag once verified.

---

## Capability map (validated 2026-07-03)

Three live experiments established where Google AI Mode adds value and where it doesn't. Use this as
the decision table for whether to reach for it.

| Task | Query style | Sources? | Yield | Use it? |
|---|---|---|---|---|
| Archetype pitfalls + improvements | Open-ended search | Reddit URLs | High — finds concrete edge cases the guide missed | ✅ Yes, in parallel with guide read |
| **Early-league mechanic sweep** | League-name search | Reddit URLs | **Highest** — only live source for current-league discoveries; training knowledge has nothing here | ✅ Yes — run at launch, 1 wk, 3–4 wks |
| Character gear recommendations | Direct advice + gear list | None (training) | Low — generic/wrong (dismissed 3-ring slot, suggested totem anoint on non-totem build) | ❌ No — use PoB sim |
| Passive tree (direct advice) | Direct advice + node list | Wrong archetype articles (3.21) | Low — generic defensive nodes, no connection to actual tree state | ❌ No — use `get_passive_upgrades` |
| Passive tree (archetype shape) | Open-ended search | Reddit threads | Medium — tells you what the archetype generally targets; can't know what's already allocated | ⚠️ Pre-tree only |
| Community consensus on a specific item/slot | "[Archetype] [item] reddit" | Reddit URLs | Medium — finds community verdicts; verify numbers in PoB | ✅ Useful supplementary |

**The core boundary:** Google AI Mode retrieves what the *community has written* about an archetype. It
cannot reason about your specific character's current state — tree allocations, exact stat margins,
or niche mechanics the community hasn't written about (e.g. The Unseen Hand three-ring slot).

**When community and PoB conflict, PoB wins.** Example: community recommends Trinity Support for Cyclone
Slayer (because random elemental conversion looks like it should trigger resonance), but PoB simulation
showed Trinity = 0 DPS and Melee Physical Damage = +50.4% for the Diamond Shrine variant specifically.
Community consensus is written for the common version of a build; niche variants diverge. The simulation
runs the actual numbers on the actual character — always the tiebreaker.

**The parallel-query question:** Worth running in parallel during guide/archetype analysis — two queries,
~30 seconds, consistently surfaces 3-5 findings the guide doesn't cover. Not worth it during character
optimization sessions where PoB has real data and community knowledge is too coarse to help.

**Connection to league reference cache:** Early-league sweep findings that are league-mechanic-specific
(not archetype-specific) belong in `reference_data/leagues/{league}.md`, not in a build-plan. Write
archetype-specific findings to the archetype's build-plan or README; write league-wide mechanic
discoveries (drop rates, farming strategies, economy observations) to the league cache file. See
`playbooks/README.md` §2b for the league reference protocol.
