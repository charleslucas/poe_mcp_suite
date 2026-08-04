# frameworks/ — meta-build guides, tech library, farming roster

Curated, contribution-ready knowledge layers that sit *above* any one build or character. Built and
field-tested in live sessions (first instances: 2026-08-04); **open to PRs** — same bar as `playbooks/`
(see `playbooks/README.md` §9): tested in at least one real session, provenance labeled, pitfalls specific
and falsifiable.

| Framework | What it holds |
|---|---|
| [`styles/`](styles/minions.md) | **Meta-build guides** (style templates) — the layer above build archetypes. Per style (minions first): decision axes, archetype roster with aliases, shared infrastructure ("best-known practices"), staged acquisitions by level band, verified traps, dated survey ledger. Use one to *design* a build of that style, then hand off to `playbooks/build-design.md`. |
| [`concepts/`](concepts/README.md) | **Tech library** — mechanisms/pairings that work across unrelated builds (conversion ladders, trigger automation, charge engines). One file per tech: aliases, mechanism *including the intuitive-but-wrong version*, availability, references, builds using it. |
| [`farming/`](farming/README.md) | **Farming strategy roster** — currency-making strategies with aliases, investment/attention/payout axes, build-fit, and **league-stamped** viability. Feeds `playbooks/atlas-planning.md` sessions. |

## Conventions (uniform across all three)

- **Confidence labels on every claim:** ✅ verified (sim / in-game / game-data) · ◐ community-sourced,
  unverified · ⛔ dead or wrong — **kept in the doc deliberately** so it isn't re-proposed; the *why* of a
  dead end is often the most valuable line in the file.
- **Aliases:** community names for everything — different groups name the same thing differently, and
  aliases are the search keys for future surveys. Record as encountered; never invent.
- **References:** YouTube videos, published guides, and detailed reddit tutorial threads, dated/patch-tagged
  where known. Reddit threads are where techs get *named*, so they feed the aliases field.
- **Obtainability gate before anything is presented as actionable** (full version:
  `playbooks/gear-shopping.md` pitfalls): spawn weight → variant → slot legality → market. Plus the
  fuzzy-name rule: an exact-string miss is NOT nonexistence — community sources garble proper nouns
  ("Bladefall of the Tarter" → **of Trarthus**).
- **League stamps:** viability claims carry the patch they were surveyed in and expire at league
  transition — the entry survives, its verdict gets re-surveyed.
- **Survey ledger:** every framework ends with dated survey entries recording queries run, what was found,
  what was refuted, and source quality (a `sources: []` AI answer is synthesis, not retrieval).

## Publication policy — the evidence ladder

**The criterion is observable: "has this been seen to work in the actual game, and can we get data on
that?"** A video of someone actually playing it, ladder presence, or a measured build of a played
character. Three tiers, each with a defined promotion:

1. **Private-conceptual** (personal stash, not in this repo): raw seeds — "new unique, maybe build around
   it." Stays private until fleshed out to at least the detail of a good r/PathOfExileBuilds post.
   **Promotion mechanism can literally be making that post** — publishing to the community's venue.
2. **Public-experimental** (here, labeled ◐ EXPERIMENTAL): surfaced in a reputable venue and worthy of
   investigation, but no play data yet. The repo *indexes* the experiment (link to the post), it doesn't
   host the speculation. Promotes when play data appears.
3. **Proven** (here, ✅ with evidence linked): seen to work in the actual game, data attached in the
   References field. League re-stamps can demote — evidence from three patches ago degrades back to
   experimental.

**Class is a view, style is canonical** — [`styles/by-class.md`](styles/by-class.md) indexes builds the way
players search (by class/ascendancy) while the style files keep shared infrastructure unduplicated.

## Relationship to the maintainer's private library

These frameworks were extracted from a local guide library that also holds **character data and digested
third-party guide content — neither is distributed**. `local library:` citations in the files refer to that
private layer; treat them as worked-example provenance. Your own instances (characters, guide digests) wire
in the same way — the frameworks are the shareable layer.

Maintenance procedure: `playbooks/knowledge-frameworks.md`.
