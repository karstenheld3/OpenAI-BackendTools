# workspace_sync_template.ps1
# Template: Execute sync operations based on diff output.
# Adapt before use: replace [placeholder] values with workspace constants.
# SK-FL-07: Template file - requires parameter substitution before running.

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("downstream","upstream")]
    [string]$Direction,

    [Parameter(Mandatory=$true)]
    [string]$Source,

    [Parameter(Mandatory=$true)]
    [string]$Target,

    [Parameter(Mandatory=$false)]
    [switch]$Preview,

    [Parameter(Mandatory=$false)]
    [string[]]$IncludePatterns = @("*"),

    [Parameter(Mandatory=$false)]
    [string[]]$ExcludePatterns = @("_*",".*"),

    [Parameter(Mandatory=$false)]
    [string[]]$PreserveList = @("NOTES.md","PROBLEMS.md","PROGRESS.md","*.local.*")
)

# Error handling
$ErrorActionPreference = "Stop"

# Validate paths
if (-not (Test-Path -LiteralPath $Source)) {
    Write-Host "ERROR: Source path not found: $Source" -ForegroundColor Red
    exit 1
}
if (-not (Test-Path -LiteralPath $Target)) {
    Write-Host "ERROR: Target path not found: $Target" -ForegroundColor Red
    exit 1
}

# For downstream: source is read-only, target is writable
# For upstream: target is read-only, source is writable
if ($Direction -eq "downstream") {
    $fromPath = $Source
    $toPath = $Target
} else {
    $fromPath = $Target
    $toPath = $Source
}

# Read .sync-timestamp
$syncTimestampPath = Join-Path $Target ".sync-timestamp"
$lastSyncTime = $null
if (Test-Path -LiteralPath $syncTimestampPath) {
    $lastSyncTime = Get-Item -LiteralPath $syncTimestampPath | Select-Object -ExpandProperty LastWriteTime
}

# Function: Test if path matches any pattern
function Test-PatternMatch {
    param([string]$Path, [string[]]$Patterns)
    foreach ($pattern in $Patterns) {
        if ($Path -like $pattern) { return $true }
    }
    return $false
}

# Function: Test if file should be included
function Test-FileIncluded {
    param([string]$RelativePath, [string[]]$IncludePatterns, [string[]]$ExcludePatterns)
    if (Test-PatternMatch -Path $RelativePath -Patterns $ExcludePatterns) { return $false }
    if (-not (Test-PatternMatch -Path $RelativePath -Patterns $IncludePatterns)) { return $false }
    return $true
}

# Function: Test if file is in preserve list
function Test-FilePreserved {
    param([string]$RelativePath, [string[]]$PreserveList)
    return (Test-PatternMatch -Path $RelativePath -Patterns $PreserveList)
}

# Function: Get file hash (SHA-256)
function Get-FileHash256 {
    param([string]$Path)
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA-256).Hash
}

