<#
.SYNOPSIS
    Extract YouTube metadata to JSON for MP3 tagging workflow.

.DESCRIPTION
    Uses yt-dlp --dump-json to extract metadata (title, description, URL, date)
    from YouTube videos, playlists, or channels. Outputs a consolidated JSON file
    with one entry per video, ready for agent enrichment (Step 3) and tag writing (Step 4).

.PARAMETER Urls
    One or more YouTube URLs (video, playlist, or channel).

.PARAMETER Topic
    Topic name used in the output filename: .tmp_[TOPIC]_youtube-metadata.json

.PARAMETER OutputFolder
    Directory for the output JSON file.

.PARAMETER ToolsFolder
    Location for yt-dlp binary. Defaults to [WORKSPACE]/../.tools/youtube-downloader

.PARAMETER Force
    Overwrite existing JSON file for same topic.

.EXAMPLE
    .\Download-Youtube-Metadata.ps1 -Urls "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -Topic "Test" -OutputFolder "D:\downloads"

.EXAMPLE
    .\Download-Youtube-Metadata.ps1 -Urls "https://www.youtube.com/@channelname" -Topic "ChannelDump" -OutputFolder "D:\downloads" -Force
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [string[]]$Urls,

    [Parameter(Mandatory = $true)]
    [string]$Topic,

    [Parameter(Mandatory = $true)]
    [string]$OutputFolder,

    [Parameter()]
    [string]$ToolsFolder = (Join-Path (Split-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) -Parent) ".tools\youtube-downloader"),

    [Parameter()]
    [switch]$Force
)

begin {
    $ErrorActionPreference = "Stop"

    # Output file path
    $OutputFile = Join-Path $OutputFolder ".tmp_${Topic}_youtube-metadata.json"

    # Check existing file
    if ((Test-Path $OutputFile) -and -not $Force) {
        Write-Host "ERROR: Output file already exists: '$OutputFile'. Use -Force to overwrite." -ForegroundColor Red
        exit 1
    }

    # Validate yt-dlp
    $ytdlpPath = Join-Path $ToolsFolder "yt-dlp.exe"
    if (-not (Test-Path $ytdlpPath)) {
        Write-Host "ERROR: yt-dlp not found at '$ytdlpPath'." -ForegroundColor Red
        exit 1
    }

    # Ensure output folder exists
    if (-not (Test-Path $OutputFolder)) {
        New-Item -ItemType Directory -Path $OutputFolder -Force | Out-Null
    }

    $allVideos = [System.Collections.Generic.List[object]]::new()
    $skippedCount = 0
    $scriptStartTime = Get-Date
}

process {
    # Header
    $urlWord = if ($Urls.Count -eq 1) { "URL" } else { "URLs" }
    Write-Host ""
    Write-Host "================================ START: YOUTUBE METADATA EXTRACTION ================================" -ForegroundColor Cyan
    Write-Host (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    Write-Host ""
    Write-Host "Topic: '$Topic'"
    Write-Host "Output: '$OutputFile'"
    Write-Host "$($Urls.Count) $urlWord to process."
    Write-Host ""

    foreach ($url in $Urls) {
        Write-Host "Extracting metadata from '$url'..."

        $ytArgs = @(
            "--skip-download"
            "--dump-json"
            "--socket-timeout", "30"
            "--retries", "3"
            "--sleep-interval", "1"
            "--max-sleep-interval", "3"
            "--extractor-args", "youtube:player_client=android"
            "--no-warnings"
            $url
        )

        $videoCount = 0

        try {
            & $ytdlpPath @ytArgs 2>&1 | ForEach-Object {
                $line = $_

                # yt-dlp error lines (stderr redirected to stdout)
                if ($line -is [System.Management.Automation.ErrorRecord]) {
                    $errMsg = $line.ToString()
                    if ($errMsg -match "unavailable|private|removed|deleted") {
                        $skippedCount++
                        Write-Host "  WARNING: Video unavailable - skipped." -ForegroundColor Yellow
                    }
                    return
                }

                # Parse JSON line
                try {
                    $videoJson = $line | ConvertFrom-Json

                    $videoCount++
                    $titlePreview = $videoJson.title
                    if ($titlePreview.Length -gt 60) {
                        $titlePreview = $titlePreview.Substring(0, 57) + "..."
                    }
                    Write-Host "  [ $($allVideos.Count + 1) ] $($videoJson.id) - $titlePreview"

                    # Extract upload_date -> published_date (YYYYMMDD -> YYYY-MM-DD)
                    $publishedDate = ""
                    $rawDate = if ($videoJson.upload_date) { $videoJson.upload_date } else { "" }
                    if ($rawDate -match "^\d{8}$") {
                        $publishedDate = "$($rawDate.Substring(0,4))-$($rawDate.Substring(4,2))-$($rawDate.Substring(6,2))"
                    }

                    $entry = [ordered]@{
                        youtube_id        = $videoJson.id
                        title             = $videoJson.title
                        url               = $videoJson.webpage_url
                        description       = if ($videoJson.description) { $videoJson.description } else { "" }
                        published_date    = $publishedDate
                        download_filename = ""
                        mp3_title         = ""
                        mp3_artist        = ""
                        mp3_year          = ""
                        mp3_encoded_by    = ""
                        mp3_filename      = ""
                    }

                    $allVideos.Add($entry)
                }
                catch {
                    # Non-JSON output from yt-dlp (progress lines, etc.)
                }
            }

            if ($videoCount -gt 0) {
                $vidWord = if ($videoCount -eq 1) { "video" } else { "videos" }
                Write-Host "  $videoCount $vidWord extracted from this URL."
            }
        }
        catch {
            Write-Host "  ERROR: Failed to extract metadata from '$url' -> $($_.Exception.Message)" -ForegroundColor Red
        }
    }
}

end {
    if ($allVideos.Count -eq 0) {
        Write-Host ""
        Write-Host "FAIL: No metadata extracted. Check URLs and network connection." -ForegroundColor Red
        exit 1
    }

    # Build consolidated JSON
    $output = [ordered]@{
        topic   = $Topic
        created = (Get-Date -Format "yyyy-MM-dd HH:mm")
        videos  = $allVideos.ToArray()
    }

    # Write JSON with UTF-8 encoding
    $jsonText = $output | ConvertTo-Json -Depth 4
    [System.IO.File]::WriteAllText($OutputFile, $jsonText, [System.Text.Encoding]::UTF8)

    # Summary
    $videoWord = if ($allVideos.Count -eq 1) { "video" } else { "videos" }
    $skippedSuffix = if ($skippedCount -gt 0) { ", $skippedCount skipped" } else { "" }
    Write-Host ""
    Write-Host "Metadata saved: '$OutputFile' ($($allVideos.Count) $videoWord$skippedSuffix)."
    Write-Host "OK." -ForegroundColor Green

    # Footer
    $elapsed = (Get-Date) - $scriptStartTime
    if ($elapsed.TotalSeconds -lt 60) { $duration = "$([math]::Round($elapsed.TotalSeconds, 1)) secs" }
    elseif ($elapsed.TotalMinutes -lt 60) { $duration = "$([math]::Floor($elapsed.TotalMinutes)) mins $($elapsed.Seconds) secs" }
    else { $duration = "$([math]::Floor($elapsed.TotalHours)) hours $($elapsed.Minutes) mins" }
    Write-Host ""
    Write-Host "================================= END: YOUTUBE METADATA EXTRACTION =================================" -ForegroundColor Cyan
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ($duration)"

    # Return output path for caller
    Write-Output $OutputFile
}
