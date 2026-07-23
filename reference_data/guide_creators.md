# Guide Creator Registry — build-guide authors worth surveying

**Purpose:** A curated list of PoE build-guide *creators* (people/channels) who consistently produce
sound, useful builds — the ones worth **periodically surveying** to see what interesting builds they're
publishing this league. This is a third discovery dimension, distinct from the other two:

- [`guide_sources.md`](guide_sources.md) — *aggregator sites* (poe.ninja, Maxroll, Mobalytics, …): "where to find guides."
- `character_data/guides/{archetype}/` — guides **already digested** for a specific build.
- **This file** — *individual authors*: "whose new output to check on a cadence."

**Committed (not cached):** like [`guide_sources.md`](guide_sources.md) and [`freshness_index.md`](freshness_index.md),
this travels with the suite (gitignore exception) — a curated creator list is useful to every clone, unlike the
per-character digested guides in the gitignored `character_data/` cache.

**How to survey (cadence):** every few weeks, or at a new league / big patch, walk the table and check each
creator's **live survey source** (their YouTube uploads / channel, not necessarily their personal site — those
go stale). Note anything interesting. When a specific build looks worth committing to, **digest** it into
`character_data/guides/{archetype}/` via the guide-analysis skill (`Skill guide-analysis`), and back-link the
entry here. Keep the `Last surveyed` column current so gaps are visible.

**Trust reminder** (full hierarchy in `playbooks/README.md` §5): a trusted creator is a good *filter*, not
ground truth. Their builds are still patch-dated secondary sources — verify mechanics/values against live tools
+ [`freshness_index.md`](freshness_index.md) before asserting how anything works.

---

## Creators

| Creator | Live survey source | Focus / philosophy | Notable archetypes | Digested in library | Last surveyed |
|---|---|---|---|---|---|
| **BalorMage** | [YouTube @Balormage](https://www.youtube.com/@Balormage/videos) · [PoE Vault author](https://www.poe-vault.com/guides) · [poebuilds.cc](https://www.poebuilds.cc/poe/author/balormage/) | **QoL / ease-of-use over max DPS** — league-starter-friendly, low-button, returning-player oriented. Veteran (playing since Bloodlines, content since 2015; co-hosts the *Fated Connections* podcast). | Poison SRS Necromancer (long-running signature), Holy Relic Necromancer, EA Totem Hierophant | ✅ [`holy-relic-necromancer/`](../character_data/guides/holy-relic-necromancer/) + [`poison-srs-necromancer/`](../character_data/guides/poison-srs-necromancer/) (both his guides) | 2026-07-22 |

---

## Per-creator notes

### BalorMage
- **Where to actually survey:** his **YouTube channel** ([@Balormage](https://www.youtube.com/@Balormage/videos))
  is the live feed of current builds; **PoE Vault** carries his written guides (currently 3.29 Curse of the
  Allflame: Holy Relic Necromancer, Poison SRS Necromancer). ⚠ His personal site
  [balormage.com/build-guides](https://balormage.com/build-guides/) is **stale** (builds from 3.9–3.14) — don't
  rely on it for current output.
- **Signature build:** Poison Summon Raging Spirits (SRS) Necromancer — a perennial league-starter he re-updates
  most leagues ("...Because It Never Changes"). Reliable, cheap-entry minion starter; league-start viable at
  level 8, with low/medium/high-budget progression tiers. Positioned as league-starter + bosser + all-rounder.
- **Why he's on the list:** already vetted indirectly — his Holy Relic Necromancer guide is the anchor of
  [`character_data/guides/holy-relic-necromancer/`](../character_data/guides/holy-relic-necromancer/) (see that
  folder's README for the cross-check against other sources; single-author guides warrant corroboration).
- **Seed link (this entry's origin):** [PoE Vault — Poison SRS Necromancer](https://www.poe-vault.com/guides/balormage-summon-raging-spirits-necromancer-build-guide)
  (3.29 Curse of the Allflame, updated 2026-07-21) · PoB: https://pobb.in/kio7xkhMV23W . ✅ Digested 2026-07-22
  → [`poison-srs-necromancer/`](../character_data/guides/poison-srs-necromancer/).

---

## Adding a creator
Add a row when a creator's output proves consistently sound and worth periodic review. Fill in the **live survey
source** (prefer their YouTube/channel feed over a personal site), their **focus/philosophy** (what niche they own,
what they optimize for), **notable archetypes**, any **library back-links**, and set `Last surveyed`. Add a
`### Name` notes block for anything richer (caveats, where their site goes stale, signature builds). Remove or mark
a creator if their output quality drops or they go inactive.