# Collect files from source (from) and target (to)
$fromFiles = @{}
Get-ChildItem -LiteralPath $fromPath -Recurse -File | ForEach-Object {
    $relativePath = $_.FullName.Substring($fromPath.Length).TrimStart('\','/')
    if (Test-FileIncluded -RelativePath $relativePath -IncludePatterns $IncludePatterns -ExcludePatterns $ExcludePatterns) {
        $fromFiles[$relativePath] = $_.FullName
    }
}

$toFiles = @{}
Get-ChildItem -LiteralPath $toPath -Recurse -File | ForEach-Object {
    $relativePath = $_.FullName.Substring($toPath.Length).TrimStart('\','/')
    if (Test-FileIncluded -RelativePath $relativePath -IncludePatterns $IncludePatterns -ExcludePatterns $ExcludePatterns) {
        $toFiles[$relativePath] = $_.FullName
    }
}

# Build operation list
$operations = @()

foreach ($relativePath in $fromFiles.Keys) {
    if ($toFiles.ContainsKey($relativePath)) {
        $fromHash = Get-FileHash256 -Path $fromFiles[$relativePath]
        $toHash = Get-FileHash256 -Path $toFiles[$relativePath]

        if ($fromHash -ne $toHash) {
            $isPreserved = Test-FilePreserved -RelativePath $relativePath -PreserveList $PreserveList

            if ($isPreserved) {
                $operations += [PSCustomObject]@{
                    Action = "skip"
                    Path = $relativePath
                    Reason = "preserve list"
                }
            } else {
                # Check if locally modified
                $toItem = Get-Item -LiteralPath $toFiles[$relativePath]
                $isLocallyModified = $false
                if ($lastSyncTime -and $toItem.LastWriteTime -gt $lastSyncTime) {
                    $isLocallyModified = $true
                }

                if ($isLocallyModified) {
                    $operations += [PSCustomObject]@{
                        Action = "warn-overwrite"
                        Path = $relativePath
                        Reason = "locally modified, not in preserve list"
                    }
                } else {
                    $operations += [PSCustomObject]@{
                        Action = "overwrite"
                        Path = $relativePath
                        Reason = "content differs"
                    }
                }
            }
        }
    } else {
        $operations += [PSCustomObject]@{
            Action = "add"
            Path = $relativePath
            Reason = "new in source"
        }
    }
}

foreach ($relativePath in $toFiles.Keys) {
    if (-not $fromFiles.ContainsKey($relativePath)) {
        $isPreserved = Test-FilePreserved -RelativePath $relativePath -PreserveList $PreserveList
        if ($isPreserved) {
            $operations += [PSCustomObject]@{
                Action = "skip"
                Path = $relativePath
                Reason = "deleted in source but in preserve list"
            }
        } else {
            $operations += [PSCustomObject]@{
                Action = "delete"
                Path = $relativePath
                Reason = "not in source"
            }
        }
    }
}

# Preview mode: show operations only
if ($Preview) {
    Write-Host "Workspace Sync Preview (dry-run)"
    Write-Host "Direction: $Direction"
    Write-Host "From: $fromPath"
    Write-Host "To: $toPath"
    Write-Host ""
    Write-Host "Operations ($($operations.Count)):"
    foreach ($op in $operations) {
        $marker = switch ($op.Action) {
            "add" { "+" }
            "overwrite" { "~" }
            "delete" { "-" }
            "skip" { "!" }
            "warn-overwrite" { "~!" }
        }
        Write-Host "  $marker $($op.Path) ($($op.Reason))"
    }
    Write-Host ""
    Write-Host "Preview complete. No changes made."
    exit 0
}

# Execute mode: perform operations
$added = 0
$modified = 0
$deleted = 0
$skipped = 0
$warnings = 0

foreach ($op in $operations) {
    switch ($op.Action) {
        "add" {
            $targetFile = Join-Path $toPath $op.Path
            $sourceFile = $fromFiles[$op.Path]
            $targetDir = Split-Path -Parent $targetFile
            if (-not (Test-Path -LiteralPath $targetDir)) {
                New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
            }
            Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
            Write-Host "  + $($op.Path)"
            $added++
        }
        "overwrite" {
            $targetFile = $toFiles[$op.Path]
            $sourceFile = $fromFiles[$op.Path]
            # Backup before overwrite
            $backupPath = "$targetFile._backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item -LiteralPath $targetFile -Destination $backupPath -Force
            Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
            Remove-Item -LiteralPath $backupPath -Force
            Write-Host "  ~ $($op.Path)"
            $modified++
        }
        "warn-overwrite" {
            Write-Host "  ~! $($op.Path) - WARNING: locally modified, overwriting" -ForegroundColor Yellow
            $targetFile = $toFiles[$op.Path]
            $sourceFile = $fromFiles[$op.Path]
            $backupPath = "$targetFile._backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
            Copy-Item -LiteralPath $targetFile -Destination $backupPath -Force
            Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
            Remove-Item -LiteralPath $backupPath -Force
            $modified++
            $warnings++
        }
        "delete" {
            $targetFile = $toFiles[$op.Path]
            Remove-Item -LiteralPath $targetFile -Force
            Write-Host "  - $($op.Path)"
            $deleted++
        }
        "skip" {
            Write-Host "  ! $($op.Path) ($($op.Reason))"
            $skipped++
        }
    }
}

# Update .sync-timestamp
$timestampPath = Join-Path $Target ".sync-timestamp"
Set-Content -LiteralPath $timestampPath -Value (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') -Encoding UTF8

# Summary
Write-Host ""
Write-Host "Sync complete."
Write-Host "  Added: $added"
Write-Host "  Modified: $modified"
Write-Host "  Deleted: $deleted"
Write-Host "  Skipped: $skipped"
if ($warnings -gt 0) {
    Write-Host "  Warnings: $warnings (locally-modified files overwritten)" -ForegroundColor Yellow
}
Write-Host "  Timestamp updated: $timestampPath"
