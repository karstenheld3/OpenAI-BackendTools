<#
.SYNOPSIS
    Delete Cascade conversation files from disk.
.DESCRIPTION
    Removes .pb conversation files from ~/.codeium/windsurf/cascade/ (and optionally implicit/).
    ALWAYS previews before deletion unless -Confirm is specified.
    Recommend closing Windsurf before deleting to avoid file handle conflicts.
.PARAMETER Index
    Delete conversation(s) by index number from cascade-search.ps1 output.
    Accepts single index (5), range (3-7), or comma-separated (1,3,5).
.PARAMETER Before
    Delete all conversations last modified before this date (YYYY-MM-DD).
.PARAMETER OlderThanDays
    Delete all conversations older than N days.
.PARAMETER UUID
    Delete specific conversation by UUID (filename without .pb extension).
.PARAMETER IncludeImplicit
    Also target the implicit/ folder.
.PARAMETER Confirm
    Skip preview and delete immediately (DANGEROUS).
.PARAMETER DryRun
    Show what would be deleted without actually deleting.
.EXAMPLE
    .\cascade-delete.ps1 -Index 1
    .\cascade-delete.ps1 -Index 3-7
    .\cascade-delete.ps1 -Index 1,3,5
    .\cascade-delete.ps1 -Before 2026-06-01
    .\cascade-delete.ps1 -OlderThanDays 30
    .\cascade-delete.ps1 -UUID "05b6ae42-8d3b-4624-9272-7248d8b20d83"
    .\cascade-delete.ps1 -Before 2026-06-01 -DryRun
#>
[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$Index,
    [string]$Before,
    [int]$OlderThanDays,
    [string]$UUID,
    [switch]$IncludeImplicit,
    [switch]$Confirm,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'

$cascadeDir = Join-Path $env:USERPROFILE '.codeium\windsurf\cascade'
$implicitDir = Join-Path $env:USERPROFILE '.codeium\windsurf\implicit'

if (-not (Test-Path $cascadeDir)) {
    Write-Error "Cascade directory not found: $cascadeDir"
    return
}

# Collect all .pb files (same logic as cascade-search.ps1)
$allFiles = Get-ChildItem -Path $cascadeDir -Filter '*.pb' -File
if ($IncludeImplicit -and (Test-Path $implicitDir)) {
    $allFiles = @($allFiles) + @(Get-ChildItem -Path $implicitDir -Filter '*.pb' -File)
}
$allFiles = $allFiles | Sort-Object LastWriteTime -Descending

# Determine target files based on parameters
$targets = @()

if ($UUID) {
    $targets = $allFiles | Where-Object { $_.BaseName -eq $UUID }
    if ($targets.Count -eq 0) {
        Write-Error "No conversation found with UUID: $UUID"
        return
    }
}
elseif ($Before) {
    $beforeDate = [datetime]::ParseExact($Before, 'yyyy-MM-dd', $null)
    $targets = $allFiles | Where-Object { $_.LastWriteTime -lt $beforeDate }
}
elseif ($OlderThanDays -gt 0) {
    $cutoff = (Get-Date).AddDays(-$OlderThanDays)
    $targets = $allFiles | Where-Object { $_.LastWriteTime -lt $cutoff }
}
elseif ($Index) {
    # Parse index specification: single (5), range (3-7), or list (1,3,5)
    $indices = @()
    foreach ($part in ($Index -split ',')) {
        $part = $part.Trim()
        if ($part -match '^(\d+)-(\d+)$') {
            $start = [int]$Matches[1]
            $end = [int]$Matches[2]
            $indices += $start..$end
        }
        elseif ($part -match '^\d+$') {
            $indices += [int]$part
        }
        else {
            Write-Error "Invalid index format: $part. Use: 5, 3-7, or 1,3,5"
            return
        }
    }
    # Indices are 1-based, referencing sorted-by-date order (newest first)
    foreach ($i in $indices) {
        if ($i -lt 1 -or $i -gt $allFiles.Count) {
            Write-Error "Index $i out of range (1-$($allFiles.Count))"
            return
        }
        $targets += $allFiles[$i - 1]
    }
}
else {
    Write-Error "Specify one of: -Index, -Before, -OlderThanDays, or -UUID"
    return
}

if ($targets.Count -eq 0) {
    Write-Host 'No conversations match the specified criteria.' -ForegroundColor Yellow
    return
}

# Preview
Write-Host ''
Write-Host "DELETE PREVIEW" -ForegroundColor Red
Write-Host ('=' * 70)
Write-Host ('{0,-18} {1,-10} {2,-8} {3}' -f 'Last Modified', 'Size', 'Source', 'UUID')
Write-Host ('-' * 70)

$totalSize = 0
foreach ($f in $targets) {
    $source = if ($f.DirectoryName -match 'implicit') { 'implicit' } else { 'cascade' }
    $sizeMB = [math]::Round($f.Length / 1MB, 1)
    $sizeLabel = if ($sizeMB -ge 1) { "${sizeMB} MB" } else { "$([math]::Round($f.Length / 1KB, 0)) KB" }
    $totalSize += $f.Length
    Write-Host ('{0,-18} {1,-10} {2,-8} {3}' -f $f.LastWriteTime.ToString('yyyy-MM-dd HH:mm'), $sizeLabel, $source, $f.BaseName)
}

Write-Host ('-' * 70)
Write-Host "$($targets.Count) file(s), $([math]::Round($totalSize / 1MB, 1)) MB total" -ForegroundColor Yellow
Write-Host ''

if ($DryRun) {
    Write-Host '[DRY RUN] No files deleted.' -ForegroundColor Cyan
    return
}

# Confirmation
if (-not $Confirm) {
    Write-Host 'WARNING: Cascade conversations are encrypted and CANNOT be recovered after deletion.' -ForegroundColor Red
    Write-Host 'WARNING: Close Windsurf before deleting to avoid file handle conflicts.' -ForegroundColor Red
    Write-Host ''
    $response = Read-Host 'Delete these conversations? (yes/no)'
    if ($response -notin @('yes', 'y')) {
        Write-Host 'Cancelled.' -ForegroundColor Yellow
        return
    }
}

# Execute deletion
$deleted = 0
$failed = 0
foreach ($f in $targets) {
    try {
        Remove-Item $f.FullName -Force
        $deleted++
    }
    catch {
        Write-Host "FAILED: $($f.Name) - $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
}

# Also remove associated .tmp files
foreach ($f in $targets) {
    $tmpPattern = "$($f.BaseName).*.tmp"
    $tmpFiles = Get-ChildItem -Path $f.DirectoryName -Filter $tmpPattern -File -ErrorAction SilentlyContinue
    foreach ($tmp in $tmpFiles) {
        try {
            Remove-Item $tmp.FullName -Force
            Write-Host "  Removed tmp: $($tmp.Name)" -ForegroundColor DarkGray
        }
        catch { }
    }
}

Write-Host ''
Write-Host "RESULT: $deleted deleted, $failed failed" -ForegroundColor $(if ($failed -gt 0) { 'Red' } else { 'Green' })
if ($deleted -gt 0) {
    Write-Host 'Restart Windsurf for changes to take effect.' -ForegroundColor Cyan
}
