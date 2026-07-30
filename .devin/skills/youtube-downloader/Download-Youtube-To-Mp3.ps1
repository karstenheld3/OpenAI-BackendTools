<#
.SYNOPSIS
    Download YouTube videos as MP3 audio files.

.DESCRIPTION
    Downloads YouTube videos and converts them to MP3 using yt-dlp and ffmpeg.
    Auto-downloads required tools if missing. Supports Chrome cookies for age-restricted content.

.PARAMETER Urls
    One or more YouTube URLs to download.

.PARAMETER OutputFolder
    Output directory for downloaded files. Defaults to [WORKSPACE]/../.tools/_downloaded_audio

.PARAMETER Quality
    Audio bitrate: 128k, 192k, 256k, 320k. Default: 192k

.PARAMETER UseCookies
    Use Chrome cookies for age-restricted content. Default: $true

.PARAMETER ChromeProfile
    Specific Chrome profile name. Auto-detected if not specified.

.PARAMETER UserAgent
    Custom user agent string.

.PARAMETER Retries
    Number of download retries. Default: 3

.PARAMETER SleepInterval
    Minimum seconds between requests. Default: 1

.PARAMETER MaxSleepInterval
    Maximum seconds between requests. Default: 5

.PARAMETER ToolsFolder
    Location for yt-dlp and ffmpeg binaries. Defaults to [WORKSPACE]/../.tools/youtube-downloader

.PARAMETER Playlist
    Download entire playlist instead of single video. Default: $false

.EXAMPLE
    .\Download-Youtube-To-Mp3.ps1 -Urls "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

.EXAMPLE
    .\Download-Youtube-To-Mp3.ps1 -Urls "https://youtu.be/abc123" -Quality 320k -OutputFolder "D:\Music"

.EXAMPLE
    .\Download-Youtube-To-Mp3.ps1 -Urls "https://youtu.be/vid1", "https://youtu.be/vid2" -UseCookies:$false
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true, Position = 0, ValueFromPipeline = $true)]
    [string[]]$Urls,

    [Parameter()]
    [string]$OutputFolder = (Join-Path (Split-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) -Parent) ".tools\_downloaded_audio"),

    [Parameter()]
    [ValidateSet("128k", "192k", "256k", "320k")]
    [string]$Quality = "192k",

    [Parameter()]
    [bool]$UseCookies = $true,

    [Parameter()]
    [string]$ChromeProfile,

    [Parameter()]
    [string]$UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

    [Parameter()]
    [int]$Retries = 3,

    [Parameter()]
    [int]$SleepInterval = 1,

    [Parameter()]
    [int]$MaxSleepInterval = 5,

    [Parameter()]
    [string]$ToolsFolder = (Join-Path (Split-Path (Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent) -Parent) ".tools\youtube-downloader"),

    [Parameter()]
    [switch]$Playlist
)

