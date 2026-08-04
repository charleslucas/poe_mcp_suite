> **Canonical home:** `poe_mcp_suite/frameworks/` (public). Instance data is patch-stamped (3.29) — re-verify after any league/patch change. `local library:` references point into the maintainer's private guide library (character data + digested third-party guides, not distributed); treat them as worked-example citations, not links.

# _concepts/ — the cross-build TECH database

One file per **tech**: a mechanism/pairing that works across otherwise-unrelated builds (conversion
ladders, trigger automation, charge engines…). Style templates (`_styles/`) and archetype entries link
here instead of restating mechanics — vastly different builds use the same techs, so the tech is the
unit of reuse (decided with user, 2026-08-04).

**Required fields per entry:**
- **Aliases:** the community names for it — different groups name the same tech differently, and the
  aliases are the *search keys* for future surveys. Record them as encountered; never invent them.
- **Status + confidence:** `IDEA` → `VERIFIED-ON-PAPER` → `REALIZED` (measured on a real character), with
  ✅/◐/⛔ labels on individual claims.
- **Mechanism** — including the intuitive-but-wrong version if there is one (the trap is often the most
  valuable part of the entry).
- **Availability/scope** — how you actually GET it (mod source, league/core status), gated per
  `playbooks/gear-shopping.md`'s obtainability pitfall.
- **Builds using it** — links both ways (archetype entries / style templates / live characters).
- **References** — YouTube videos, published build guides, and **detailed reddit posts that act as
  tutorials** for the tech, with creator and date/patch where known. These are the fastest route to a
  working implementation when the tech gets picked up later — and they date the claim (a 3.24 video is a
  ◐ for 3.29 mechanics). Reddit tutorial threads especially: they're where techs get named, so they feed
  the Aliases field too.

Current entries: [`minion-fire-to-chaos.md`](minion-fire-to-chaos.md) (REALIZED 2026-08-04) ·
[`minion-concepts.md`](minion-concepts.md) (grab-bag; split into per-tech files as items mature).
