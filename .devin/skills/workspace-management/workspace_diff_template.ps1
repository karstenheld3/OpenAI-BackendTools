# workspace_diff_template.ps1
# Template: Compare source and target folders, report differences.
# Adapt before use: replace [placeholder] values with workspace constants.
# SK-FL-07: Template file - requires parameter substitution before running.

param(
    [Parameter(Mandatory=$true)]
    [string]$Source,

    [Parameter(Mandatory=$true)]
    [string]$Target,

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

# Read .sync-timestamp if exists
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

# Collect source files
$sourceFiles = @{}
Get-ChildItem -LiteralPath $Source -Recurse -File | ForEach-Object {
    $relativePath = $_.FullName.Substring($Source.Length).TrimStart('\','/')
    if (Test-FileIncluded -RelativePath $relativePath -IncludePatterns $IncludePatterns -ExcludePatterns $ExcludePatterns) {
        $sourceFiles[$relativePath] = $_.FullName
    }
}

# Collect target files
$targetFiles = @{}
if (Test-Path -LiteralPath $Target) {
    Get-ChildItem -LiteralPath $Target -Recurse -File | ForEach-Object {
        $relativePath = $_.FullName.Substring($Target.Length).TrimStart('\','/')
        if (Test-FileIncluded -RelativePath $relativePath -IncludePatterns $IncludePatterns -ExcludePatterns $ExcludePatterns) {
            $targetFiles[$relativePath] = $_.FullName
        }
    }
}

# Compare
$newFiles = @()
$modifiedFiles = @()
$deletedFiles = @()
$skippedFiles = @()
$locallyModifiedFiles = @()

foreach ($relativePath in $sourceFiles.Keys) {
    if ($targetFiles.ContainsKey($relativePath)) {
        # File exists in both - compare hashes
        $sourceHash = Get-FileHash256 -Path $sourceFiles[$relativePath]
        $targetHash = Get-FileHash256 -Path $targetFiles[$relativePath]

        if ($sourceHash -ne $targetHash) {
            # Check if locally modified
            $targetItem = Get-Item -LiteralPath $targetFiles[$relativePath]
            $isLocallyModified = $false
            if ($lastSyncTime -and $targetItem.LastWriteTime -gt $lastSyncTime) {
                $isLocallyModified = $true
            }

            # Check if in preserve list
            $isPreserved = Test-FilePreserved -RelativePath $relativePath -PreserveList $PreserveList

            if ($isPreserved) {
                $skippedFiles += [PSCustomObject]@{
                    Path = $relativePath
                    Reason = "preserve list"
                    LocallyModified = $isLocallyModified
                }
            } else {
                $modifiedFiles += [PSCustomObject]@{
                    Path = $relativePath
                    Reason = "content differs"
                    LocallyModified = $isLocallyModified
                }
                if ($isLocallyModified) {
                    $locallyModifiedFiles += $relativePath
                }
            }
        }
    } else {
        # New file in source
        $newFiles += [PSCustomObject]@{
            Path = $relativePath
            Reason = "new in source"
        }
    }
}

foreach ($relativePath in $targetFiles.Keys) {
    if (-not $sourceFiles.ContainsKey($relativePath)) {
        $isPreserved = Test-FilePreserved -RelativePath $relativePath -PreserveList $PreserveList
        if ($isPreserved) {
            $skippedFiles += [PSCustomObject]@{
                Path = $relativePath
                Reason = "deleted in source but in preserve list"
                LocallyModified = $false
            }
        } else {
            $deletedFiles += [PSCustomObject]@{
                Path = $relativePath
                Reason = "not in source"
            }
        }
    }
}

# Output structured diff report
Write-Host "Workspace Diff Report"
Write-Host "Source: $Source"
Write-Host "Target: $Target"
Write-Host ""
Write-Host "New files ($($newFiles.Count)):"
foreach ($f in $newFiles) {
    Write-Host "  + $($f.Path)"
}
Write-Host ""
Write-Host "Modified files ($($modifiedFiles.Count)):"
foreach ($f in $modifiedFiles) {
    $marker = if ($f.LocallyModified) { " [LOCALLY MODIFIED]" } else { "" }
    Write-Host "  ~ $($f.Path)$marker"
}
Write-Host ""
Write-Host "Deleted files ($($deletedFiles.Count)):"
foreach ($f in $deletedFiles) {
    Write-Host "  - $($f.Path)"
}
Write-Host ""
Write-Host "Skipped files ($($skippedFiles.Count)):"
foreach ($f in $skippedFiles) {
    Write-Host "  ! $($f.Path) ($($f.Reason))"
}
Write-Host ""

if ($locallyModifiedFiles.Count -gt 0) {
    Write-Host "WARNING: $($locallyModifiedFiles.Count) locally-modified file(s) detected." -ForegroundColor Yellow
    Write-Host "These files were modified after last sync and are not in preserve list." -ForegroundColor Yellow
    Write-Host "Review before proceeding with sync." -ForegroundColor Yellow
}

Write-Host "Summary: $($newFiles.Count) new, $($modifiedFiles.Count) modified, $($deletedFiles.Count) deleted, $($skippedFiles.Count) skipped"
