# Patch Notes Index — links to official PoE patch notes & hotfix threads

**Purpose:** A bookmark index of **patch-note sources** — the primary record of *what changed* in each
version. Pairs with `freshness_index.md`: the freshness index says *which mechanics postdate the running
model* (and must be verified); this index is *where to read the actual change* that introduced or altered
them. When a freshness entry says "verify," the patch notes here are the authoritative diff.

**Committed (not cached):** travels with the suite (gitignore exception, like `freshness_index.md` and
`guide_sources.md`) — a curated link index is useful to every clone.

## How GGG publishes patch notes (so you know where to look)

- **News page** — https://www.pathofexile.com/news — every release gets a news post; the fastest "what's
  the latest version" check.
- **Forum patch-notes threads** — each release has a forum thread (full notes for major versions; shorter
  notes for hotfixes). GGG posts these **first**, before the wiki transcribes them. This is the **primary
  source**.
- **Version numbering:** `X.Y.0` = a league/expansion launch (big notes). `X.Y.0a`, `X.Y.0b` … `X.Y.0j` …
  = sequential **hotfix/point releases** during that league (small notes, often bug/balance fixes). The
  wiki usually only has a single `Version_X.Y.0` page; **individual point releases live on the forum**, so
  bookmark them here as they're encountered.
- **Wiki transcription** — https://www.poewiki.net/wiki/Version_history lists every version; each links to a
  `Version_X.Y.0`-style page. Good for searchable, consolidated notes once they're up.

## Discovery anchors (stable — start here for anything not yet bookmarked below)

| Anchor | URL |
|---|---|
| **poepatchnotes.com (aggregator — fastest single check)** | https://poepatchnotes.com/ |
| PoE News (latest releases) | https://www.pathofexile.com/news |
| Wiki — Version history (all versions) | https://www.poewiki.net/wiki/Version_history |

> **poepatchnotes.com** (third-party, verified useful 2026-07-07): full text of every patch, point release,
> and hotfix on one page — including the granular `X.Y.0j Hotfix 2`-level entries the wiki never gets —
> each with a `[Source]` link to the official forum thread. PoE1 and PoE2 on separate pages. Use it as the
> first stop when the session-start hook reports a game patch; the forum threads it links to remain the
> primary source for anything load-bearing.

---

## Bookmarked threads / pages by version

Append a row whenever a specific patch-notes or hotfix thread is encountered. Official forum thread =
primary; wiki Version page = consolidated transcription.

| Version | Type | Official forum thread | Wiki Version page | Patch line |
|---|---|---|---|---|
| **3.29.0** | League launch | https://www.pathofexile.com/forum/view-thread/3985332 (posted 2026-07-16) | https://www.poewiki.net/wiki/Version_3.29.0 _(not yet populated at bookmark time)_ | **3.29 Curse of the Allflame** (launches 2026-07-24). Digested → `leagues/curse_of_the_allflame_3.29.md` (with drill-down ledger) |
| **3.28.0j** | Hotfix / point release | https://www.pathofexile.com/forum/view-thread/3974219 (posted ~2026-06-23) | — | 3.28 Mirage cycle; notes also cover the concurrent **Return of the Ancestors** event league |
| 3.28.0 | League launch | _(add when bookmarked)_ | https://www.poewiki.net/wiki/Version_3.28.0 | 3.28 Mirage |
| 3.27.0 | League launch | _(add when bookmarked)_ | https://www.poewiki.net/wiki/Version_3.27.0 | 3.27 Keepers of the Flame |
| 3.26.0 | League launch | _(add when bookmarked)_ | https://www.poewiki.net/wiki/Version_3.26.0 | 3.26 Secrets of the Atlas |
| 3.25.0 | League launch | _(add when bookmarked)_ | https://www.poewiki.net/wiki/Version_3.25.0 | 3.25 Settlers of Kalguur |

> ✅ **Resolved (2026-06-29):** 3.28 = **Mirage** (confirmed). The 3.28.0j notes reference **Return of the
> Ancestors** because it's a separate **~3-week event league** (2026-06-25 → 07-16) running *inside* 3.28
> Mirage (same client, same ladders) — not the 3.28 expansion. It's strongly build-relevant (alternate
> Phrecian ascendancies + Forbidden Tattoos). See `leagues/return_of_the_ancestors.md` and the freshness
> index entry.

## Maintenance

- Bookmark each point release (`X.Y.0a..z`) here as it's encountered — the forum is the only place most live.
- At a **league launch**, add the new `X.Y.0` row (forum thread + wiki page) and start its point-release chain.
- Keep `freshness_index.md`'s "Source bookmarks" in sync — it points to the wiki Version pages; this file adds
  the forum threads + the granular point releases.
