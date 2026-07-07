# Playbook: Guide Analysis

For digesting an external build guide (YouTube, written site, or bare pobb.in link) into the global guide library at `character_data/guides/{archetype}/`. The library's *data format* is documented in `character_data/guides/README.md`; this playbook is the *procedure* for populating it.

Read `playbooks/README.md` first (meta-framework: cursory gate, pre-flight, sub-agents, narration norms). Note the **model routing** rule in `CLAUDE.md`: guide synthesis is the canonical Opus-class task — training meta-knowledge is the primary input. Note it inline ("Running guide synthesis with best meta knowledge — say 'use Sonnet' to downgrade") and proceed.

---

## Step 0 — Frame the work

*"Using the Guide Analysis playbook — I'll check the archetype library first, then digest the guide in a sub-agent and add a library entry."*

Announce the sub-agent dispatch when it happens ("Digesting the transcript in a sub-agent so the raw text never enters main context").

---

## Step 1 — Triage

Auto-derive before asking: check `character_data/guides/` for an existing archetype directory matching the guide's build, and check whether the user's message already names a character or purpose.

1. **Existing archetype or new?** — If a matching `{archetype}/` dir exists, this is an *addition* (read its README first, load its entry list). If not, it's a *bootstrap* (create the directory from the root README's conventions).
2. **Source type?** — YouTube video / written guide (poe-vault, maxroll, mobalytics) / bare pobb.in link. Gates which fetch tools Step 2 uses.
3. **Purpose?** — (a) library entry only; (b) evaluating for a specific character (adds character files to Step 2 and a comparison stage to Step 3); (c) league-start planning (adds tier/budget emphasis).
4. **Depth?** — *Quick entry* (metadata, PoB link, key uniques — no transcript) vs *full digest* (transcript/article + PoB extraction + synthesis update). Default to full for a new archetype, quick for a third-or-later guide in a well-covered archetype.

---

## Step 2 — Data loads

| Condition | Load | Via |
|---|---|---|
| Always | Root conventions | `character_data/guides/README.md` (first time per session) |
| Always | Archetype README (if exists) | Read — consensus notes + current best guide by tier |
| Always | Freshness pre-flight | Guide's league vs current league; `reference_data/mechanics_index.md` scope check for the build's core mechanics (README §2e) |
| YouTube source | Video description **first** (cheap — usually contains the pobb.in link) | `mcp__poemcp__fetch_youtube_description` |
| YouTube + full digest | Transcript — **sub-agent only**, never main context | Explore sub-agent calling `mcp__poemcp__fetch_youtube_transcript` |
| Written guide | Article — sub-agent | Explore sub-agent with WebFetch |
| PoB link present | Build extraction | `mcp__poemcp__parse_pob`, or sub-agent digesting the XML |
| Purpose = (b) evaluating for character | `meta.json` + `build-profile.md` | Character dir (README §2c/§2d) |

---

## Step 3 — Analysis pattern

1. **Archetype dir**: create if new (README.md skeleton: mechanic summary, build identity, key uniques by accessibility, best guide by tier, common pitfalls).
2. **Sub-agent digest**: one Explore agent per guide (parallel dispatch if multiple). The agent's prompt asks for a structured extraction matching the entry schema — `author, title, league, tier, pobb_in, youtube, guide_url, class, ascendancy, main_skill, trigger_skill, key_uniques[], bandit, active_spec_nodes, stored_stats{}, notes` — plus the 3-5 most load-bearing claims with timestamps/sections for verification.
3. **Cross-version check**: if the guide's league ≠ current league, run every load-bearing mechanic/unique through the freshness + mechanics indexes before trusting it. Do not silently blend cross-version advice (same risk the community-survey playbook documents).
4. **Write the entry**: `{author}_{league}_{source}.json` (e.g. `balormage_3.28_poe-vault.json`). `tier` must be one of `league-starter · standard · uber · mageblood · aspirational`. Save the raw transcript/XML to `buffer/`.
5. **Update the archetype README**: best-guide-by-tier table, new pitfalls, consensus deltas ("guide 3 disagrees with 1-2 on X").
6. **Synthesis**: once the archetype has ≥2 entries, create/update `synthesis.md` (consensus / mechanic opportunities / trade-off map / open research questions).
7. **Offer the follow-up**: a `community-survey` pass on the archetype (its playbook positions itself as exactly this post-guide-analysis step). If purpose = (b), offer `build-comparison` against the character.

---

## Step 4 — Output shape

Everything lands in `character_data/guides/{archetype}/` (this directory **is committed** — no account names, session IDs, or personal economy data in entries):

- `{author}_{league}_{source}.json` — the entry
- `README.md` — updated tier table + pitfalls
- `synthesis.md` — created/updated at ≥2 entries
- `buffer/` — raw transcript / article dump / PoB XML (regenerable, safe to delete)

If purpose = (b), also append a journal entry in the character dir noting what the guide changes about the plan.

---

## Step 5 — Pitfalls

- **Transcripts are ~10-12K tokens** (README §2a cost table). Loading one into main context to "skim" defeats the sub-agent pattern — the digest must happen in the agent.
- **Fetch the YouTube description before the transcript.** It's a fraction of the cost and usually contains the pobb.in link, tier claims, and patch number — sometimes enough for a quick entry with no transcript at all.
- **Record `stored_stats` as the guide's *claimed* numbers — don't recompute them in PoB here.** Recomputation against a real character is `build-comparison`'s job; mixing the two makes the entry's provenance ambiguous.
- **A guide's league is a freshness claim about every mechanic it uses.** A 3.26 guide recommending a mechanic that `mechanics_index.md` marks `nerfed`/`removed` must be flagged in `notes`, not copied forward.
- **The root README's schema is the canonical minimum, not a maximum** — real entries add `guide_url`, `faq_url`, `trigger_skill`. Extra fields are fine; missing canonical fields are not.
- **Author names collide across leagues** — the `{author}_{league}_{source}` filename is what keeps a creator's 3.27 and 3.28 versions of "the same build" as separate entries. Never overwrite an old-league entry with a new-league update; add a new file.
