---
name: tree-analysis
description: Detailed passive-tree audit, optimization, or reallocation for a Path of Exile build — finding wasted nodes, reaching a target notable, or freeing points for an upgrade. Runs the systematic methodology (node classification, connectivity/chain checks, jewel-socket safety, mastery topology).
when_to_use: Use for substantive passive-tree work — "look at my passive tree", "what nodes should I change", "I want to get [notable]", "which nodes are weakest", "can I free up some points", "what's the best passive point to take", "which node should I pick", "I just levelled up what should I take". Skip for a single-node lookup (use get_tree_node directly). IMPORTANT: when using get_passive_upgrades, always verify path cost with find_path_to_node before recommending — the tool ranks by stat impact only and ignores travel node cost entirely.
---

This task uses the **Passive Tree Analysis** playbook. The playbooks in `playbooks/` are the single source of truth — read them rather than working from memory, so you always get the current version.

1. Read `playbooks/README.md` first — the shared meta-framework (cursory-vs-detailed gate, context/pre-flight protocol, league reference, trust hierarchy, narration norms).
2. Then read `playbooks/tree-analysis.md` and follow it for this task.

Do not summarize or duplicate the playbook content here.
