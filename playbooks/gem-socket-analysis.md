# Playbook: Skill-Gem & Socket Analysis

Analyze a character's socket colours, links, gem placement, off-colours, and empty
sockets — the layer that `build-optimization-sim` and `dps-analysis` assume away.
This playbook **owns the socket dimension**: which gem sits in which coloured
socket, whether anything is off-colour, what a given empty socket can actually take,
and whether the arrangement is sound. It **hands the "is a change worth it?" question
to [`build-optimization-sim.md`](build-optimization-sim.md)** (live PoB DPS sim) and
socket-aware purchases to [`gear-shopping.md`](gear-shopping.md).

Read [`README.md`](README.md) first (cursory/detailed gate, pre-flight, context
management, narration norms, trust hierarchy).

---

## When to use this playbook

- "Give me a full skill-gem / socket analysis."
- "I have an empty socket — what's the best gem to put in it?"
- "Are there gem-arrangement improvements that would improve my build?"
- "Are any of my gems off-colour?" / "How hard is this item to colour?"
- Before a **gear purchase**, to preserve (or cheaply match) an item's socket setup.
- **From a build link:** "What socket colours/links do I need to copy this build?"
  (a pobb.in / poedb.tw / pastebin PoB link) — see the *shared-build* section below.

Detailed scope — run pre-flight and pause for approval before pulling data.

---

## Why a dedicated playbook

The socket picture lives across several sources, and the traps are in combining them
correctly. What matters is a group's **colour *counts* + link size** — never a
per-gem map: within a link group, which gem sits in which same-colour socket is
**interchangeable** (a linked pair of two blue sockets is order-independent). The
sources:

- **Item socket colours** — stored on the item (the `Sockets:` line). PoB keeps
  these; it only abstracts *which gem occupies which position* (irrelevant, per
  above). Read them via `get_socket_colors` (own loaded build) or `item_sockets`
  from `parse_pob_skill_groups` (a shared build link).
- **Which gems are grouped / linked** — `get_skill_setup` (own build) or
  `parse_pob_skill_groups` (shared build).
- **A gem's natural colour** — static game data; `get_gem_detail` (never memory).
- **Exact per-socket gem + colour + off-colour, in one call**, for the user's *own*
  loaded character — `get_socketed_gems` (GGG API). The convenient authoritative
  source; the essentials are also derivable from the three above.

**Off-colour is a colour-count comparison** — a group's gem colours vs its socket
colours — not a per-gem lookup.

---

## Stage 0 — Triage & pre-flight

Ask up front (saves rework):
1. **Which character / build?** Confirm it's loaded in PoB and confirm the league
   (pass `league` / `character_name` explicitly — auto-detect is unreliable).
2. **Goal:** full audit · a specific empty socket · an off-colour check · a
   socket-aware gear swap?
3. **Budget** for chromatics / gear, and any **locked items** (can't recolour or
   replace — e.g. a corrupted item can't be re-chromed).

Then pull the two structural reads:

```
mcp__poe-trade-mcp__get_socketed_gems(character_name=…)   # EXACT binding: colours, links, gem-in-each-socket, empties
mcp__pob__get_skill_setup(main_only=false)                # gem groups: active vs support, item-granted skills
```

**Pause and state the plan** (which items/sockets you'll analyze, whether off-colour
or empty-socket work is in scope so you know to pull gem colours). Wait for approval.

---

## Stage 1 — Build the socket/gem/colour map

Merge the two reads into one per-item view: slot, item, `layout` (e.g. `B-B-B-R`),
link groups, and each socket's colour + the gem in it (level/quality/support) or
`empty`.

`get_socketed_gems` is authoritative for **colours, links, empties, and which gem is
where** — including multi-group items that `get_skill_setup` can't disambiguate (a
body armour split into two 3-links shows as one "Body Armour" slot in
`get_skill_setup`, but `get_socketed_gems` gives the exact per-socket group).

Use `get_skill_setup` for what the API doesn't label: **active vs support** role, and
**item-granted skills**.

