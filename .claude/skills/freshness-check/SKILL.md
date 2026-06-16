---
name: freshness-check
description: Model-aware check of whether your PoE training data is stale on a specific mechanic, item, or system before you assert how it works. Routes to reference_data/freshness_index.md, which keys post-training mechanics by patch and lists each Claude model's training cutoff.
when_to_use: Use before stating how a recent or current-league PoE mechanic/item/system works; when the user asks "is X still in the game", "does Y still work", "what changed in league Z", "is this new this league", or asks about a mechanic you don't clearly recognize; and within detailed analyses (dps-analysis, gear-shopping, tree-analysis, build-optimization-sim, crafting-lookup, atlas-planning, build-design) at the stage where patch-specific mechanic/item knowledge is the input. Skip for timeless/conceptual questions (how a mechanic fundamentally works, the math) — those are safe from memory.
---

Your PoE training knowledge has a **model-specific cutoff** and the game changes every league, so the
biggest risk is an *unknown unknown*: confidently asserting a mechanic that changed or didn't exist yet.

1. Read [`reference_data/freshness_index.md`](../../../reference_data/freshness_index.md) and follow its
   "How to use it" procedure:
   - Identify the running model (`mcp__pob__get_context_usage` reports the model ID).
   - Look up that model's training cutoff in the index's model table.
   - Treat anything in the index **newer than the running model's cutoff as must-verify** — use the entry's
     "Where / verify via" pointer (a cached file, a memory, or a fresh `fetch_wiki_page` / live PoB call).
2. If the mechanic/item isn't in the index but is plausibly recent (current or last few leagues), **verify
   it anyway** and add a row to the index so the next session is covered.
3. This is most load-bearing when asserting how a mechanic works or evaluating a unique/node/item's
   *current* stats — not every step of a task. Per `CLAUDE.md`, defer to live tool data over memory when
   they conflict.

Do not duplicate the index content here — the index is the single source of truth and is maintained per league.
