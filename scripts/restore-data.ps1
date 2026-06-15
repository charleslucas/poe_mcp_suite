<#
.SYNOPSIS
  Restore poe_mcp_suite user/character data from a backup zip made by backup-data.ps1.

.DESCRIPTION
  Restores:
    - character_data -> %APPDATA%\poe_claude_data  (existing dir is backed up first
                        unless -Force)
    - memory         -> the Claude project memory dir (auto-located, or pass -MemoryDest)
  Re-creates the repo's character_data junction if it is missing.

  Does NOT touch .mcp.json: if the archive contains one it is left in the extracted
  temp folder path printed at the end, so you can copy it manually and re-enter the
  POE_SESSION_ID.

.EXAMPLE
  pwsh scripts\restore-data.ps1 -Zip "$env:USERPROFILE\poe_mcp_suite_backups\poe_data_backup_20260615_120000.zip"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$Zip,
    [string]$CharacterData = (Join-Path $env:APPDATA 'poe_claude_data'),
    [string]$MemoryDest,
    [string]$RepoRoot,
    [switch]$Force
)
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $PSCommandPath
if (-not $RepoRoot) { $RepoRoot = (Resolve-Path (Join-Path $scriptDir '..')).Path }

if (-not (Test-Path $Zip)) { throw "Zip not found: $Zip" }

$tmp = Join-Path ([System.IO.Path]::GetTempPath()) ("poe_restore_" + (Get-Date -Format 'yyyyMMddHHmmss'))
Expand-Archive -Path $Zip -DestinationPath $tmp -Force
Write-Host "Extracted to $tmp"

# --- character_data -> %APPDATA%\poe_claude_data (merge; back up existing) ---
$srcCD = Join-Path $tmp 'character_data'
if (Test-Path $srcCD) {
    if ((Test-Path $CharacterData) -and (-not $Force)) {
        $bak = "$CharacterData.bak_$(Get-Date -Format 'yyyyMMddHHmmss')"
        Write-Host "Existing character_data found -> backing up to $bak"
        Copy-Item -Recurse -Force $CharacterData $bak
    }
    New-Item -ItemType Directory -Force -Path $CharacterData | Out-Null
    Copy-Item -Recurse -Force (Join-Path $srcCD '*') $CharacterData
    Write-Host "Restored character_data -> $CharacterData"
} else {
    Write-Warning "No character_data in archive."
}

# --- memory -> Claude project memory dir ---
$srcMem = Join-Path $tmp 'memory'
if (Test-Path $srcMem) {
    if (-not $MemoryDest) {
        $projects = Join-Path $env:USERPROFILE '.claude\projects'
        $cand = @(Get-ChildItem $projects -Directory -ErrorAction SilentlyContinue |
                  Where-Object { $_.Name -like '*poe*mcp*suite*' })
        if ($cand.Count -eq 1) {
            $MemoryDest = Join-Path $cand[0].FullName 'memory'
        } elseif ($cand.Count -gt 1) {
            Write-Warning ("Multiple candidate project dirs -- re-run with -MemoryDest <path>:`n  " +
                           ($cand.FullName -join "`n  "))
        } else {
            Write-Warning "Could not auto-locate the Claude project memory dir -- re-run with -MemoryDest <path>."
        }
    }
    if ($MemoryDest) {
        New-Item -ItemType Directory -Force -Path $MemoryDest | Out-Null
        Copy-Item -Recurse -Force (Join-Path $srcMem '*') $MemoryDest
        Write-Host "Restored memory -> $MemoryDest"
    }
} else {
    Write-Warning "No memory in archive."
}

# --- recreate the repo's character_data junction if missing ---
$junction = Join-Path $RepoRoot 'character_data'
if (-not (Test-Path $junction)) {
    cmd /c mklink /J "$junction" "$CharacterData" | Out-Null
    Write-Host "Created junction $junction -> $CharacterData"
}

$hadConfig = Test-Path (Join-Path $tmp 'mcp.json')
Write-Host ""
Write-Host "Restore complete."
if ($hadConfig) {
    Write-Host "NOTE: archive contained mcp.json at $tmp\mcp.json -- copy it to $RepoRoot\.mcp.json"
    Write-Host "      and re-enter POE_SESSION_ID if it was redacted. (Temp folder left in place for this.)"
} else {
    Remove-Item -Recurse -Force $tmp
}