**Reconcile the counts** — mismatches are the interesting findings:
- **Empty sockets** (fewer gems than sockets) → candidates for Stage 3.
- **Item-granted skills are NOT socketed.** A skill granted by an item (e.g. Maw of
  Mischief → *Death Wish*) shows up as its own group in `get_skill_setup` but occupies
  **no socket**. Never count it against socket capacity, and never "move" it.
- **Abyssal sockets hold jewels, not skill gems** (e.g. Stygian Vise → Ghastly Eye
  Jewels). They appear in `get_socketed_gems` with colour `A`; treat them as jewels
  (defer to jewel analysis, not gem analysis).

---

## Stage 2 — Off-colour analysis

A gem in a socket whose colour ≠ the gem's natural colour is **off-colour** — it works
in-game but was forced there with chromatics/harder crafting, and PoB hides it
entirely.

**`get_socketed_gems` already reports this.** For each gem in an R/G/B socket it returns
`gem_color` (the gem's natural colour, sourced from the API's authoritative attribute
data) and `off_color`, plus `off_color_count` per item. **White/colourless gems** (no
attribute requirement — Convocation, Portal, etc.) return `gem_color: "W"`, fit any
socket, and are **never** off-colour; the API omits their colour and the tool maps that
to "W". So read off-colours straight from the tool.

Only reach for `get_gem_detail` when you need the colour of a gem that **isn't currently
socketed** — e.g. an empty-socket candidate (Stage 3). Natural colour = the gem's
**dominant attribute requirement**: Strength → **R**, Dexterity → **G**, Intelligence →
**B**; no attribute requirement → **white** (fits any socket).

> **Cardinal rule — never assert a gem's colour from memory.** In one session, two
> memory-based colour claims were both wrong — *Raise Zombie* is **blue** (not red) and
> *Convocation* is **white** (not blue) — each nearly derailing the analysis. The tool's
> `gem_color`/`off_color` come from the game's own data; trust them over recollection,
> and use `get_gem_detail`'s requirements for anything not already socketed.

**Colour-driven unique items are a special case, not an error.** On items whose mods
key off socket colour — **Triad Grip** (minions convert 25% of physical per socket:
Fire/R, Cold/G, Lightning/B, Chaos/W), Tinkerskin, etc. — the *colours are the
mechanic*. Report what the colours produce and whether it matches the build's scaling.
(Agnes's Triad Grip `B-B-B-R` → minions deal 75% Lightning / 25% Fire, and all four
gems happen to be on-colour — a clean setup, not an off-colour problem.)

For any off-colour found, estimate **chromatic difficulty** from the base's attribute
requirements: colours matching the base's dominant attribute are cheap; forcing a
colour the base has no requirement for (e.g. a pure-dex base needing 3 blue) is
expensive — flag it and consider `Vorici`/fossil/Hillock methods.

---

## Stage 3 — "Best gem for this empty socket?"

An empty socket can only be answered with its **colour** and its **link group** — both
from `get_socketed_gems`. Work in this order:

1. **Colour** — the empty socket's colour constrains cheap options to gems of that
   natural colour (others require a recolour first; note the cost).
2. **Link membership** — is the empty socket in the same group as an active skill?
   - **Linked to an active skill** → a *support* gem for that skill is the high-value
     use. Shortlist supports that (a) are that socket's colour and (b) support the
     skill's tags (confirm tags via `get_gem_detail`).
   - **Unlinked / its own group** → only a standalone active/utility gem helps (aura,
     golem, movement, guard, curse-on-self, Convocation, etc.).
3. **Value** — shortlist 2–4 candidates, then **hand off to
   [`build-optimization-sim.md`](build-optimization-sim.md) Stage 2b**: `add_gem` each
   into the live build and sim the DPS/EHP delta. Do not guess the value — sim it.

Recommend the winner with: colour (and recolour cost if off-colour), the link it
joins, and the simmed gain.

---

## Stage 4 — Arrangement improvements

With the full map, look for structural wins (then sim value in
`build-optimization-sim`):

