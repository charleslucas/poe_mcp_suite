---
name: stash-scanning
description: Stash tab scanning and item pricing — evaluating stash contents to find items worth listing, vendoring, or keeping. NOTE - bulk stash tools are currently blocked (GGG disabled the legacy stash endpoint; OAuth developer registration required for full access). score_rare works today for individual items.
when_to_use: Use when the user wants to scan or price stash tab contents — "what's in my stash worth selling", "price my dump tab", "is this item worth listing", "scan my stash", "what should I vendor". IMPORTANT - immediately inform the user that bulk stash scanning is currently blocked and explain the three options (score_rare for individual items, OAuth registration if they want full access, or waiting for GGG to restore the endpoint). Do not attempt list_tabs or get_tab — they will return 403.
---

This task uses the **Stash Scanning** playbook. The playbooks in `playbooks/` are the single source of truth — read them rather than working from memory, so you always get the current version.

1. Read `playbooks/README.md` first — the shared meta-framework (cursory-vs-detailed gate, context/pre-flight protocol, league reference, trust hierarchy, narration norms).
2. Then read `playbooks/stash-scanning.md` and follow it for this task.

**CRITICAL:** Read the "Current status: BLOCKED" section first before attempting any stash tools. `list_tabs`, `get_tab`, `scan_stash_tabs`, and `price_tab` all return HTTP 403. Use `score_rare` for individual item evaluation instead.

Do not summarize or duplicate the playbook content here.
