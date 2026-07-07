#!/usr/bin/env bash
# SessionStart hook: suite + PoB update check.
# Prints a message ONLY when action is needed; silent (empty stdout) when current.
# Mirrors the check described in CLAUDE.md "Session-start update check".

cd "$(dirname "$0")/.." 2>/dev/null || exit 0

out=""

# --- 1. Suite upstream commits ---
if git fetch origin --quiet 2>/dev/null; then
  n=$(git log HEAD..origin/main --oneline 2>/dev/null | grep -c . || true)
  if [ "${n:-0}" -gt 0 ] 2>/dev/null; then
    out="poe_mcp_suite has $n upstream commit(s) — run 'git pull' to update."
  fi
fi

# --- 2. PoB version (skip silently if PoB not installed here) ---
changelog="${POB_CHANGELOG:-$APPDATA/Path of Building Community/changelog.txt}"
if [ -f "$changelog" ]; then
  installed=$(head -1 "$changelog" | sed -n 's/^VERSION\[\([0-9.]*\)\].*/\1/p')
  latest=$(curl -s --max-time 10 https://api.github.com/repos/PathOfBuildingCommunity/PathOfBuilding/releases/latest 2>/dev/null \
    | sed -n 's/.*"tag_name": *"v\{0,1\}\([0-9.]*\)".*/\1/p' | head -1)
  if [ -n "$installed" ] && [ -n "$latest" ] && [ "$installed" != "$latest" ]; then
    [ -n "$out" ] && out="$out"$'\n'
    out="${out}PoB has an update: installed $installed → latest $latest. Update via the PoB launcher, then relaunch via pob-mcp/LaunchPoBWithAPI.bat."
  fi
fi

# Stdout from a SessionStart hook is injected into model context.
# Empty output = nothing injected = invisible when everything is current.
if [ -n "$out" ]; then
  printf '[Session-start update check] %s\n' "$out"
fi
exit 0
