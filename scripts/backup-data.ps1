<#
.SYNOPSIS
  Back up the non-git-tracked poe_mcp_suite user/character data into a timestamped zip.

.DESCRIPTION
  Archives the two pieces of hand-built, irreplaceable data that live outside git:
    - character_data  (the per-character cache: journals, snapshots, build profiles,
                       guides, analysis_log) -- real location %APPDATA%\poe_claude_data
    - memory          (Claude auto-memory: preferences, feedback, TOS ack)

  Optionally includes .mcp.json. By default the POE_SESSION_ID is REDACTED; pass
  -IncludeSecret to keep it as-is (the session cookie then lives inside the archive).

  Restore with scripts\restore-data.ps1 -Zip <produced-file>.

.EXAMPLE
  pwsh scripts\backup-data.ps1
  pwsh scripts\backup-data.ps1 -OutDir "$env:OneDrive\poe_backups"
  pwsh scripts\backup-data.ps1 -IncludeConfig            # adds redacted .mcp.json
  pwsh scripts\backup-data.ps1 -IncludeConfig -IncludeSecret
#>
[CmdletBinding()]
param(
    [string]$OutDir = (Join-Path $env:USERPROFILE 'poe_mcp_suite_backups'),
    [string]$CharacterData = (Join-Path $env:APPDATA 'poe_claude_data'),
    [string]$MemoryDir = (Join-Path $env:USERPROFILE '.claude\projects\c--Users-charl-tools-poe-mcp-suite\memory'),
    [switch]$IncludeConfig,
    [switch]$IncludeSecret,
    [string]$ConfigPath
)
$ErrorActionPreference = 'Stop'

$scriptDir = Split-Path -Parent $PSCommandPath
if (-not $ConfigPath) { $ConfigPath = Join-Path $scriptDir '..\.mcp.json' }

$stamp   = Get-Date -Format 'yyyyMMdd_HHmmss'
$staging = Join-Path ([System.IO.Path]::GetTempPath()) ("poe_backup_$stamp")
New-Item -ItemType Directory -Force -Path $staging | Out-Null

try {
    if (Test-Path $CharacterData) {
        Copy-Item -Recurse -Force $CharacterData (Join-Path $staging 'character_data')
        Write-Host "  + character_data  <- $CharacterData"
    } else {
        Write-Warning "character_data not found at $CharacterData (skipped)"
    }

    if (Test-Path $MemoryDir) {
        Copy-Item -Recurse -Force $MemoryDir (Join-Path $staging 'memory')
        Write-Host "  + memory          <- $MemoryDir"
    } else {
        Write-Warning "memory dir not found at $MemoryDir (skipped) -- pass -MemoryDir if it lives elsewhere"
    }

    $cfgNote = ''
    if ($IncludeConfig) {
        if (Test-Path $ConfigPath) {
            $dest = Join-Path $staging 'mcp.json'
            if ($IncludeSecret) {
                Copy-Item $ConfigPath $dest
                $cfgNote = "  mcp.json       <- $ConfigPath (secret: INCLUDED)"
                Write-Warning "POE_SESSION_ID is included in this archive in cleartext."
            } else {
                ((Get-Content $ConfigPath -Raw) -replace '("POE_SESSION_ID"\s*:\s*")[^"]*(")', '${1}REDACTED${2}') |
                    Set-Content $dest -Encoding utf8
                $cfgNote = "  mcp.json       <- $ConfigPath (secret: REDACTED)"
            }
            Write-Host "  + mcp.json        <- $ConfigPath"
        } else {
            Write-Warning ".mcp.json not found at $ConfigPath (config skipped)"
        }
    }

    $manifest = @"
poe_mcp_suite data backup
Created : $(Get-Date -Format o)
Machine : $env:COMPUTERNAME
User    : $env:USERNAME

Contents:
  character_data <- $CharacterData
  memory         <- $MemoryDir
$cfgNote

Restore:
  pwsh scripts\restore-data.ps1 -Zip "<this-file>"
"@
    $manifest | Set-Content (Join-Path $staging 'MANIFEST.txt') -Encoding utf8

    New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
    $zip = Join-Path $OutDir ("poe_data_backup_$stamp.zip")
    if (Test-Path $zip) { Remove-Item $zip -Force }
    Compress-Archive -Path (Join-Path $staging '*') -DestinationPath $zip

    $size = '{0:N0} KB' -f ((Get-Item $zip).Length / 1KB)
    Write-Host ""
    Write-Host "Backup created: $zip ($size)"
}
finally {
    if (Test-Path $staging) { Remove-Item -Recurse -Force $staging }
}
