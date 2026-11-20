---
name: budget-loadout
description: Turn a finished Path of Building target build into a ready-to-buy loadout under a stated budget - prices the uniques, closes the resist/attribute caps with rares, verifies the trade links, and produces one page listing every purchase and step.
when_to_use: Use when the user points at an existing target build and gives constraints - "make me a working version on N div", "goal loadout is X, this is what I own", "build it under budget", "budget loadout for this build". Also when a previous budget build needs re-pricing or re-capping. Skip designing from a concept (build-design) and slot-by-slot upgrades of a working character (dps-analysis, gear-shopping).
---

This task uses the **Budget Loadout** playbook - read `playbooks/budget-loadout.md` and follow it. Read `playbooks/README.md` first for the shared meta-framework.

The playbook owns the procedure: reading the target, measuring what matters, assembling a complete `BUDGET` loadout, spending inside the budget, closing the caps, producing verified links, and generating the final page.

Load `playbooks/assets/budget-loadout/loadout-xml.md` when a loadout family or a jewel socket has to be created, and `playbooks/assets/budget-loadout/make-page.cjs` for the page.

Progress is tracked by the playbook's four signals: **ceiling**, **caps**, **green**, **receipt**.