begin {
    # Ensure tools folder exists
    if (-not (Test-Path $ToolsFolder)) {
        New-Item -ItemType Directory -Path $ToolsFolder -Force | Out-Null
    }

    # Tool paths
    $ytdlpPath = Join-Path $ToolsFolder "yt-dlp.exe"
    $ffmpegPath = Join-Path $ToolsFolder "ffmpeg.exe"
    $ffprobePath = Join-Path $ToolsFolder "ffprobe.exe"

    function Test-ChromeProfile {
        param($profileName, $testUrl)
        if (-not (Test-Path $ytdlpPath)) { return $false }
        $output = & $ytdlpPath --cookies-from-browser "chrome:$profileName" --skip-download $testUrl 2>&1
        return $output -notmatch "ERROR: could not find chrome cookies database"
    }

    function Get-RequiredTools {
        $ffmpegZipPath = Join-Path $ToolsFolder "ffmpeg.zip"
        
        # Check if yt-dlp needs updating
        $needsUpdate = $false
        if (-not (Test-Path $ytdlpPath)) {
            Write-Host "yt-dlp.exe not found. Downloading..." -ForegroundColor Yellow
            $needsUpdate = $true
        } else {
            try {
                $currentVersion = (& $ytdlpPath --version 2>&1) -replace '^(\d{4}\.\d{2}\.\d{2}).*', '$1'
                $latestRelease = Invoke-RestMethod -Uri "https://api.github.com/repos/yt-dlp/yt-dlp/releases/latest" -ErrorAction Stop
                $latestVersion = $latestRelease.tag_name -replace '^v?', ''
                
                if ($currentVersion -ne $latestVersion) {
                    Write-Host "yt-dlp update available: $currentVersion -> $latestVersion" -ForegroundColor Yellow
                    $needsUpdate = $true
                } else {
                    Write-Host "yt-dlp is up to date ($currentVersion)" -ForegroundColor Green
                }
            } catch {
                Write-Host "Could not check yt-dlp version. Using existing version." -ForegroundColor Yellow
            }
        }
        
        if ($needsUpdate) {
            Write-Host "Downloading yt-dlp..." -ForegroundColor Yellow
            try {
                Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile $ytdlpPath -TimeoutSec 300
            } catch {
                Write-Host "Failed to download yt-dlp -> $_" -ForegroundColor Red
                return $false
            }
        }
        
        # Download ffmpeg if not present
        if (-not (Test-Path $ffmpegPath) -or -not (Test-Path $ffprobePath)) {
            Write-Host "Downloading ffmpeg to script folder..." -ForegroundColor Yellow
            try {
                Invoke-WebRequest -Uri "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip" -OutFile $ffmpegZipPath -TimeoutSec 300
                Add-Type -AssemblyName System.IO.Compression.FileSystem
                $zip = [System.IO.Compression.ZipFile]::OpenRead($ffmpegZipPath)
                
                $ffmpegEntry = $zip.Entries | Where-Object { $_.Name -eq "ffmpeg.exe" -and $_.FullName -like "*/bin/*" } | Select-Object -First 1
                $ffprobeEntry = $zip.Entries | Where-Object { $_.Name -eq "ffprobe.exe" -and $_.FullName -like "*/bin/*" } | Select-Object -First 1
                
                if ($ffmpegEntry) { [System.IO.Compression.ZipFileExtensions]::ExtractToFile($ffmpegEntry, $ffmpegPath, $true) }
                if ($ffprobeEntry) { [System.IO.Compression.ZipFileExtensions]::ExtractToFile($ffprobeEntry, $ffprobePath, $true) }
                
                $zip.Dispose()
                Remove-Item $ffmpegZipPath -Force
                Write-Host "ffmpeg downloaded and extracted successfully." -ForegroundColor Green
            } catch {
                Write-Host "Failed to download or extract ffmpeg -> $_" -ForegroundColor Red
                return $false
            }
        }
        return $true
    }

    # Ensure output folder exists
    if (-not (Test-Path $OutputFolder)) {
        New-Item -ItemType Directory -Path $OutputFolder -Force | Out-Null
    }

    # Collect URLs from pipeline
    $allUrls = @()
    $scriptStartTime = Get-Date
}

process {
    $allUrls += $Urls
}