- **Support in the wrong link** — a support gem in a group with no active skill (or the
  wrong skill's group) does nothing. `get_socketed_gems` groups reveal this.
- **Main skill under-linked** while a lesser skill hogs a bigger link → consider
  swapping which skill lives in the best link.
- **Missing obvious support** in a link with an empty socket (Stage 3).
- **Redundant/dead supports** for the build's scaling → `build-optimization-sim`
  Stage 2 owns the DPS-value call; this playbook just flags the socket/colour
  feasibility of the swap (does the replacement fit the colour?).
- **Quality/level** gaps are `build-optimization-sim`'s domain — note but don't
  re-audit here.

---

## Stage 5 — Socket-aware gear implications

When a slot is a purchase candidate (hand the search itself to
[`gear-shopping.md`](gear-shopping.md)):

- **Default: match the existing socket arrangement.** Unless the user says otherwise,
  a replacement should have **≥ the same links** and be able to hold the same gem
  colours — otherwise the gem setup breaks or needs expensive recolouring/re-linking.
  Use `search_trade` with `min_links` (and socket-colour filters where the trade site
  supports them).
- **"Easily modified to match"** = the base's attribute requirements make the needed
  colours cheap, and the item isn't corrupted (corrupted → colours/links locked).
- **Colour-driven uniques** (Triad Grip et al.): a replacement must reproduce the
  *functional* colour counts, not just the link count — losing a blue socket changes
  the minion damage type.

---

## Shared-build variant — required colours from a PoB link

When the input is a **build link** (pobb.in / poedb.tw / pastebin), not the user's
own loaded character, you can't use `get_socketed_gems` (that reads *their* live
character from the PoE API). Reconstruct it from the export instead. The file stores
gem **identity + grouping** *and* each **item's actual socket colours** (the author's
real `Sockets:` layout); only a *gem's own* colour is game data that's looked up.

1. **Pull the structure:** `mcp__poe-data-mcp__parse_pob_skill_groups(link, skill_set=…)`.
   A build usually has many skill sets (per act / progression stage) — the returned
   `skill_sets` index lists them; pick the one you're copying (e.g. the endgame set)
   by id or title substring. You get every link group: its gems (name/skillId/
   level/quality/support), `gem_count`, an item `slot` **only when the author bound
   one**, and — for slot-bound groups — `item_sockets`: the item's **actual** socket
   colours (e.g. `B-R-G-B-B-B`). That's the author's real coloring, the direct target
   to replicate; derive from gems (below) for unassigned groups and to sanity-check.
2. **The link group is the unit.** Unassigned groups (`slot: null`) are
   item-agnostic — any gear with the right links/colours hosts them. A `slot` appears
   only when the **item itself is load-bearing**: a real N-link, a +gem-level weapon,
   or a support-granting unique. Report those as "needs *this* item".
3. **Derive each gem's colour** via `mcp__pob__get_gem_detail` — dominant attribute
   requirement → R/G/B, no requirement → **white** (fits any). **Read at a mid/high
   level** (e.g. 20): low levels omit the requirement (Void Manipulation and Unbound
   Ailments show none at L1 — and Void Manipulation is *Dex/green*, not blue).
4. **Required colours per group** = the colour counts of its non-white gems, in a
   link of `gem_count` size. e.g. a 6-link of Raise Zombie(B) + Multistrike(R) +
   Minion Damage(B) + Vaal Skeletons(B) + Void Manip(G) + Unbound Ailments(B) →
   **`4B 1R 1G`**.
5. **Subtract item-granted supports.** A support-granting unique inflates `gem_count`
   without adding sockets — **The Hungry Loop** shows 6 gems but is a 1-socket unset
   ring: it holds one gem and *grants* the rest. Its real requirement is 1 socket of
   the socketed gem's colour, not a 6-link.
6. **Flag chromatic difficulty** against the target base (Stage 2): e.g. that
   `4B` on Cospri's Will (an *evasion/Dex* base — wants green) is a heavy off-colour.

### Output template — the socketing guide

Render the result as an implementation guide someone can follow, in this shape:

