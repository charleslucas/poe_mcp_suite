# Playbook: Knowledge Frameworks (styles / concepts / farming)

Maintain the shared knowledge layers in [`frameworks/`](../frameworks/README.md): **style templates**
(archetype rosters + shared infrastructure), the **tech/concepts database** (cross-build mechanisms), and
the **farming strategy roster**. Covers adding entries, re-stamping at league transitions, and standing up
a new framework of the same shape.

**Triggers:** "add X to the minions template", "survey how people are farming", "is tech Y worth recording",
"re-stamp the farming tiers for the new league", "create a style template for totems/melee/…".

---

## Step 0 — Frame the work

*"Updating the [X] framework — surveys → gate → label → ledger. Frameworks live in `frameworks/`
(committed, public); character/archetype instances stay in the private library."*

Cursory when it's one entry from data already in hand; **detailed** (pause for approval) when it means a
survey battery or a new framework.

## Step 1 — Triage

1. **Which framework** — style / concept / farming — or a **new framework**? (A new one must justify a new
   *shape*: would its entries fit an existing table?)
2. **Operation:** new entry · verify/upgrade an entry (◐→✅/⛔) · league re-stamp · roster-gap survey.
3. **Scope context:** which league/patch is being surveyed, and does `reference_data/mechanics_index.md`
   scope-tag any mechanic involved (`removed` / `event-only` / `disabled-this-league`)?

## Step 2 — Data loads

