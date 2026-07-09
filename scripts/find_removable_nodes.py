#!/usr/bin/env python3
"""Find safely-removable passive tree nodes via connectivity (articulation-point) analysis.

Used by playbooks/tree-analysis.md Step 3b. Two modes:

  1. LIST mode (default): report every allocated node that can be removed ALONE without
     disconnecting any other allocated node from the class start. This correctly includes
     loop nodes (degree-2 nodes on a cycle), which naive pendant-leaf peeling misses.

  2. SET mode (--remove id,id,...): validate a proposed removal SET as a whole.
     ⚠ Individually-removable nodes are NOT necessarily jointly removable — a loop
     segment tolerates one cut but not two (2026-07-09: two wheel travel nodes were each
     safe alone; removing both stranded the notable between them).

  3. NEAR mode (--near N [--grep text] [--travel]): list unallocated nodes reachable
     within N allocations of the current tree, grouped by real path distance (respects
     the mastery-terminal rule). Offline complement to PoB's get_node_power heat map:
     exhaustive (no top-20 cap), filterable by stat text, no PoB required. Value
     judgement still belongs to PoB simulation (playbook 3e).

  4. ADD mode (--add id,id,...): analyze a proposed allocation. Reports whether the
     addition CREATES loops (cycle count before/after) and — the useful part — which
     previously-locked nodes become individually removable because the new loop provides
     an alternate path. Loops have zero mechanical value in PoE, so a created loop means
     a redundant connection: the refund candidates on the ring's other side reduce the
     NET cost of reaching the target. Validate any actual refund set with --remove.

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
    p.add_argument("--near", type=int, help="list unallocated nodes within N allocations of the tree")
    p.add_argument("--grep", help="near mode: only nodes whose name/stats contain this text (case-insensitive)")
    p.add_argument("--travel", action="store_true", help="near mode: include travel nodes (default: notables/jewels only)")
    p.add_argument("--add", help="comma-separated node IDs: analyze a proposed allocation (loop creation + refund candidates)")
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

    def traversable(nid):
        n = nodes.get(nid)
        return (n is not None and not n.get("isMastery") and n.get("group") is not None
                and n.get("classStartIndex") is None and not n.get("isAscendancyStart"))

    def removable_alone(graph, roots):
        """IDs whose solo removal leaves every other node reachable from roots."""
        def reach(live):
            seen = set(roots & live)
            stack = list(seen)
            while stack:
                cur = stack.pop()
                for nb in nbrs(cur) & live:
                    if nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
            return seen
        out = set()
        for nid in graph:
            if nid in roots:
                continue
            live = graph - {nid}
            if reach(live) == live:
                out.add(nid)
        return out

    if a.near:
        # BFS outward from the allocated frontier through unallocated, traversable nodes.
        # dist = number of allocations needed to have the node (its whole path included).
        dist = {}
        cur = set()
        for u in main:
            for v in nbrs(u):
                if v not in main and v not in dist and traversable(v):
                    dist[v] = 1
                    cur.add(v)
        depth = 1
        while cur and depth < a.near:
            nxt = set()
            for u in cur:
                for v in nbrs(u):
                    if v not in main and v not in dist and traversable(v):
                        dist[v] = depth + 1
                        nxt.add(v)
            cur = nxt
            depth += 1
        rows = []
        for nid, dd in dist.items():
            n = nodes[nid]
            is_notable = n.get("isNotable")
            is_jewel = "Jewel Socket" in (n.get("name") or "")
            if not (is_notable or is_jewel or a.travel):
                continue
            blob = ((n.get("name") or "") + " " + " ".join(n.get("stats", []))).lower()
            if a.grep and a.grep.lower() not in blob:
                continue
            rows.append((dd, 0 if is_notable else (1 if is_jewel else 2), nid))
        rows.sort()
        print(f"=== UNALLOCATED NODES WITHIN {a.near} ALLOCATION(S)"
              + (f" matching '{a.grep}'" if a.grep else "")
              + (" (incl. travel)" if a.travel else " (notables/jewels; --travel for all)") + " ===")
        for dd, _, nid in rows:
            print(f"[cost {dd}] {describe(nid)}")
        print(f"\n{len(rows)} node(s). Cost = allocations to reach (path included). "
              "Exact path via find_path_to_node; value via PoB sim (playbook 3e).")
        sys.exit(0)

    if a.add:
        added = {x for x in parse_ids(a.add) if x not in main}
        bad = [x for x in added if not traversable(x) and not (nodes.get(x) or {}).get("isAscendancyStart")]
        if bad:
            print(f"⚠ skipped (mastery/class-start/unknown): {sorted(bad)}")
            added -= set(bad)
        union = main | added
        roots = starts | {nid for nid in added if nodes[nid].get("isAscendancyStart")}

        def reach_from(roots_, live):
            seen = set(roots_ & live)
            stack = list(seen)
            while stack:
                cur_ = stack.pop()
                for nb in nbrs(cur_) & live:
                    if nb not in seen:
                        seen.add(nb)
                        stack.append(nb)
            return seen

        stranded = added - reach_from(roots, union)
        if stranded:
            print(f"❌ addition not connected to the tree: {sorted(stranded)} — "
                  "include the connecting path nodes in --add")
            sys.exit(1)

        def cycle_count(graph):
            E = sum(len(nbrs(u) & graph) for u in graph) // 2
            seen, comps = set(), 0
            for s in graph:
                if s in seen:
                    continue
                comps += 1
                stack = [s]
                seen.add(s)
                while stack:
                    cur_ = stack.pop()
                    for nb in nbrs(cur_) & graph:
                        if nb not in seen:
                            seen.add(nb)
                            stack.append(nb)
            return E - len(graph) + comps

        dc = cycle_count(union) - cycle_count(main)
        print(f"=== ADDITION ANALYSIS: +{len(added)} node(s) {sorted(added)} ===")
        for nid in sorted(added, key=int):
            print(f"  {describe(nid)}")
        if dc <= 0:
            print("\nNo loop created — a plain extension (dead-end chain). "
                  "Removability of existing nodes is unchanged.")
        else:
            print(f"\n🔁 CREATES {dc} loop(s) — this connection is redundant (loops have no "
                  "mechanical value), which usually means REFUND POTENTIAL on the ring:")
            before = removable_alone(main, starts)
            after = removable_alone(union, roots)
            newly = sorted((after - before) - added, key=int)
            if newly:
                print("  Previously-locked nodes now individually removable (refund candidates):")
                for nid in newly:
                    print(f"    {describe(nid)}")
                print(f"  → Net cost of this addition could be as low as "
                      f"{len(added)} - {len(newly)} refunded = {len(added) - len(newly)} point(s)."
                      f"\n  ⚠ Refunds are ALTERNATIVES on the ring, not all simultaneously safe —"
                      f"\n     validate the exact refund set with --remove id,id,...")
            else:
                print("  ...but no allocated node becomes individually removable "
                      "(the ring's other side is load-bearing or already removable).")
        sys.exit(0)

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