- **Load-bearing gear** (specific items — colours must match): one entry per
  slot-bound group → *item · link size · **colours** (from `item_sockets`) · the gems
  it holds*, plus the craft steps: **buy → Jeweller's (sockets) → Fusing (links) →
  Chromatic / bench "N sockets coloured X" / Harvest (colours)**, with **off-colour
  difficulty flagged** (dominant-attribute base vs required colours). Call out
  support-granting uniques (Hungry Loop: 1 real socket, level the supports in to be
  consumed).
- **Item-agnostic groups** (any spare sockets — helmet / gloves / boots): a table of
  *link size · **colours** (derived from gems) · gems*. Note the easiest base for each
  (e.g. a `4B` link → an Int/ES piece).
- **Don't build these:** PoB DPS-calc dummies, alternate/duplicate groups (e.g. the
  same spectre link shown per spectre), and item-*granted* skills (temp chains from
  the AG's gloves) — flag them so they aren't mistaken for real sockets.
- **One-line takeaway:** which single item carries the real cost (usually the one
  heavy off-colour), everything else being on-colour or trivial.

---

## Stage 6 — Record findings & close

Update `character_data/<Account>/<League>/<Character>/build.md`:
- Add a dated "Socket / Gem-Layout" section: the full per-item map (colours, links,
  gem-in-each-socket), any off-colours (with chromatic difficulty), empty sockets and
  the recommended gem (with simmed gain), and arrangement changes.
- Add follow-ups (unsimmed candidates, gear-swap socket constraints) to Open Questions.

---

## Pitfalls (this playbook exists to encode these)

| Pitfall | Reality |
|---|---|
| Reading socket colours from PoB | PoB **discards** them on import — use `get_socketed_gems` (API) |
| Gem colours from memory | Frequently wrong (Raise Zombie is **blue**, Convocation is **white**) — trust the tool's `gem_color` / `get_gem_detail` |
| Treating a gem's missing API colour as bad data | Absent colour = **white/colourless** gem (fits any socket), not an error — the tool reports `gem_color: "W"` |
| Counting item-granted skills as socketed | They occupy **no** socket (Maw of Mischief → Death Wish) |
| Reading gem colour at gem level 1 | Low levels omit the attribute requirement — read at mid/high level (Void Manipulation is **green**, not blue) |
| Treating a support-granting unique's group as a real link | The Hungry Loop shows 6 gems but is a **1-socket** ring (grants the supports) — subtract item-granted supports |
| Treating abyssal sockets as gem sockets | They hold **jewels** — defer to jewel analysis |
| Recommending a gem for an empty socket without its colour/link | Needs both — a support only helps if **linked** to an active skill of the right colour |
| Assuming Triad-Grip-style colours are "wrong" | The colours are the **mechanic** — analyze the conversion they produce |
| Guessing a change's DPS value here | Hand to `build-optimization-sim` and **sim** it |

---

## Data sources

| Source | Gives | Notes |
|---|---|---|
| `mcp__poe-trade-mcp__get_socketed_gems` | Exact colours, links, gem-in-each-socket, empties, **off-colour** (`gem_color`/`off_color`) | **Authoritative** for the user's own loaded character; white gems report `gem_color: "W"` |
| `mcp__poe-data-mcp__parse_pob_skill_groups` | Link groups per skill set from a **build link** (gems, support flags, item slot bindings) | For copying a shared build; **no colours** (derive via get_gem_detail) |
| `mcp__pob__get_skill_setup` | Gem groups, active/support, item-granted skills | No colours |
| `mcp__pob__get_socket_colors` | Item colour layout from the live PoB build | Fallback if API unavailable; **no gem binding** |
| `mcp__pob__get_gem_detail` | Gem tags + attribute requirements (→ natural colour) | Patch-current; the authoritative colour source |
| [`build-optimization-sim.md`](build-optimization-sim.md) | DPS/EHP value of a gem change | Sim every candidate here |
| [`gear-shopping.md`](gear-shopping.md) | Socket-aware replacement search | `min_links`, colour matching |
