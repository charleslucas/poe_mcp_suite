#!/usr/bin/env python3
"""Enumerate the "closed shapes" (loops) of a passive-tree allocation.

The loops a human sees when visually inspecting the tree are, formally, the FACES of the
tree's planar drawing. This tool reconstructs each node's drawn position from the tree
export (group center + orbit radius + orbit index), sorts each node's edges by angle, and
runs standard planar face tracing on the allocated subgraph. Output: each closed shape as
an array of its member nodes — triangles, mastery-cluster rings, big travel loops.

Why this matters for removability (companion to find_removable_nodes.py):
  - Within a shape, the actionable unit is the SEGMENT — the chain of degree-2 nodes
    between junctions (nodes with 3+ allocated connections).
  - You can generally cut AT MOST ONE node per segment: the loop provides the alternate
    path around a single cut, but two cuts in the same segment always strand the nodes
    between them (2026-07-09: Fearsome Force + Arcanist's Dominion, ~20 nodes silently
    dropped by PoB).
  - This is a reasoning aid, not a guarantee: cuts in DIFFERENT segments usually compose
    but can still interact through the wider graph (theta shapes). Always validate the
    final removal set: find_removable_nodes.py --remove id,id,...

Usage:
  python scripts/find_tree_shapes.py --alloc 1203,2913,...
  python scripts/find_tree_shapes.py --alloc-file ids.txt [--data path/to/data.json]

Caveat: positions and edges come from GGG's *standard* data.json; nodes absent from it
(alternate/Phrecian ascendancies) are skipped — live PoB is the arbiter there. Crossing
long-connector edges (rare) can distort face boundaries.
"""
import argparse
import json
import math
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


def parse_ids(text):
    import re
    return [t for t in re.split(r"[^0-9]+", text) if t]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--alloc", help="comma-separated allocated node IDs")
    p.add_argument("--alloc-file", help="file containing allocated node IDs (any separators)")
    p.add_argument("--data", default="reference_data/skilltree/data.json")
    a = p.parse_args()
    if not a.alloc and not a.alloc_file:
        p.error("provide --alloc or --alloc-file")

    data = json.loads(Path(a.data).read_text())
    nodes, groups = data["nodes"], data["groups"]
    spo = data["constants"]["skillsPerOrbit"]
    radii = data["constants"]["orbitRadii"]

    # --- Allocated subgraph (same filter as find_removable_nodes.py): main tree AND
    # ascendancy nodes — several ascendancy trees contain loops (Deadeye, Raider,
    # Saboteur, Chieftain, Reliquarian, King in the Mists). Masteries and nodes absent
    # from data.json (alt-ascendancies) are skipped.
    alloc = parse_ids(a.alloc or Path(a.alloc_file).read_text())
    main_set = set()
    for nid in alloc:
        n = nodes.get(nid)
        if n and not n.get("isMastery") and n.get("group") is not None:
            main_set.add(nid)

    # --- Drawn position of each node: group center + orbit radius at orbit-index angle ---
    def pos(nid):
        n = nodes[nid]
        g = groups[str(n["group"])]
        orbit, idx = n.get("orbit", 0), n.get("orbitIndex", 0)
        theta = 2 * math.pi * idx / spo[orbit]  # 0 at 12 o'clock, clockwise
        r = radii[orbit]
        return (g["x"] + r * math.sin(theta), g["y"] - r * math.cos(theta))

    xy = {nid: pos(nid) for nid in main_set}

    def nbrs(nid):
        n = nodes[nid]
        return sorted({str(x) for x in (n.get("in", []) + n.get("out", []))} & main_set,
                      key=lambda m: math.atan2(xy[m][1] - xy[nid][1], xy[m][0] - xy[nid][0]))

    adj = {nid: nbrs(nid) for nid in main_set}

    # --- Planar face tracing over half-edges ---
    # After arriving along u->v, the next boundary edge leaves v toward the neighbor
    # immediately BEFORE u in v's angular order (consistent orientation traces each face once).
    def next_half_edge(u, v):
        ring = adj[v]
        return v, ring[(ring.index(u) - 1) % len(ring)]

    seen, faces = set(), []
    for u in main_set:
        for v in adj[u]:
            if (u, v) in seen:
                continue
            face, cur = [], (u, v)
            while cur not in seen:
                seen.add(cur)
                face.append(cur[0])
                cur = next_half_edge(*cur)
            faces.append(face)

    # --- Keep simple closed shapes (all nodes distinct, length >= 3); dedupe by node set.
    # Bridge/dead-end walks repeat nodes and are filtered; a pure isolated ring yields the
    # same node set twice (inner + outer boundary) and dedupes to one shape.
    shapes, seen_sets = [], set()
    for f in faces:
        if len(f) >= 3 and len(set(f)) == len(f):
            key = frozenset(f)
            if key not in seen_sets:
                seen_sets.add(key)
                shapes.append(f)
    # The unbounded outer boundary of the whole allocation can also appear as one huge
    # simple cycle; it is a real ring in the graph, so keep it — size sorting surfaces
    # the small local shapes first either way.
    shapes.sort(key=len)

    def label(nid):
        n = nodes[nid]
        kind = ("notable" if n.get("isNotable")
                else "jewel" if "Jewel Socket" in (n.get("name") or "")
                else "travel")
        if n.get("ascendancyName"):
            kind = f"asc-{kind}"
        return f"[{nid}] {n.get('name')} <{kind}>"

    degree = {nid: len(adj[nid]) for nid in main_set}

    print(f"=== CLOSED SHAPES in the allocated tree ({len(main_set)} main-tree nodes) ===\n")
    if not shapes:
        print("No closed shapes — the allocation is a pure tree (every node is chain/leaf).")
    for i, f in enumerate(shapes, 1):
        junctions = [nid for nid in f if degree[nid] >= 3]
        print(f"--- Shape {i}: {len(f)} nodes, {len(junctions)} junction(s) ---")
        for nid in f:
            j = "  «junction»" if degree[nid] >= 3 else ""
            print(f"  {label(nid)}{j}")
        # Segments: maximal runs of non-junction nodes between junctions (circular)
        if junctions:
            segs, run = [], []
            jset = set(junctions)
            start = next(k for k, nid in enumerate(f) if nid in jset)
            order = f[start:] + f[:start]
            for nid in order:
                if nid in jset:
                    if run:
                        segs.append(run)
                        run = []
                else:
                    run.append(nid)
            if run:
                segs.append(run)
            cuttable = [s for s in segs if s]
            if cuttable:
                print("  Segments (≤1 cut per segment, then validate the set):")
                for s in cuttable:
                    print("    - " + " → ".join(label(nid) for nid in s))
            else:
                print("  All shape nodes are junctions — no free cuts on this shape.")
        else:
            print("  Isolated ring (no junctions): at most ONE node can be cut from it.")
        print()
    print("Reminder: shapes are a reasoning aid. Validate any removal set with:\n"
          "  python scripts/find_removable_nodes.py --alloc ... --remove id,id,...")


if __name__ == "__main__":
    main()
