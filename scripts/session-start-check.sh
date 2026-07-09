#!/usr/bin/env bash
# SessionStart hook: suite + PoB update check, game-patch signal, league-end proximity.
# Prints a message ONLY when action is needed; silent (empty stdout) when current.
# Mirrors the checks described in CLAUDE.md "Session-start update check".

cd "$(dirname "$0")/.." 2>/dev/null || exit 0

# ── League anchors — rolled by the league-transition playbook (Step 7.4) ────
# Challenge league (the one POE_LEAGUE tracks) and the next one to launch.
TEMP_LEAGUE="${POE_TEMP_LEAGUE:-Mirage}"
LEAGUE_END="${POE_LEAGUE_END:-2026-07-20}"
NEXT_LEAGUE_START="${POE_NEXT_LEAGUE_START:-2026-07-24}"
NEXT_LEAGUE_NAME="${POE_NEXT_LEAGUE_NAME:-Curse of the Allflame (3.29)}"
# Concurrent EVENT league — ends on its own (earlier) date and POE_LEAGUE never
# points at it, so it needs its own proximity signal (see check 4b).
EVENT_LEAGUE="${POE_EVENT_LEAGUE:-Return of the Ancestors}"
EVENT_END="${POE_EVENT_END:-2026-07-16}"

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
      append "$TEMP_LEAGUE ends in $days day(s) ($LEAGUE_END; $NEXT_LEAGUE_NAME launches $NEXT_LEAGUE_START) — plan the league-transition run."
    fi
  fi
fi

# --- 4b. Event-league end (independent of POE_LEAGUE; events don't flip it) ---
# Event leagues (e.g. Return of the Ancestors) end on their own date and have
# their own fresh-start characters that migrate to Standard/Void — but because
# POE_LEAGUE stays on the challenge league, check 4 never sees them. Signal only
# while an UN-migrated event character still exists (its meta.json league field
# still names the event); the transition playbook flips that field, so this
# self-limits once the migration is done rather than nagging forever.
if [ -n "$EVENT_LEAGUE" ] && [ -n "$EVENT_END" ]; then
  unmigrated=0
  for m in character_data/*/"$EVENT_LEAGUE"/*/meta.json; do
    [ -f "$m" ] || continue
    if grep -q "\"league\" *: *\"$EVENT_LEAGUE\"" "$m" 2>/dev/null; then unmigrated=1; break; fi
  done
  if [ "$unmigrated" = 1 ]; then
    ev_epoch=$(date -d "$EVENT_END" +%s 2>/dev/null)
    if [ -n "$ev_epoch" ]; then
      ev_days=$(( (ev_epoch - $(date +%s)) / 86400 ))
      if [ "$ev_days" -lt 0 ]; then
        append "Event league '$EVENT_LEAGUE' ended $EVENT_END but a character is still marked in it — migrate it to Standard/Void and re-scope event mechanics (league-transition playbook → 'Event leagues' notes)."
      elif [ "$ev_days" -le 7 ]; then
        append "Event league '$EVENT_LEAGUE' ends in $ev_days day(s) ($EVENT_END) — its character(s) migrate to Standard/Void; plan the lightweight event-transition."
      fi
    fi
  fi
fi

# --- 5. Repo hygiene: playbook contribution + pairing drift ---
# Each finding is announced ONCE (state-deduped), then stays quiet forever.
# Three checks: (a) uncommitted playbook drafts; (b) playbook changes not on
# the canonical upstream repo (fork users with an `upstream` remote — skipped
# silently otherwise); (c) playbooks missing their wrapper skill.
hygiene_state="reference_data/.state/announced_hygiene"
mkdir -p "$(dirname "$hygiene_state")" 2>/dev/null && touch "$hygiene_state" 2>/dev/null
first_seen() {  # returns 0 (and records the key) only the first time a key is seen
  grep -qxF "$1" "$hygiene_state" 2>/dev/null && return 1
  printf '%s\n' "$1" >> "$hygiene_state"
  return 0
}

# (a) Untracked playbook drafts
drafts=""
for f in $(git ls-files --others --exclude-standard playbooks/ 2>/dev/null | grep '\.md$'); do
  first_seen "draft:$f" && drafts="$drafts ${f#playbooks/}"
done
[ -n "$drafts" ] && append "Uncommitted playbook draft(s):$drafts — commit once session-tested."

# (b) Playbook changes not on the canonical upstream (fork users)
if git remote get-url upstream >/dev/null 2>&1; then
  git fetch upstream --quiet 2>/dev/null
  unshared=""
  for f in $(git log upstream/main..HEAD --name-only --pretty=format: -- playbooks/ 2>/dev/null | sort -u | grep '\.md$'); do
    first_seen "unshared:$f" && unshared="$unshared ${f#playbooks/}"
  done
  [ -n "$unshared" ] && append "Playbook change(s) not in the canonical upstream repo:$unshared — if session-tested and generally useful, consider a PR back (playbooks/README.md §9)."
fi

# (c) Playbooks missing a wrapper skill (framework/format docs excluded)
noskill=""
for f in playbooks/*.md; do
  [ -f "$f" ] || continue
  base=$(basename "$f" .md)
  case "$base" in README|PLANNING|multi-stage-analysis|build-profile-format) continue;; esac
  if [ ! -f ".claude/skills/$base/SKILL.md" ]; then
    first_seen "noskill:$base" && noskill="$noskill $base"
  fi
done
[ -n "$noskill" ] && append "Playbook(s) missing a wrapper skill in .claude/skills/:$noskill (every domain playbook gets one — playbooks/README.md §7)."

# Stdout from a SessionStart hook is injected into model context.
# Empty output = nothing injected = invisible when everything is current.
if [ -n "$out" ]; then
  printf '[Session-start update check] %s\n' "$out"
fi
exit 0
