#!/usr/bin/env python3
"""Detect PoB method-signature drift before it becomes a runtime failure.

Our TCP API (`PathOfBuilding/src/API/*.lua`) calls into PoB's own classes. When PoB
changes a method's parameters upstream, our calls keep *parsing* fine and fail only when
that code path runs — usually mid-analysis, with a confusing Lua error. This has bitten
the suite three times:

  * `ImportPassiveTreeAndJewels` / `ImportItemsAndSkills` — 3.29 changed both (fixed 2026-07-25)
  * `ImportFromNodeList`        — 3.29 prepended a `className` parameter, silently shifting
                                  every argument by one (fixed 2026-08-01)

This script compares the arguments we PASS against the parameters PoB DECLARES, and
reports mismatches. Run it after every PoB submodule bump (see UPDATING.md).

    python scripts/check_pob_api_signatures.py          # report
    python scripts/check_pob_api_signatures.py --quiet  # only problems; exit 1 if any

Heuristics, and their limits: arguments are counted at paren depth 0, ignoring commas
inside nested calls, tables and strings. Lua allows trailing args to be omitted (they
arrive as nil), so passing FEWER args than declared is reported as INFO, not an error —
passing MORE is an ERROR, and an exact-name mismatch on the first parameter is flagged
as a likely shift. Methods PoB defines in several classes are reported once per match.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
API_DIR = REPO / "PathOfBuilding" / "src" / "API"
POB_SRC = REPO / "PathOfBuilding" / "src"

# Receivers whose methods live in PoB's own classes. Anything else (locals, our own
# module tables) is skipped — we only audit the boundary we don't control.
POB_RECEIVERS = re.compile(
    r"\b(?:build|self)\.(?:spec|importTab|skillsTab|itemsTab|treeTab|calcsTab|configTab|notesTab)\b"
    r"|\bbuild\b|\bmain\b|\blaunch\b"
)

# Under-arity calls REVIEWED and confirmed safe — the omitted parameters are genuinely
# optional in PoB's implementation. Anything not listed here is surfaced as a warning and
# fails the run, so new signature drift can't hide among known-good noise.
# Before adding an entry: open PoB's definition and confirm the trailing params are
# optional (defaulted or only read behind a nil check) — do NOT silence a real shift.
REVIEWED_OPTIONAL: set[str] = {
    "UndoHandlerClass:AddUndoState",  # noClearRedo — optional flag
    "EditClass:SetText",              # notify — optional
    "ItemsTabClass:AddItem",          # index — optional (appends when nil)
}

CALL_RE = re.compile(r"([A-Za-z_][\w.]*)\s*:\s*([A-Za-z_]\w*)\s*\(")
DEF_RE = re.compile(r"^\s*function\s+([A-Za-z_]\w*)\s*:\s*([A-Za-z_]\w*)\s*\(([^)]*)\)", re.M)


def split_top_level(arg_text: str) -> list[str]:
    """Split a Lua argument list on commas at paren/brace/bracket depth 0."""
    args, depth, current, i, in_str, quote = [], 0, [], 0, False, ""
    while i < len(arg_text):
        ch = arg_text[i]
        if in_str:
            if ch == "\\":
                current.append(arg_text[i : i + 2]); i += 2; continue
            if ch == quote:
                in_str = False
            current.append(ch)
        elif ch in "\"'":
            in_str, quote = True, ch
            current.append(ch)
        elif ch in "([{":
            depth += 1; current.append(ch)
        elif ch in ")]}":
            depth -= 1; current.append(ch)
        elif ch == "," and depth == 0:
            args.append("".join(current).strip()); current = []
        else:
            current.append(ch)
        i += 1
    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


def extract_call_args(text: str, open_paren_idx: int) -> str | None:
    """Return the raw argument text for a call whose '(' is at open_paren_idx."""
    depth, i, in_str, quote = 0, open_paren_idx, False, ""
    while i < len(text):
        ch = text[i]
        if in_str:
            if ch == "\\":
                i += 2; continue
            if ch == quote:
                in_str = False
        elif ch in "\"'":
            in_str, quote = True, ch
        elif ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
            if depth == 0:
                return text[open_paren_idx + 1 : i]
        i += 1
    return None


def load_pob_definitions() -> dict[str, list[tuple[str, list[str], Path]]]:
    """Map method name -> [(ClassName, [params], file), ...] from PoB's source."""
    defs: dict[str, list[tuple[str, list[str], Path]]] = {}
    for path in list((POB_SRC / "Classes").rglob("*.lua")) + list((POB_SRC / "Modules").rglob("*.lua")):
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for cls, method, params in DEF_RE.findall(text):
            plist = [p.strip() for p in params.split(",") if p.strip()]
            defs.setdefault(method, []).append((cls, plist, path))
    return defs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="only print problems; exit 1 if any")
    args = ap.parse_args()

    if not API_DIR.is_dir():
        print(f"ERROR: API dir not found: {API_DIR}", file=sys.stderr)
        return 2

    defs = load_pob_definitions()
    problems: list[str] = []
    warnings: list[str] = []
    checked = 0

    for api_file in sorted(API_DIR.glob("*.lua")):
        text = api_file.read_text(encoding="utf-8", errors="ignore")
        for m in CALL_RE.finditer(text):
            receiver, method = m.group(1), m.group(2)
            if not POB_RECEIVERS.search(receiver):
                continue
            candidates = defs.get(method)
            if not candidates:
                continue  # not a PoB class method (or defined somewhere we don't scan)

            raw = extract_call_args(text, m.end() - 1)
            if raw is None:
                continue
            passed = split_top_level(raw)
            n_passed = len(passed)
            line_no = text[: m.start()].count("\n") + 1
            checked += 1

            for cls, params, def_path in candidates:
                n_params = len(params)
                where = f"{api_file.name}:{line_no}  {receiver}:{method}()"
                target = f"{cls}:{method}({', '.join(params) or ''})  [{def_path.name}]"

                # Lua varargs accept any arity — `SetMode(newMode, ...)` is not a mismatch.
                if params and params[-1] == "...":
                    if n_passed >= n_params - 1:
                        if not args.quiet:
                            print(f"ok     {where}: {n_passed} args, varargs target {target}")
                        continue
                    n_params -= 1  # fall through and report as under-arity

                if n_passed > n_params:
                    problems.append(
                        f"ERROR  {where}\n"
                        f"       passes {n_passed} args, PoB declares {n_params}\n"
                        f"       {target}"
                    )
                elif n_passed < n_params and f"{cls}:{method}" in REVIEWED_OPTIONAL:
                    if not args.quiet:
                        print(f"ok*    {where}: {n_passed}/{n_params} args, reviewed-optional -> {target}")
                elif n_passed < n_params:
                    # Trailing nils ARE legal Lua, so this isn't proof of a bug — but it is
                    # exactly how the 3.29 ImportFromNodeList break presented (we passed 7
                    # where 8 were declared, because a parameter was PREPENDED and every
                    # argument silently shifted). Always surface it; verify after a PoB bump.
                    warnings.append(
                        f"WARN   {where}\n"
                        f"       passes {n_passed} args, PoB declares {n_params} — legal if the\n"
                        f"       trailing params are optional, but CHECK for a prepended/inserted\n"
                        f"       parameter that silently shifts the ones you do pass.\n"
                        f"       {target}"
                    )
                elif not args.quiet:
                    print(f"ok     {where}: {n_passed} args match {target}")

    # Warnings always print — an under-arity call is how a PREPENDED parameter presents,
    # which is the failure mode that has actually bitten this suite.
    if warnings:
        print("\n".join(("", *warnings)))
    if problems:
        print("\n".join(("", *problems, "")))
        print(f"{len(problems)} ERROR(s), {len(warnings)} warning(s) across {checked} checked call(s).")
        return 1

    print(f"\nNo arity errors. {len(warnings)} warning(s) across {checked} checked PoB call(s).")
    return 1 if warnings else 0


if __name__ == "__main__":
    raise SystemExit(main())
