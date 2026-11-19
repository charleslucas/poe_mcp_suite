---
name: stash-scanning
description: Stash tab scanning and item pricing — list/get/price stash tabs (POESESSID, undocumented endpoint working as of 2026-11-18), score_rare for single items.
when_to_use: Use for scanning or pricing stash contents — "what's in my stash worth selling", "price my dump tab", "is this item worth listing", "what should I vendor". Stash tools take an optional league (default POE_LEAGUE; pass "Standard" for Standard tabs).
---

This task uses the **Stash Scanning** playbook. The playbooks in `playbooks/` are the single source of truth — read them rather than working from memory, so you always get the current version.

1. Read `playbooks/README.md` first — the shared meta-framework (cursory-vs-detailed gate, context/pre-flight protocol, league reference, trust hierarchy, narration norms).
2. Then read `playbooks/stash-scanning.md` and follow it for this task.

Read the playbook's "Current status" section first: it covers the league argument, what 403 and 404 mean, and the ToS caveat on this endpoint.

Do not summarize or duplicate the playbook content here.
