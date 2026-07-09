#!/usr/bin/env python3
"""Find safely-removable passive tree nodes via connectivity (articulation-point) analysis.

Used by playbooks/tree-analysis.md Step 3b. Two modes:

  1. LIST mode (default): report every allocated node that can be removed ALONE without
     disconnecting any other allocated node from the class start. This correctly includes
     loop nodes (degree-2 nodes on a cycle), which naive pendant-leaf peeling misses.

  2. SET mode (--remove id,id,...): validate a proposed removal SET as a whole.
     ⚠ Individually-removable nodes are NOT necessarily jointly removable — a loop
     tolerates one cut but not two (2026-07-09: removing Fearsome Force + Arcanist's
     Dominion together stranded 22 nodes even though each sat on a loop).

Guards beyond raw connectivity:
  - Mastery clusters: a mastery stays allocatable only while >=1 notable from its own
    cluster group is allocated. Removals that strip a cluster's last allocated notable
    are flagged (the mastery effect would silently drop).
  - Masteries are never traversable paths (mastery-terminal rule).
  - Ascendancy nodes ARE analyzed (several ascendancy trees contain loops — Deadeye,
    Raider, Saboteur, Chieftain, Reliquarian, King in the Mists), rooted at the
    allocated ascendancy-start node. Alternate/Phrecian ascendancy nodes absent from
    data.json are skipped gracefully (live PoB is the arbiter for those).

Usage:
  python scripts/find_removable_nodes.py --alloc 1203,2913,...        # list mode
  python scripts/find_removable_nodes.py --alloc-file ids.txt --remove 35685,11420
  Optional: --data path/to/data.json (default: reference_data/skilltree/data.json)
"""
import argparse
import json
import sys
from pathlib import Path

# Windows consoles default to cp1252; keep the ⚠/✅/❌ markers working when piped.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def load_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--alloc", help="comma-separated allocated node IDs")
    p.add_argument("--alloc-file", help="file containing allocated node IDs (any separators)")
    p.add_argument("--remove", help="comma-separated node IDs: validate this removal set instead of listing")
    p.add_argument("--data", default="reference_data/skilltree/data.json", help="path to GGG tree data.json")
    a = p.parse_args()
    if not a.alloc and not a.alloc_file:
        p.error("provide --alloc or --alloc-file")
    return a


def parse_ids(text):
    import re
    return [t for t in re.split(r"[^0-9]+", text) if t]


def main():
    a = load_args()
    data = json.loads(Path(a.data).read_text())
    nodes = data["nodes"]
    raw_alloc = parse_ids(a.alloc or Path(a.alloc_file).read_text())

    # Partition: traversable (main tree + ascendancy) vs skipped (mastery/unknown).
    # Ascendancy nodes present in data.json are analyzed like any other — their trees can
    # contain loops. Alt-ascendancy nodes (absent from data.json) are skipped.
    main, skipped, masteries = set(), [], []
    for nid in raw_alloc:
        n = nodes.get(nid)
        if n is None:
            skipped.append((nid, "not in data.json (alt-ascendancy?)"))
        elif n.get("isMastery"):
            masteries.append(nid)  # allocated masteries: checked for cluster-notable rule, not pathing
            skipped.append((nid, f"mastery ({n.get('name')})"))
        else:
            main.add(nid)

    def nbrs(nid):
        n = nodes.get(nid, {})
        return {str(x) for x in (n.get("in", []) + n.get("out", []))}

    # Connectivity roots: the class start (adjacent to the synthetic root) PLUS each
    # allocated ascendancy start — the ascendancy cluster is a separate component whose
    # own start anchors it (the class edge is implicit, not in the edge data).
    starts = {str(x) for x in nodes.get("root", {}).get("out", [])} & main
    starts |= {nid for nid in main if nodes[nid].get("isAscendancyStart")}
    if not starts:
        sys.exit("ERROR: no allocated class-start node found — check the alloc list")

    def reachable(live):
        seen = set(starts & live)
        stack = list(seen)
        while stack:
            cur = stack.pop()
            for nb in nbrs(cur) & live:
                if nb not in seen:
                    seen.add(nb)
                    stack.append(nb)
        return seen

    base = reachable(main)
    disconnected = main - base
    if disconnected:
        print(f"⚠ {len(disconnected)} allocated node(s) already unreachable from start "
              f"(data gap or odd tree): {sorted(disconnected)}")

    def mastery_warnings(removal_set):
        """Masteries whose cluster would lose its last allocated notable."""
        warn = []
        for mid in masteries:
            grp = nodes[mid].get("group")
            live_notables = [x for x in main - removal_set
                             if nodes[x].get("isNotable") and nodes[x].get("group") == grp]
            if not live_notables:
                warn.append(f"mastery {mid} ({nodes[mid].get('name')}) loses its last cluster notable")
        return warn

    def describe(nid):
        n = nodes[nid]
        kind = ("notable" if n.get("isNotable")
                else "jewel" if "Jewel Socket" in (n.get("name") or "")
                else "travel")
        if n.get("ascendancyName"):
            kind = f"asc-{kind}"
        return f"[{nid}] {n.get('name')} <{kind}>: " + "; ".join(n.get("stats", []))

    if a.remove:
        removal = set(parse_ids(a.remove))
        unknown = removal - main
        if unknown:
            print(f"⚠ not in the allocated main-tree set (ignored): {sorted(unknown)}")
            removal &= main
        live = main - removal
        stranded = (reachable(live) ^ live) if live else set()
        mw = mastery_warnings(removal)
        print(f"=== SET VALIDATION: remove {sorted(removal)} ===")
        if stranded:
            print(f"❌ UNSAFE — strands {len(stranded)} node(s): {sorted(stranded)}")
        elif mw:
            print("⚠ CONNECTED but mastery warning(s):")
            for w in mw:
                print(f"   - {w}")
        else:
            print(f"✅ SAFE — remaining {len(live)} nodes stay connected; no mastery stranding")
        sys.exit(0)

    # LIST mode: single-node removability via remove-and-BFS (O(N^2), fine at ~120 nodes)
    print(f"=== SAFELY REMOVABLE ALONE ({len(main)} main-tree nodes, {len(starts)} start) ===")
    removable = []
    for nid in sorted(main, key=int):
        if nid in starts:
            continue
        live = main - {nid}
        if reachable(live) == live:
            mw = mastery_warnings({nid})
            removable.append((nid, mw))
    for nid, mw in removable:
        loop = " (in a loop)" if len(nbrs(nid) & main) >= 2 else ""
        print(describe(nid) + loop)
        for w in mw:
            print(f"      ⚠ {w}")
    print(f"\n{len(removable)} of {len(main)} nodes removable alone.")
    print("⚠ Individually-removable ≠ jointly-removable: validate any multi-node removal "
          "with --remove id,id,... before recommending it.")


if __name__ == "__main__":
    main()
