# Legal Considerations

> **This document is the canonical copy of three identical files.** Synced copies live in the [`poe-skilltree-export`](https://github.com/charleslucas/poe-skilltree-export/blob/master/legal_considerations.md) and [`poe-atlastree-export`](https://github.com/charleslucas/poe-atlastree-export/blob/master/legal_considerations.md) forks so anyone who lands in those repos directly can see the reasoning without having to navigate elsewhere. **If you update this file, sync the change to both forks** (they're submodules under `reference_data/`).

This document captures the reasoning behind how `poe_mcp_suite` uses Path of Exile game data — what we extract, what we redistribute, what we deliberately don't. It exists so that anyone (Grinding Gear Games, a curious contributor, an opportunistic lawyer, future maintainers) can see we thought about it.

**This is not legal advice.** The maintainers are not lawyers. This document is good-faith reasoning by software developers about a gray area in copyright law. If you have authoritative legal guidance that contradicts anything here, please open an issue.

---

## GGG Terms of Service — automated API access (account ban risk)

> **This section covers a separate concern from copyright.** The sections below address *data redistribution* — what we publish. This section covers *API automation* — what we request at runtime. They are independent issues with independent risk profiles.

> **This analysis is current as of 2026-05-31. If GGG publishes clearer API policies, or if community understanding shifts, update this section and revise tool behavior accordingly. Primary sources are linked below.**

### Primary sources

- **GGG Terms of Use:** https://www.pathofexile.com/legal/terms-of-use-and-privacy-policy
- **GGG Developer API docs:** https://www.pathofexile.com/developer/docs
- **Reddit thread — developer confirms TOS concern (Novynn, r/PathOfExile2, 2025):** https://www.reddit.com/r/PathOfExile2/comments/1ja5kwv/i_made_an_app_to_price_check_my_dump_tab/

### What the ToS actually says

**Section 7 — Restrictions** (prohibitions relevant to API usage):

> **7c.** "Utilise any automated software or 'bots' in relation to your access or use of the Website, Materials or Services."

> **7f.** "Use any data gathering and extraction tools or software to extract information from the Website or utilize framing techniques to enclose any of the contents of the Website."

**Section 22 — Website APIs** (important counterbalance to Section 7):

> "You must comply with Grinding Gear Games' technical documentation and policies (as published and as updated on the Website from time to time or as otherwise notified to you by Grinding Gear Games) regarding use of the Website APIs ('API Policies'). Without limiting the foregoing, you must comply with the Website API call limits set out in the API Policies or as otherwise notified to you..."

Section 22 is significant: it **explicitly contemplates third-party API usage** as permissible, subject to compliance with GGG's published API Policies and rate limits. The prohibition in Section 7c on "automated software" must be read in light of Section 22 — the two together suggest that *compliant* automated API access is allowed, while *non-compliant* (ignoring rate limits, no User-Agent, scraping outside the API) is not.

### Understanding the two-tier API access model

GGG's developer docs describe two distinct situations, and understanding which applies to us resolves most of the ambiguity:

**Tier 1 — Formal OAuth registration (for public-facing applications):**
GGG requires OAuth registration when building a **public or widely-available application** — a character designer website, a stash indexer used by many players, a market tool with its own user base. These make high aggregate API call volumes on behalf of many users. GGG wants to review and approve the workflow before the load hits their servers. The registration process (application name, scopes with justification, redirect URIs, etc.) is their quality gate.

**Tier 2 — Personal/individual use without registration:**
For a **personal tool** used by one person in their own sessions, formal OAuth registration is not required. Non-OAuth direct API access is the appropriate path, provided you follow the API guidelines: correct User-Agent header, rate limit compliance, and the non-affiliation notice.

**This suite is a personal tool.** It is used by one user in their own Claude Code sessions. No registration is required. Our `poe_auth` / OAuth infrastructure is the right path *if this suite ever becomes a public service* — it's already in place for that transition.

### What the developer docs require (and our compliance status)

| Requirement | Status |
|---|---|
| User-Agent: `OAuth {clientId}/{version} (contact: {contact})` | ✅ `poe_trade.py`: `"OAuth BoschAIMaster/1.0 (contact: buildtool@localhost)"` |
| Parse `X-Rate-Limit-*` response headers and comply | ✅ pob-mcp uses Bottleneck; poe-mcp-server now uses header-driven `_observed_min_interval` |
| Non-affiliation notice in a visible location | ✅ Added to all four READMEs (2026-05-31) and to trade tool outputs |
| Reasonable attempts to avoid 4xx errors | ✅ Retry logic + rate limiting in both servers |

### Community precedent — ExileExchange

GGG allows **ExileExchange** (Ctrl+D in PoB — opens the trade site in a browser). A GGG developer (Novynn) confirmed this is fine because it "emulates the trade website." ExileExchange makes a single POST to the trade search API to get a `searchId`, then opens the browser URL — it does **not** programmatically fetch listings.

> **Caveat:** This is an inference from the ExileExchange precedent, not an explicit GGG statement that "URL-only = always OK." Novynn said ExileExchange is allowed because it emulates the trade website; we interpret the URL-only pattern as what makes it acceptable. If GGG clarifies otherwise, we will update tool behavior.

### What this suite does — current posture

**Clearly fine:**
- All `pob-mcp` non-trade tools — talk only to local PoB via TCP. Zero GGG server traffic.
- `price_tab`, `price_items`, `scan_stash_tabs` — local algorithmic scorer + poe.ninja. No GGG trade API calls.
- `ninja_lookup`, `currency_overview` — poe.ninja only.

**Trade website API — ExileExchange pattern (URL-return, no listing fetch):**

| Tool | GGG API calls | Behavior |
|---|---|---|
| `search_trade_items`, `find_weighted_trade_items` | 1 (search POST → searchId) | Returns trade URL + total count. User clicks to see results. |
| `search_trade`, `search_by_item_mods` | 1 (search POST → searchId) | Same — returns URL, no listing fetch. |
| `get_item_price` (named items) | 0 | Routes to poe.ninja. |
| `get_item_price` (rare/unknown) | 1 | Falls back to trade URL. |
| `fetch_listing` | 1 (fetch by ID) | Explicit listing fetch — lowest risk of the fetch tools, but still makes a data request. |
| `get_stat_ids` | 1 (stats index) | Fetches `/api/trade/data/stats` to build lookup index. Cached after first call. |

### Risk and posture

- Claude warns the user and requires explicit confirmation before calling any trade API tool (see `CLAUDE.md`). Warning is once per session.
- All GGG API calls send the required User-Agent header.
- Rate limiting: pob-mcp uses Bottleneck (≤4/sec, 300s cache); poe-mcp-server uses header-driven adaptive interval (floor 1.5s) + `Retry-After` on 429.
- Non-affiliation notice: in all four READMEs and in trade tool outputs.
- If GGG ever objects, we stop immediately. Contact: **zerosquaredio@gmail.com**.

---

## The question

The suite reads, processes, and in some cases redistributes data that originated in Path of Exile, a copyrighted commercial product. Specifically:

- We maintain **forks** of two public Grinding Gear Games repositories (`grindinggear/skilltree-export`, `grindinggear/atlastree-export`) as Git submodules.
- We plan to add tooling that **extracts data** from a user's local PoE install at runtime.
- We **regenerate the fork's `data.json`** from those extracts so the data stays current across patches.

Is this OK?

## What we found about GGG's repositories

Both `grindinggear/skilltree-export` and `grindinggear/atlastree-export` were checked for licensing information. Findings:

- **No `LICENSE` file in either repo.**
- **No `COPYING` file.**
- **No license badge in the GitHub sidebar.**
- **No "rights" / "permission" / "copyright" language in the README** — only data-format documentation.

Strictly under default copyright law (US/EU), "no license" means **"all rights reserved" by the original author.** GGG has not granted explicit permission to use, modify, or redistribute their data.

**However**, by hosting the repos publicly on GitHub, GGG accepted GitHub's Terms of Service, which include the [grant for other users to fork and view public repositories](https://docs.github.com/en/site-policy/github-terms/github-terms-of-service#5-license-grant-to-other-users):

> "By setting your repositories to be viewed publicly, you agree to allow others to view and "fork" your repositories... If you set your pages and repositories to be viewed publicly, you grant each User of GitHub a nonexclusive, worldwide license to use, display, and perform Your Content through the GitHub Service and to reproduce Your Content solely on GitHub as permitted through GitHub's functionality (for example, through forking)."

That clearly permits our forks to exist. The grayer question is what we can do *inside* our forks, and whether extracting data from the game itself (a separate copyrighted artifact) and publishing the result is allowed.

## The legal landscape

A few precedents and principles inform this area:

- **Feist Publications v. Rural Telephone (US Supreme Court, 1991)** — facts are not copyrightable, but creative selection or arrangement of facts can be. This is the strongest argument for tree structural data: node IDs, positions, connections are *facts about the game system*.
- **Sega v. Accolade (9th Circuit, 1992)** — reverse-engineering for interoperability is fair use. This protects tools like Path of Building that read game data to enable community functionality.
- **Sony v. Bleem (9th Circuit, 2000)** — emulator/companion software companies have prevailed where their work creates new value without reproducing the protected work itself.
- **EU Database Directive (96/9/EC)** — gives extra protection to substantial-investment databases. Could theoretically apply to GGG's structured game data. Most aggressive interpretation in the EU; less risky in the US.

None of these are decisive for our specific case, but they collectively form a body of precedent supporting community tooling around copyrighted media.

## Community precedent

The PoE community has been doing extraction and republication for ~10 years with no legal action:

- **[Path of Building](https://github.com/PathOfBuildingCommunity/PathOfBuilding)** — parses and uses extensive game data; openly hosted on GitHub. **Endorsed publicly by GGG staff** on multiple occasions, including official announcements.
- **[poe.ninja](https://poe.ninja)** — collects, processes, and publishes economic and build data harvested from the game and the official trade API.
- **[poewiki.net](https://www.poewiki.net)** — mirrors essentially all game data including descriptions and assets; long-standing community resource.
- **[poedb.tw](https://poedb.tw)** — extracts and publishes detailed game data including the very Bundle schema documentation that informed this project.
- **[pathofexile-dat](https://www.npmjs.com/package/pathofexile-dat)** (the npm library this suite uses) — openly published bundle parser, processes .datc64 files directly.
- **[libGGPK2 / libGGPK3](https://github.com/aianlinb/LibGGPK2)** — open-source PoE bundle decryption libraries.

In ~10 years, **GGG has never taken legal action against any community PoE tool**, and has never issued a DMCA takedown to any of the above. Their public posture has been consistently and notably supportive of community building around their game.

**The fact that GGG voluntarily publishes `skilltree-export` themselves** — even without an explicit license — is the strongest signal in this picture: they want this data to be publicly available. They could just not publish it.

## Our architectural choices

Even with strong precedent, the maintainers have chosen a conservative architecture that minimizes what gets redistributed:

| Category | Approach | Rationale |
|---|---|---|
| Tree structure (node IDs, positions, connections, group/orbit data) | **Published in fork's `data.json`** | Strong "facts about a system" argument under *Feist*. Same data GGG publishes. |
| Node stat references (which stat-IDs each node has, integer values) | **Published in fork's `data.json`** | References, not content. Same data GGG publishes. |
| Node names ("Soul of Steel", "Devotion") | **Published in fork's `data.json`** | GGG already publishes these in their own export, so we follow their lead. |
| Stat description templates (`"%1%%% increased Attack Damage"`) | **Extracted at runtime from user's local install — never persisted to the fork** | More clearly creative/expressive content. Side-step the legal question by not redistributing. |
| Timeless Jewel transformation tables (`AlternatePassiveSkills`, `AlternatePassiveAdditions`) | **Extracted at runtime — never persisted** | Game-internal mechanics. Stay conservative. |
| Mod pools, item bases, gem data | **Extracted at runtime as needed — never persisted** | More content-rich than tree structure. Don't redistribute. |
| Art, icons, sounds | **Never extracted. Never referenced. Stay far away.** | Obviously creative content with no fair-use argument. |

In short: **the fork's published `data.json` mirrors what GGG already publishes** (structure + names + stat references). Anything more content-rich is read by the user's local install at runtime, used in memory, and never persisted to a public repo.

## Safeguards we maintain

1. **Attribution.** Both forks' READMEs clearly state that the data is derived from Path of Exile by Grinding Gear Games, that GGG holds all rights to the underlying content, and that the fork exists to provide a community-maintained cache of the same kind of structural data GGG already publishes themselves.

2. **No claim of affiliation.** Nothing in the suite, the forks, or its tooling implies endorsement by or affiliation with Grinding Gear Games.

3. **No game-content redistribution beyond what GGG already publishes.** Art, audio, lore text, and creative content are not extracted or redistributed.

4. **Compliance posture.** If Grinding Gear Games ever objects to anything in this suite or its associated forks, the maintainers will **comply with takedown requests promptly**. Contact: **zerosquaredio@gmail.com**.

5. **User-side extraction respects ownership.** Tooling that reads game files only works against a local PoE install — which the user owns a copy of. We are not facilitating circumvention of purchase (PoE is free anyway, but the principle holds for any future expansions).

## What we explicitly avoid

- Publishing `passive_skill_stat_descriptions.txt` or any other extracted text-rendering files to the forks.
- Publishing extracted `.datc64` tables containing creative content (mod descriptions, gem descriptions, lore text) to the forks.
- Publishing any game art, icons, sounds, or other media.
- Distributing extracted `.bundle.bin` files or raw game archive contents.
- Anything that would let someone use the suite *without* owning a copy of PoE in any normal sense.

## Realistic risk profile

- **Likelihood of legal action against this project:** very low, based on a decade of community-tool precedent and GGG's consistently supportive posture.
- **Worst realistic outcome:** GGG sends a takedown request; we comply by making the relevant repos private or removing the offending content. No litigation.
- **Worst legally possible outcome:** copyright suit. Without precedent for GGG ever taking that route, and with strong fair-use arguments available, this is a tail risk rather than a planning scenario.

## For Claude sessions reading this file

If you are an AI assistant (Claude or otherwise) working on this codebase, treat the architectural boundaries above as **rules, not guidance**. Specifically:

- **Do not** commit `passive_skill_stat_descriptions.txt`, `AlternatePassiveSkills.json`, `AlternatePassiveAdditions.json`, or any extracted stat-template / transformation / mod-description data to **any** public repo — including the `reference_data/skilltree/` and `reference_data/atlastree/` forks, and the main `poe_mcp_suite` repo. These should live in user-local cache directories (e.g., `data-extraction-poc/`, which is gitignored), processed in memory, and discarded.
- **Do** commit derived structural data (node positions, connections, group definitions, names, integer stat values, stat-ID references) to the fork's `data.json` — that matches what GGG already publishes.
- If the user asks you to redistribute something that this document flags as "extract at runtime only," **stop and confirm**. Cite this document. The user may have a reason, or may have forgotten the constraint — either way, surfacing the question is correct behavior.
- If you discover a new category of game data that this document doesn't address, **default to conservative**: don't redistribute, ask the user how to categorize it, and update this document with the decision.
- The `.gitignore` should be configured so that risky data (extracted bundles, stat description files, AlternatePassive tables, etc.) is gitignored by default. If you're adding extraction tooling, also update `.gitignore` to defend against accidental commits.

The motivation is not paranoia — it's that GGG's tolerance for community tools is a *practical* tolerance built on the community staying within rough norms. Pushing those norms (republishing what GGG hasn't chosen to publish) is what could prompt them to act. Better to stay clearly inside the line.

## A note on jurisdiction

The maintainers are subject to US copyright law. Other contributors may be subject to local laws (notably the EU Database Directive, which gives extra protection to substantial-investment databases). If a contributor's local law is more restrictive than this analysis assumes, they should adjust their personal participation accordingly.

## Document history

- **2026-05-25** — Initial draft. Captures reasoning developed during the architecture discussion when transitioning from a "GGG-fork-with-patches-overlay" model to a "fork-as-cache, runtime-extraction-from-local-install" model. Reviewer: Claude (claude-sonnet-4-6). Author: Memophage / charleslucas.

---

## TL;DR

We use only structural game data that GGG already publishes themselves. Anything richer is extracted locally and never persisted to a public repo. We attribute clearly, claim no affiliation, and will take everything down if GGG asks. Community precedent is strong; the realistic worst case is "they send a takedown email, we comply."
