# Community Survey Playbook

Use this playbook when the task is to gather **community-discovered pitfalls, improvements, or consensus**
for a build archetype — typically run as a post-deep-analysis pass on a build-plan.md, or on request.

This is a **cursory-scope tool** by default (two queries, minimal synthesis). It becomes detailed only if
the results reveal something that needs cross-checking against PoB or the wiki.

---

## When to use this

- After an initial guide analysis: "did the community find anything the guide missed?"
- User asks: "what does Reddit say about X", "common mistakes", "community pitfalls", "any improvements
  people found", "what's wrong with this build in practice"
- Pre-league-start: sanity-check a build plan against real player experience before committing

**Not for:**
- Verifying mechanical interactions (use PoB or `fetch_wiki_page`)
- Resistance/attribute math or breakpoint calculations (use PoB)
- Current prices (use `ninja_lookup`)
- Anything requiring a single authoritative answer — community consensus is noisy

---

## Standard queries

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
- Distinguishing league-specific changes from permanent ones — note the league context

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
