# Skilltree Data Patches

GGG publishes the passive skill tree as a JSON export at https://github.com/grindinggear/skilltree-export. That export is the most authoritative public source, but it lags real game state — sometimes by months. A node's stat line can change in a patch without the export being re-tagged.

This file documents a small overlay layer that lets us keep `data.json` untouched while correcting individual nodes as we verify them against in-game tooltips or PoB's bundled tree data.

## Why not edit `data.json` directly?

- `data.json` is a clone of GGG's repo. Editing it conflicts with `git pull` whenever upstream updates.
- We want an audit trail: which nodes have we hand-verified, when, and against what source.
- If GGG eventually fixes a node, we want to retire our patch without re-deriving what we changed.

## File: `data_patches.json`

Sits next to `data.json`. Optional — if missing, no patches are applied. Format:

```json
{
  "11730": {
    "stats_add": ["0.4% of Attack Damage Leeched as Life"],
    "verified_from": "in-game tooltip",
    "verified_date": "2026-05-25",
    "verified_by": "Memophage#4428",
    "note": "GGG 3.28.0 export missing this stat; PoB also missing it"
  },
  "9695": {
    "stats_replace": [
      "+150 to Armour",
      "30% increased Armour",
      "+1% to all maximum Elemental Resistances"
    ],
    "verified_from": "in-game tooltip",
    "verified_date": "2026-05-25",
    "verified_by": "Memophage#4428"
  }
}
```

### Patch operations

| Key | Effect |
|-----|--------|
| `stats_add` | Appends entries to the node's existing `stats` array. Use when GGG has SOME of the stats but is missing additions. |
| `stats_replace` | Replaces the node's `stats` array entirely. Use when stats have been re-worded or completely revised. |
| `name_replace` | Replaces the node's `name` string. Rare. |
| `flags_set` | Sets `isNotable` / `isKeystone` / `isJewelSocket` / `isMastery` to provided values. Rare. |

A single node can have multiple operations; they're applied in the order listed in the table.

### Required metadata on every patch

- `verified_from`: one of `"in-game tooltip"`, `"PoB tree data"`, `"PoB lua_get_passive_detail"`, `"wiki"`, `"reddit/forum"`.
- `verified_date`: ISO date (`YYYY-MM-DD`).
- `verified_by`: account handle of the player who confirmed (`AccountName#1234`) or `"Claude"` if Claude pulled it from PoB programmatically.
- `note` (optional): why the patch was needed.

The metadata is required because patches go stale too — a node corrected today might be re-balanced next patch. The `verified_date` lets us flag patches older than N months for re-verification.

## When to add a patch

Add an entry when a session encounters a tree-data discrepancy that affects a recommendation:

1. **Stat mismatch**: in-game tooltip shows stats the JSON doesn't have, or vice versa.
2. **New node**: a node ID exists in PoB's data but not in GGG's export.
3. **Renamed node**: the stats are right but the name in JSON is out of date.

Do NOT patch:
- Visual / positioning differences (sprites, x/y, orbit) — those don't affect analysis.
- Differences attributable to Timeless Jewels or other in-game transformations — those aren't bugs in the base data.

## How patches get applied

Any script or tool that consumes tree data should merge `data.json` + `data_patches.json` at load time. The MCP server may also expose a dedicated tool that returns the merged view of a single node — see `pob-mcp/TODO.md` ("Skilltree Patches MCP Tool") for the spec.

## Upstream contribution

Patches we verify with high confidence are good candidates to submit upstream as PRs / issues to https://github.com/grindinggear/skilltree-export. The metadata on each patch (source + date) is exactly the evidence GGG would want. When a patch is accepted upstream, retire it from `data_patches.json` after the next `git pull`.
