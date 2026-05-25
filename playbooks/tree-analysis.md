# Playbook: Passive Tree Analysis

For sessions where the user wants to evaluate, optimise, or reallocate nodes on their passive tree — whether that's finding waste, reaching a specific notable, or freeing points for a targeted upgrade. Covers both "what should I change" (open-ended) and "I want X, what do I remove" (surgical).

**Triggers:** "look at my passive tree", "what nodes should I change", "I want to get [notable]", "which nodes are weakest", "can I free up some points", or any session where the passive tree is the primary focus.

---

## Step 0 — Frame the work for the user

*"Using the Tree Analysis playbook — triage first to establish the goal, then I'll pull the tree, classify nodes, and run connectivity analysis to find safe reallocation candidates."*

This is always a **detailed analysis** — apply the cursory/detailed gate from [`README.md`](README.md) section 1 before loading data.

---

## Step 1 — Triage

Ask before loading anything. Many of these answers may already be in the journal.

**Q1 — Intent** (gates everything downstream):
- **DPS increase** → also load [`dps-analysis.md`](dps-analysis.md) and prioritise damage multipliers, accuracy, crit chance, and skill-specific notables. Use PoB stat simulation to validate candidates.
- **Survivability / defence** → focus on life pool, resistance capping, block chance, armour/ES, recovery sources. Cross-reference [`defense-audit.md`](defense-audit.md) once it exists.
- **Reach a specific notable** → surgical: identify the path cost, find N points to free, check connectivity for each candidate.
- **Well-rounded / general tune-up** → evaluate all allocated notables for value-per-point; flag both weak defence and weak offence nodes.
- **Mechanic-specific** → e.g., "I want more rage", "I want leech mastery". Pull the relevant cluster from the tree and map the path cost from the current frontier.

**Q2 — Points budget:**
- How many free points exist now?
- How many does the target require? (Use `find_path_to_node` to get the exact count before assuming.)

**Q3 — Constraints:**
- Any notables that must stay (ascendancy-enabling, aura-reservation-critical, keystone the build depends on)?
- Any jewel sockets that must stay connected?

---

## Step 2 — Data loads

### Always load
| Source | Tool | Notes |
|--------|------|-------|
| Pre-flight | See [`README.md`](README.md) section 2 | Context check, league reference, character snapshot |
| Current tree + node IDs | `mcp__pob__lua_get_tree` with `include_node_ids: true` | Need full ID list for Python classification |
| Node reference data | `reference_data/skilltree/data.json` (Python) | Names, stats, adjacency (`in`/`out` edges), type flags |

### Add if intent = DPS increase
- `mcp__pob__lua_get_stats` to establish the DPS baseline before any changes
- Load [`dps-analysis.md`](dps-analysis.md) alongside this playbook

### Add if searching for a specific notable
- `mcp__pob__search_tree_nodes` with the keyword (see pitfalls for correct usage)
- `mcp__pob__find_path_to_node` from the nearest allocated node to the target — **always verify path cost before estimating points needed**

### Add if intent involves simulation
- `mcp__pob__lua_get_stats` before and after any proposed change for a stat delta

---

## Step 3 — Analysis pattern

### 3a — Classify all allocated nodes

Run a Python script against `reference_data/skilltree/data.json` using the node IDs from `lua_get_tree`:

```python
for nid in allocated_ids:
    node = nodes[str(nid)]
    type = ('keystone' if node.get('isKeystone') else
            'notable' if node.get('isNotable') else
            'ascendancy' if node.get('ascendancyName') else
            'mastery' if node.get('isMastery') else
            'jewel' if 'Jewel Socket' in node.get('name','') else
            'normal')
```

This gives you the population of each type and the full list of normal travel nodes with their stats. Do not rely on `search_tree_nodes` alone for this — it has a `limit` cap and won't return all nodes.

### 3b — Find removable chains

For each normal node, compute its allocated neighbours (combine `in` + `out` edges, filter to allocated set). A node is **removable** only if doing so doesn't disconnect any other allocated node from the class start.

Safe removal patterns:
1. **Pendant leaf**: a notable or normal node whose only allocated neighbour is a single travel node. Remove both.
2. **Pendant chain**: a sequence N₁ → N₂ → … → Nₙ where N₁ has only one allocated neighbour (the junction back to the main tree). Remove the whole chain from Nₙ inward.
3. **Loop shortcut**: a travel node with two allocated neighbours that are themselves already connected by another path. Rare — verify before assuming.

**Jewel socket check (mandatory):** Before finalising any removal, check that every Large/Medium/Basic Jewel Socket in the allocated set retains at least one non-removed allocated neighbour. If a jewel socket's only allocated neighbour is the node being removed, the jewel socket becomes disconnected and the jewel goes inactive. The 2026-05-25 session found this ruled out two otherwise-attractive pairs (armour smalls connecting only to jewel sockets).

### 3c — Evaluate candidate value

Rank candidates by value-per-point *relative to this build's profile*:
- A "+8% Armour" node is nearly worthless for a leech-block build, significant for an armour stacker.
- A "Gain 1 Rage on Melee Hit" node is worthless if the build doesn't use Berserk or Rage-scaling skills.
- A "+5% to all Elemental Resistances" node on an already-overcapped build contributes 0 effective defence.
- Check the character's `meta.json` and journal for known constraints before declaring a node waste.

