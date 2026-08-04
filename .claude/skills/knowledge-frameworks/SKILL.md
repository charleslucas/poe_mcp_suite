---
name: knowledge-frameworks
description: Maintain the shared knowledge frameworks in frameworks/ — style templates (archetype rosters), the cross-build tech/concepts database, and the farming strategy roster. Use for "add X to the minions template", "survey how people farm currency", "record this tech", "re-stamp farming tiers for the new league", or standing up a new framework (totems, melee, ...). Runs surveys through the existence/obtainability gates and confidence labels.
---

This task uses the **Knowledge Frameworks** playbook. The playbooks in `playbooks/` are the single
source of truth — read them rather than working from memory.

1. Read `playbooks/README.md` first — the shared meta-framework (cursory-vs-detailed gate, pre-flight,
   trust hierarchy, narration norms).
2. Then read `playbooks/knowledge-frameworks.md` and follow it.

Key points:
- Frameworks live in `frameworks/` (committed, public); character/archetype instances stay in the
  private guide library.
- Gate every survey claim: existence (fuzzy-grep names!), obtainability, mechanics_index scope.
- Label everything ✅/◐/⛔ and keep ⛔ rows with reasons; record aliases and references as encountered.
- Ledger every survey with date, queries, and source quality.
