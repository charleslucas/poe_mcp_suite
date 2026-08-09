---
name: spectre-analysis
description: Choose, measure, and correctly model spectres for a Path of Exile minion build — which spectre to raise or buy, what a spectre actually grants, and why PoB shows no change when you add one. Use for "which spectres should I use", "is spectre X worth buying", "what does this spectre grant", "my spectres do nothing in PoB", or any minion-build measurement that looks lower than the in-game character sheet.
---

This task uses the **Spectre Analysis** playbook. The playbooks in `playbooks/` are the single
source of truth — read them rather than working from memory.

1. Read `playbooks/README.md` first — the shared meta-framework (cursory-vs-detailed gate, pre-flight,
   trust hierarchy, narration norms).
2. Then read `playbooks/spectre-analysis.md` and follow it.

The one thing that invalidates naive work here:

- **PoB applies the buffs of only ONE spectre** — the selected minion of a Raise Spectre instance
  (`CalcPerform.lua:2169`). Adding a spectre and seeing **zero change** is the *expected* result for a
  non-selected spectre, and is indistinguishable from a broken mod. Measure by listing the spectre
  **first**, or build the modeling group (playbook Step 3) to model several at once.
- Imports never set spectres; the PoE API doesn't report them. A modeling group is destroyed by every
  import — re-add it as part of the post-import checklist.
- `grants:` in the text lake is lossy: it drops conditions (`MonsterTag`) and omits auras, which live in
  `skills:`. Read the raw `Data/Spectres.lua` entry before believing it.
- Corpse spectres are traded by `base_type`, not `name`, and are absent from poe.ninja.
