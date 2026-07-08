---
name: freshness-check
description: Model-aware staleness check before asserting how a PoE mechanic/item/system works, plus a scope filter so league/event mechanics don't bleed into the wrong character. Routes to freshness_index.md + mechanics_index.md.
when_to_use: Use before stating how a recent or current-league mechanic/item works; on "is X still in the game", "does Y still work", "what changed in league Z", or any mechanic you don't clearly recognize; and at the patch-specific stage of any detailed analysis. Skip timeless/conceptual questions (fundamentals, math).
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
3. **Scope filter (compartmentalization).** Also consult the mechanic-keyed companion
   [`reference_data/mechanics_index.md`](../../../reference_data/mechanics_index.md) for each mechanic's
   current **scope** (`core` / `challenge-league` / `event-only` / `removed` / `disabled-this-league` /
   `nerfed`). When the task concerns a **specific character**, first establish its context (league/realm, and
   whether it's an event character — see `playbooks/README.md` §2c), then **only apply mechanics whose scope
   includes that context**. A Mirage-only or event-only mechanic must not be recommended for a Standard /
   next-league / non-event character; a removed or disabled-this-league one isn't present at all. This stops
   league/event data bleeding into the wrong build.
4. This is most load-bearing when asserting how a mechanic works or evaluating a unique/node/item's
   *current* stats — not every step of a task. Per `CLAUDE.md`, defer to live tool data over memory when
   they conflict.

Do not duplicate the index content here — the index is the single source of truth and is maintained per league.