| Always | Purpose |
|---|---|
| The target framework file | current state + its survey ledger (don't re-run answered queries) |
| `reference_data/mechanics_index.md` | scope gate for league content |
| Text lake (`rg --no-ignore`, via Bash) | existence-gating survey claims |

Add for surveys: `playbooks/community-survey.md` (query framing — open-ended, cite-seeking, year-tagged).
Add for tech verification: `get_gem_detail` / `get_tree_node` / live PoB sim.
Add for farming re-stamps: `currency_overview` (prices stale in hours), current league doc.

## Step 3 — The loop

1. **Survey** with community-survey's framing. Let the community define its own terms — the aliases you
   collect are next survey's keys.
2. **Gate every claim** before it enters a table:
   - Existence: text lake / `get_gem_detail` / `uniques.txt`. **Exact-string miss ≠ nonexistence — fuzzy-grep
     the base name first** (the "of the Tarter"→"of Trarthus" rule).
   - Obtainability: the four-step gate in `gear-shopping.md` pitfalls.
   - Scope: mechanics_index (a Crucible-dependent strategy is dead this league).
   - Freshness: claims about "how X works now" beat your training *and* old guides — but verify the load-
     bearing ones (the Dead-Reckoning-obsolete catch came from a survey; the AG-UI claim died against
     patch notes).
3. **Label** ✅/◐/⛔ — and keep the ⛔ rows with their reasons. Label source quality too: `sources: []`
   responses are synthesis; r/pathofexile2builds citations are a different game.
4. **Write**: entry into the roster/table with aliases + references (videos, guides, reddit tutorials).
5. **Ledger**: dated survey entry — queries, findings, refutations, contradictions *preserved* (two
   verdicts on one mechanic usually means two investment tiers, not an error).

### Step 3b — YouTube evidence pipeline (applies to ALL frameworks — builds AND farming alike)

Videos are the best verifiable play-evidence (the ladder's "seen to work in the actual game, with data"),
and the suite already has the tools. For any entry claiming play-proof, or any creator surfaced by survey:

1. **Discover** — surveys return video links directly; standing creator targets live in
   `reference_data/guide_sources.md` (BawLoch, Redviles, GhazzyTV, Zizaran, …). There is no YouTube-search
   tool: discovery goes through surveys, the source index, or the user.
2. **Description first** (`fetch_youtube_description` — cheap): extracts PoB links (pobb.in/pastebin) and
   guide-site links automatically; title usually carries the patch tag. Often enough to verify + Reference
   without the transcript.
   ⓘ **If a youtube tool times out, the cause is a broken console — not YouTube** (root-caused 2026-08-09;
   the long-standing "stalls transiently, retry later" note was wrong and cost many retry cycles).
   Symptom: the `yt-dlp` child IS created but sits at **0s CPU**, loader threads waiting on EventPairLow
   (the LPC handshake with the console host), until the timeout kills it — one frozen process leaked per
   attempt. Cause: the harness launches the MCP server with a console whose `conhost.exe` never finishes
   initializing (alive, 2 threads, ~0.01s CPU), so any child inheriting that console blocks forever.
   Fixed in `poe_data_mcp/sources/youtube.py` by spawning children with `CREATE_NO_WINDOW` (+
   `stdin=DEVNULL`) via the `_run()` helper — **a fix that needs an MCP restart to take effect**.
   Diagnostic worth reusing on any "MCP tool that shells out hangs" report: poll
   `Get-CimInstance Win32_Process -Filter "ParentProcessId = <server pid>"` for CPU + thread count. A
   healthy yt-dlp reaches ~30 threads and measurable CPU within a second; 4 threads at 0s CPU means the
   child never started, which points at the OS, not the network.
   **Fallback if it ever recurs — Bash works regardless** (~3s):
   `python -m yt_dlp --get-title --get-description --force-ipv4 --no-warnings <url>`, and
   `--write-auto-sub --skip-download --sub-format vtt -o <scratchpad>/%(id)s` for transcripts.
3. **Transcript when depth is needed** (`fetch_youtube_transcript`): chapter markers first for navigation;
   full transcript ~10-12K tokens, so per `playbooks/README.md` §6 delegate digestion to a sub-agent for
   long videos rather than loading raw into main context.
4. **Extract:** (a) *is it actual play* — gameplay narration vs pure theorycraft distinguishes evidence
   tiers; (b) numbers said aloud (div/hr, DPS) as ◐ until cross-checked; (c) **aliases** — creators name
   strategies/techs on camera before anyone writes them down; (d) links for the References field.
5. **Land it:** References entry with creator, patch, URL; ledger line; tier promotion if the evidence bar
   is met. Per-build deep digestion stays with `guide-analysis.md` — this pipeline is for framework-level
   rosters and evidence verification, not full build digests.

## Step 4 — Output shape

The framework file itself is the artifact. Cross-link: styles ↔ concepts (techs referenced, not restated),
farming → `atlas-planning` for implementation. Promotion conventions: IDEA → CANDIDATE → BANKED/REALIZED;
REJECTED keeps its row + cause + date.

## Step 5 — Pitfalls (all field-hit, 2026-08-04)

- **AI-search garbles proper nouns — in BOTH directions.** Fuzzy-gate names before declaring them fake ("Bladefall of the Tarter" was real gem *of Trarthus*), and treat synthesis tells (`sources: []`, no direct links, odd-looking handles) as **unverified, never probably-fake**: three creator names flagged as likely-invented (untagatunu, BawLoch, Redviles) were all real people with slightly mangled spellings. Synthesis names are mangled pointers — a 30-second reddit/YouTube search resolves them; presumption in either direction does not.
- **Survey praise omits exclusivity costs** — The Dark Monarch was "mandatory for spectre builds" with no
  mention that every variant forbids all other minions. Pull the full item text before rostering.
- **Same mechanic, opposite verdicts = investment tiers** — Essence is both a budget starter (unjuiced) and
  a slow-build trap (scarab-juiced). Record the axis, not one verdict.
- **Claims about your own gear beat surveys** — "United in Dream grants Unholy Might" died against the
  owned copy's actual mods. Owned-item text is trust-hierarchy #1.
- **Farm demand, not bugs** — durable-vs-transient test for any farming entry: if its profitability depends
  on a broken interaction, stamp it accordingly; hotfixes kill it mid-league.
- **League stamps expire** — at transition, sweep every stamped verdict (league-transition checklist step).
