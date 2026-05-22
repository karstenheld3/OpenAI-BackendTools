<#
.SYNOPSIS
    Apply ID3v2.3 tags to MP3 files from YouTube metadata JSON.

.DESCRIPTION
    Thin wrapper that delegates to set_mp3_tags_from_youtube_metadata.py for all tag writing.
    Reads an enriched YouTube metadata JSON file (from Download-Youtube-Metadata.ps1 + agent enrichment)
    and applies ID3v2.3 tags to matching MP3 files via mutagen (Python).
    Renames files from [youtube_id].mp3 to [mp3_filename] during tagging.
    Preserves original file timestamps.

.PARAMETER JsonPath
    Path to the enriched .tmp_[TOPIC]_youtube-metadata.json file.

.PARAMETER Mp3Folder
    Folder containing the MP3 files (named as [youtube_id].mp3 or already renamed).

.PARAMETER DryRun
    Show what would be done without modifying any files.

.EXAMPLE
    .\Set-Mp3-Tags-From-Youtube-Metadata.ps1 -JsonPath "D:\downloads\.tmp_Test_youtube-metadata.json" -Mp3Folder "D:\downloads"

.EXAMPLE
    .\Set-Mp3-Tags-From-Youtube-Metadata.ps1 -JsonPath "D:\downloads\.tmp_Test_youtube-metadata.json" -Mp3Folder "D:\downloads" -DryRun
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string]$JsonPath,

    [Parameter(Mandatory = $true)]
    [string]$Mp3Folder,

    [Parameter()]
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

# Python venv path: [WORKSPACE]/../.tools/llm-venv/Scripts/python.exe
$pythonPath = Join-Path (Split-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) -Parent) ".tools\llm-venv\Scripts\python.exe"
$pyScript = Join-Path $PSScriptRoot "set_mp3_tags_from_youtube_metadata.py"

$pyArgs = @($pyScript, $JsonPath, $Mp3Folder)
if ($DryRun) { $pyArgs += "--dry-run" }

& $pythonPath @pyArgs
exit $LASTEXITCODE
