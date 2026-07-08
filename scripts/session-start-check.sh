#!/usr/bin/env bash
# SessionStart hook: suite + PoB update check, game-patch signal, league-end proximity.
# Prints a message ONLY when action is needed; silent (empty stdout) when current.
# Mirrors the checks described in CLAUDE.md "Session-start update check".

cd "$(dirname "$0")/.." 2>/dev/null || exit 0

# ── League anchors — rolled by the league-transition playbook (Step 7) ──────
TEMP_LEAGUE="${POE_TEMP_LEAGUE:-Mirage}"
LEAGUE_END="${POE_LEAGUE_END:-2026-07-20}"
NEXT_LEAGUE_START="${POE_NEXT_LEAGUE_START:-2026-07-24}"

out=""
append() { [ -n "$out" ] && out="$out"$'\n'; out="$out$1"; }

# --- 1. Suite upstream commits ---
if git fetch origin --quiet 2>/dev/null; then
  n=$(git log HEAD..origin/main --oneline 2>/dev/null | grep -c . || true)
  if [ "${n:-0}" -gt 0 ] 2>/dev/null; then
    append "poe_mcp_suite has $n upstream commit(s) — run 'git pull' to update."
  fi
fi

# --- 2. PoB version (skip silently if PoB not installed here) ---
changelog="${POB_CHANGELOG:-$APPDATA/Path of Building Community/changelog.txt}"
if [ -f "$changelog" ]; then
  installed=$(head -1 "$changelog" | sed -n 's/^VERSION\[\([0-9.]*\)\].*/\1/p')
  latest=$(curl -s --max-time 10 https://api.github.com/repos/PathOfBuildingCommunity/PathOfBuilding/releases/latest 2>/dev/null \
    | sed -n 's/.*"tag_name": *"v\{0,1\}\([0-9.]*\)".*/\1/p' | head -1)
  if [ -n "$installed" ] && [ -n "$latest" ] && [ "$installed" != "$latest" ]; then
    append "PoB has an update: installed $installed → latest $latest. Update via the PoB launcher, then relaunch via pob-mcp/LaunchPoBWithAPI.bat."
  fi
fi

# --- 3. Game client patch signal ---
# The install ships no patch-notes file and the exe carries no version metadata,
# but Steam/the launcher rewrite the exe on every patch — its mtime is a reliable
# "a patch was installed" signal. Only the file timestamp is read; no game data
# is touched (see legal_considerations.md).
poe_exe="${POE_EXE_PATH:-C:/Program Files (x86)/Steam/steamapps/common/Path of Exile/PathOfExile_x64Steam.exe}"
if [ -f "$poe_exe" ]; then
  mtime=$(stat -c %Y "$poe_exe" 2>/dev/null)
  state_file="reference_data/.state/poe_exe_mtime"   # gitignored (all of reference_data is)
  last=$(cat "$state_file" 2>/dev/null)
  if [ -n "$mtime" ] && [ "$mtime" != "$last" ]; then
    mkdir -p "$(dirname "$state_file")" && printf '%s' "$mtime" > "$state_file"
    if [ -n "$last" ]; then  # first run only primes the state, silently
      patched_on=$(date -d "@$mtime" +%F 2>/dev/null)
      append "PoE client was patched since the last session (game exe changed ${patched_on:-recently}). Check reference_data/patch_notes_index.md for the new point release and update freshness_index.md / mechanics_index.md if mechanics changed."
    fi
  fi
fi

# --- 4. League-end proximity (only while POE_LEAGUE still points at the temp league) ---
current_league=$(sed -n 's/.*"POE_LEAGUE" *: *"\([^"]*\)".*/\1/p' .mcp.json 2>/dev/null | head -1)
if [ "$current_league" = "$TEMP_LEAGUE" ]; then
  end_epoch=$(date -d "$LEAGUE_END" +%s 2>/dev/null)
  if [ -n "$end_epoch" ]; then
    days=$(( (end_epoch - $(date +%s)) / 86400 ))
    if [ "$days" -lt 0 ]; then
      append "$TEMP_LEAGUE ended $LEAGUE_END but POE_LEAGUE still points at it — run the league-transition playbook."
    elif [ "$days" -le 7 ]; then
      append "$TEMP_LEAGUE ends in $days day(s) ($LEAGUE_END; next league launches $NEXT_LEAGUE_START) — plan the league-transition run."
    fi
  fi
fi

# Stdout from a SessionStart hook is injected into model context.
# Empty output = nothing injected = invisible when everything is current.
if [ -n "$out" ]; then
  printf '[Session-start update check] %s\n' "$out"
fi
exit 0
