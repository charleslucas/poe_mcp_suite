# poe_mcp_suite — TODO Index

A thin discovery hub pointing to the work-tracking files scattered across the suite. The actual content lives in the linked files; this exists so you can land at the repo root and find everything in one place.

## Tracked at the suite level

- [**ISSUES.md**](ISSUES.md) — bug-style issues and behavioral surprises across the whole suite. Categories: tool quality / PoB calc behavior / hook integration. Each entry has a concrete repro and an *Affects:* scope.

## Tracked per subsystem

- [**pob-mcp/TODO.md**](pob-mcp/TODO.md) — pob-mcp roadmap: open work, deliberately-not-doing decisions (with reasoning preserved so they aren't re-litigated), and shipped record. Also hosts the **Playbook wishlist**.
- [**playbooks/README.md**](playbooks/README.md) — shared playbook meta-framework (cursory-vs-detailed gate, league pre-flight, narration norms, trust hierarchy) and links to each playbook. New playbooks needed are listed there.

## Tracked per character (local cache)

- `character_data/<Account>/<League>/<Character>/build.md` — each active character has an **Open Questions / Follow-ups** section at the bottom for deferred upgrades, alt-archetype explorations, gap-analysis follow-ups, etc.
- `character_data/` is a junction to `%APPDATA%/poe_claude_data/` on Windows (see `character_data/README.md`). The directory itself is gitignored — per-character notes don't travel with a fresh clone (tracked in [ISSUES.md](ISSUES.md) → *Open — data persistence*).

## Tracked per league (local cache)

- `reference_data/leagues/{current-league}.md` — the **FRESHNESS CHECKLIST** (rule / mechanic changes vs. pre-2024 knowledge — check before asserting how a mechanic works) and the **What's missing from this cache** section (gaps in the league reference to refresh later). Current league file: [`reference_data/leagues/mirage.md`](reference_data/leagues/mirage.md).
- `reference_data/` is gitignored — regenerable from poewiki + official patch notes, except for the hand-curated freshness-checklist entries, which would not survive a fresh clone (tracked in [ISSUES.md](ISSUES.md) → *Open — data persistence*).

---

## When adding new tracked work

Pick the right home based on **scope**, rather than dumping everything at the top level:

| Scope | Home |
|---|---|
| Suite-wide bug or behavioral surprise | `ISSUES.md` |
| Subsystem feature / roadmap | `<subsystem>/TODO.md` |
| New playbook needed | `playbooks/README.md` wishlist |
| Character-specific upgrade or question | that character's `build.md` |
| League-specific data gap | `reference_data/leagues/<league>.md` |

Update *this* index only when a **new tracked file or location** is introduced — not for each entry inside an existing one. The point is discoverability, not content duplication.
