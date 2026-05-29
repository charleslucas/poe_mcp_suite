---
name: league-transition
description: End-of-league migration checklist for the suite — update POE_LEAGUE, fix character meta.json league fields, invalidate cached prices, and bootstrap the new league's reference doc when a PoE temp league ends and a new one launches.
when_to_use: Use when a PoE league is ending or has ended, or a new league launched — "the league is ending", "prep for the new league", "Mirage is over what do I update", or when get_active_leagues warns POE_LEAGUE points to a league no longer active.
---

This task uses the **League Transition** playbook. The playbooks in `playbooks/` are the single source of truth — read them rather than working from memory, so you always get the current version.

1. Read `playbooks/league-transition.md` and follow its checklist for this task.
2. The shared meta-framework in `playbooks/README.md` is optional here — this is a deterministic procedure, not a data-heavy analysis — but read it if you need the context/league-reference conventions.

Do not summarize or duplicate the playbook content here.