end {
    if ($allUrls.Count -eq 0) {
        Write-Host "ERROR: No URLs provided." -ForegroundColor Red
        exit 1
    }

    # Find working Chrome profile
    $workingProfile = $ChromeProfile
    $cookiesEnabled = $UseCookies

    # Warn if Chrome is running (cookie extraction may fail)
    if ($UseCookies) {
        $chromeRunning = Get-Process chrome -ErrorAction SilentlyContinue
        if ($chromeRunning) {
            Write-Host "WARNING: Chrome is running. Cookie extraction may fail. Close Chrome for best results." -ForegroundColor Yellow
        }
    }

    if ($UseCookies -and -not $ChromeProfile) {
        if (Test-Path $ytdlpPath) {
            $testUrl = $allUrls[0]
            Write-Host "Testing Chrome profiles using URL '$testUrl'..."
            $profiles = Get-ChildItem "$env:LOCALAPPDATA\Google\Chrome\User Data" -Directory -ErrorAction SilentlyContinue | 
                Where-Object { $_.Name -match "^Profile \d+$" -or $_.Name -eq "Default" }
            
            foreach ($chromeProf in $profiles) {
                Write-Host "Trying profile '$($chromeProf.Name)'..."
                if (Test-ChromeProfile $chromeProf.Name $testUrl) {
                    $workingProfile = $chromeProf.Name
                    Write-Host "Found working profile: '$workingProfile'." -ForegroundColor Green
                    break
                }
            }
            
            if (-not $workingProfile) {
                Write-Host "WARNING: No working Chrome profile found." -ForegroundColor Yellow
                $cookiesEnabled = $false
            }
        } else {
            Write-Host "yt-dlp.exe not found. Skipping Chrome profile testing..." -ForegroundColor Yellow
        }
    }

    # Ensure tools are available
    $toolsReady = Get-RequiredTools
    if (-not $toolsReady) {
        Write-Host "ERROR: Required tools not available." -ForegroundColor Red
        exit 1
    }

    # Display settings
    $urlWord = if ($allUrls.Count -eq 1) { "URL" } else { "URLs" }
    Write-Host ""
    Write-Host "==================================== START: YOUTUBE MP3 DOWNLOAD ===================================" -ForegroundColor Cyan
    Write-Host (Get-Date -Format "yyyy-MM-dd HH:mm:ss")
    Write-Host ""
    Write-Host "Output: '$OutputFolder'"
    Write-Host "Format: mp3"
    Write-Host "Quality: $Quality"
    Write-Host "Cookies: $(if ($cookiesEnabled) { "Enabled ('$workingProfile')" } else { "Disabled" })"
    Write-Host "$($allUrls.Count) $urlWord to process."
    Write-Host ""

    # Download each URL
    foreach ($url in $allUrls) {
        Write-Host "Downloading '$url'..." -ForegroundColor Cyan
        
        $dlArgs = @(
            $url
            "-f", "bestaudio[ext=m4a]/bestaudio/best"
            "-x"
            "--audio-format", "mp3"
            "--audio-quality", $Quality
            "-o", (Join-Path $OutputFolder "%(title)s.%(ext)s")
            "--user-agent", $UserAgent
            "--retries", $Retries
            "--fragment-retries", $Retries
            "--sleep-interval", $SleepInterval
            "--max-sleep-interval", $MaxSleepInterval
        )
        
        if ($Playlist) {
            $dlArgs += "--yes-playlist"
        } else {
            $dlArgs += "--no-playlist"
        }
        
        if ($cookiesEnabled -and $workingProfile) {
            $dlArgs += "--cookies-from-browser", "chrome:$workingProfile"
        }
        
        $output = & $ytdlpPath @dlArgs 2>&1
        
        # Check for DPAPI error and retry without cookies
        if ($output -match "Failed to decrypt with DPAPI" -and $cookiesEnabled) {
            Write-Host "Chrome cookie decryption failed. Retrying without cookies..." -ForegroundColor Yellow
            $dlArgs = $dlArgs | Where-Object { $_ -notmatch "cookies-from-browser" -and $_ -ne "chrome:$workingProfile" }
            & $ytdlpPath @dlArgs
        } else {
            $output | ForEach-Object { Write-Host $_ }
        }
        
        Write-Host ""
    }

    Write-Host "Download complete." -ForegroundColor Green

    # Footer
    $elapsed = (Get-Date) - $scriptStartTime
    if ($elapsed.TotalSeconds -lt 60) { $duration = "$([math]::Round($elapsed.TotalSeconds, 1)) secs" }
    elseif ($elapsed.TotalMinutes -lt 60) { $duration = "$([math]::Floor($elapsed.TotalMinutes)) mins $($elapsed.Seconds) secs" }
    else { $duration = "$([math]::Floor($elapsed.TotalHours)) hours $($elapsed.Minutes) mins" }
    Write-Host ""
    Write-Host "===================================== END: YOUTUBE MP3 DOWNLOAD ====================================" -ForegroundColor Cyan
    Write-Host "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') ($duration)"
}
