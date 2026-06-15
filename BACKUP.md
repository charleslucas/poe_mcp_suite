# Backing up your poe_mcp_suite data

Most of this repo is git-tracked (code lives in submodules), but a few pieces of
**hand-built, irreplaceable data live outside git** and won't survive a reinstall
or move to a new machine on their own:

| Data | Real location | What it is |
|------|---------------|------------|
| `character_data` | `%APPDATA%\poe_claude_data` (junctioned into the repo) | Per-character journals, snapshots, build profiles, guides, `analysis_log.md` |
| `memory` | `%USERPROFILE%\.claude\projects\<project-slug>\memory` | Claude auto-memory: your preferences, feedback, TOS acknowledgement |

Everything else that isn't committed is **regenerable** (`reference_data/` is 96 MB
of cacheable game data; the skilltree/atlastree forks are submodules) so the backup
flow deliberately skips it.

The flow is two PowerShell scripts in [`scripts/`](scripts/). They're tested on
Windows PowerShell 5.1.

---

## Back up

```powershell
powershell -ExecutionPolicy Bypass -File scripts\backup-data.ps1
```

Produces a timestamped zip (~100–300 KB) at `%USERPROFILE%\poe_mcp_suite_backups\poe_data_backup_<timestamp>.zip`
containing `character_data\`, `memory\`, and a `MANIFEST.txt`.

Useful options:

| Option | Effect |
|--------|--------|
| `-OutDir <path>` | Write the zip elsewhere — e.g. `-OutDir "$env:OneDrive\poe_backups"` for automatic offsite backup |
| `-IncludeConfig` | Also archive `.mcp.json`, with `POE_SESSION_ID` **redacted** |
| `-IncludeConfig -IncludeSecret` | Archive `.mcp.json` with the session cookie **in cleartext** (convenience vs. security trade-off) |
| `-MemoryDir <path>` | Override the memory source (if your clone path differs — see below) |

**Tip — automatic backups:** point `-OutDir` at a synced folder (OneDrive/Dropbox),
or register `backup-data.ps1` as a Windows Task Scheduler job for periodic snapshots.

---

## Restore (same machine or a new one)

1. Clone the suite with submodules and follow [`CLAUDE_INSTALL.md`](CLAUDE_INSTALL.md).
2. Restore the data:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\restore-data.ps1 -Zip "C:\path\to\poe_data_backup_<timestamp>.zip"
```

This:
- restores `character_data` → `%APPDATA%\poe_claude_data` (an existing dir is backed
  up to `…\poe_claude_data.bak_<timestamp>` first, unless you pass `-Force`),
- restores `memory` → the Claude project memory dir (auto-located by matching
  `*poe*mcp*suite*` under `%USERPROFILE%\.claude\projects\`),
- re-creates the repo's `character_data` junction if it's missing.

### Cross-machine caveats

- **Memory dir slug depends on the clone path.** Claude derives the project memory
  folder name from the repo's absolute path. If you clone to a *different* path than
  the original machine, auto-location may find the wrong dir or none — pass
  `-MemoryDest "<...>\.claude\projects\<slug>\memory"` explicitly. The script warns
  and lists candidates when it can't pick one confidently.
- **`.mcp.json` is never auto-installed.** If the archive contains one (from
  `-IncludeConfig`), the script leaves it in the extracted temp folder and prints the
  path; copy it to `.mcp.json` and re-enter `POE_SESSION_ID` if it was redacted.
  Otherwise create `.mcp.json` from `.mcp.json.example` as usual.
