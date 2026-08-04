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

## Publication policy

1. **Vetting gate: proven out with actual play.** Vetted/common builds and techs that people can succeed
   with. Experimental and concept-tier material stays in each contributor's personal stash (private
   library) until play-proven — then it graduates here with its evidence.
2. **Class is a view, style is canonical** — [`styles/by-class.md`](styles/by-class.md) indexes builds the
   way players search (by class/ascendancy) while the style files keep the shared infrastructure unduplicated.

## Relationship to the maintainer's private library

These frameworks were extracted from a local guide library that also holds **character data and digested
third-party guide content — neither is distributed**. `local library:` citations in the files refer to that
private layer; treat them as worked-example provenance. Your own instances (characters, guide digests) wire
in the same way — the frameworks are the shareable layer.

Maintenance procedure: `playbooks/knowledge-frameworks.md`.