Always prefer removing the **same number of points from the weakest cluster** over removing scattered individual smalls. A chain removal (notable + 1–2 path nodes) is cleaner and easier to reverse than random individual smalls spread across the tree.

### 3d — Verify addition paths

For each target node to add, use `mcp__pob__find_path_to_node` from the nearest currently allocated node. Do **not** assume the path cost from the JSON adjacency alone — PoB's connectivity model may route differently. Common source of error: counting the adjacent mastery node as a valid stepping stone (see Pitfalls).

---

## Step 4 — Output shape

For surgical reallocations (reach a specific notable), a chat response is sufficient:
- Table: N nodes to remove | stats lost | why it's safe
- Table: M nodes to add | stats gained | entry point
- Net stat delta (DPS %, life Δ, armour Δ, resistance Δ)

For open-ended tune-ups, append to `character_data/{Account}/{Character}/journal.md` under `## YYYY-MM-DD — Passive Tree Analysis`:
- Methodology note (intent, constraints)
- Removed nodes table
- Added nodes table
- Stat deltas before/after

Update `meta.json`:
- `last_analyzed`, `current_stats` (armour, DPS, resistances), `masteries` (if a mastery node was removed/added)

---

## Step 5 — Pitfalls

### Mastery nodes are terminal
In the passive tree graph, mastery nodes (the large central node of a cluster) appear as neighbours to regular notables and smalls in the JSON. **You can path TO a mastery node, but you cannot path THROUGH it.** A node that is adjacent to a mastery in the JSON cannot be reached via the mastery — you must find the non-mastery path.

Example from 2026-05-25: Divine Judgement [13164] appeared to be "1 node away" because it was adjacent to Elemental Mastery [44298] (already allocated). In reality, reaching Divine Judgement required a 3-node path through non-mastery nodes: `29061 → 55993 → 41251/8198 → 13164`.

**Check:** before declaring "N nodes away", filter out mastery nodes from the path. Always use `find_path_to_node` for the final count — it respects PoB's actual connectivity rules.

### Jewel sockets strand on removal
Any Large, Medium, or Basic Jewel Socket node that has only one allocated neighbour will become disconnected (and its jewel inactive) if that neighbour is removed. This silently nerfs the build without any visible error. Always check `alloc_nbrs(jewel_socket_id)` before finalising a removal that touches nodes near jewel sockets.

### `search_tree_nodes` usage
- **Omit `node_type` to search all types.** Passing `node_type: "any"` was a bug (filtered everything) — fixed 2026-05-25 in both Lua and TypeScript layers. The fix is in: `PathOfBuilding/src/API/BuildOps.lua` and `pob-mcp/src/server/toolRouter.ts`.
- **Valid `node_type` values:** `keystone`, `notable`, `jewel`, `mastery`, `ascendancy`, `normal` (small travel nodes). Omit for all types.
- **`limit` cap:** the tool returns at most 30 results. For exhaustive classification of all allocated nodes, use a Python script against `data.json` directly instead.

### `lua_set_tree` is unsafe for cluster jewel builds
`lua_set_tree` silently drops cluster jewel internal passives and wipes all mastery effect selections. For any character with Large Cluster Jewels, do tree changes in the PoB GUI or in-game, then re-sync with `lua_import_character`. See 2026-05-21 journal entry for the full list of known `lua_set_tree` bugs.

### Point budget accounting
`lua_get_tree` returns the count of allocated nodes, not available passive points. Available points = (level − 1) + quest rewards (typically 24 at endgame) + bandit bonus − allocated nodes. A level 96 character with 24 quest rewards and Kill All bandit has 95 + 24 + 1 = 120 available points. If `lua_get_tree` shows 124 allocated nodes, there are no free points — the "extra" nodes came from Passive Skill Point items or similar.

### Connectivity is not obvious
Even with the adjacency data, it's not always obvious which nodes are safely removable. The "find all leaf nodes" approach often returns zero results at endgame because nodes form dense loops around the Duelist/Witch starting areas. Use the pendant-chain analysis (Step 3b) instead of trying to find pure graph leaves.

### `reference_data/skilltree/data.json` can be stale
GGG's published skilltree export lags real game state — sometimes by months. A node's stat line can change in a patch without the export being re-tagged. Example from 2026-05-25: node 11730 "Endurance" shows only `+1 to Maximum Endurance Charges` in the 3.28.0 export, but the in-game tooltip also has `0.4% of Attack Damage Leeched as Life`. Recommending the node for removal based on the JSON alone undervalued its real defensive contribution.

**Before recommending a notable for removal, cross-verify its stats against:**
1. The user's in-game tooltip (ask them to paste it — fastest and most authoritative)
2. PoB's bundled tree data via `mcp__pob__search_tree_nodes` or `mcp__poemcp__get_passive_detail`
3. The wiki (`fetch_wiki_page` on the node's individual page)

If you find a discrepancy, log a patch entry in `reference_data/skilltree/data_patches.json` (see `reference_data/SKILLTREE_PATCHES.md` for format). Future sessions inherit the corrected data automatically. This is especially important for notable removals, where missing a stat line can cost real defensive value (life leech, max res, charge generation) without showing up in your analysis.
