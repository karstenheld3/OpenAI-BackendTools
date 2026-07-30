<#
.SYNOPSIS
    List and search Cascade conversation files on disk.
.DESCRIPTION
    Searches ~/.codeium/windsurf/cascade/ for .pb conversation files.
    Shows file metadata (date, size, UUID) since content is encrypted.
    Supports filtering by date range, count, or size threshold.
.PARAMETER Last
    Show the N most recent conversations (default: 10)
.PARAMETER Since
    Show conversations modified after this date (YYYY-MM-DD)
.PARAMETER Before
    Show conversations modified before this date (YYYY-MM-DD)
.PARAMETER MinSizeMB
    Only show conversations larger than N MB
.PARAMETER IncludeImplicit
    Also search the implicit/ folder (background conversations)
.PARAMETER Raw
    Output as objects for pipeline use (no formatting)
.EXAMPLE
    .\cascade-search.ps1
    .\cascade-search.ps1 -Last 5
    .\cascade-search.ps1 -Since 2026-07-01
    .\cascade-search.ps1 -Since 2026-07-01 -Before 2026-07-08
    .\cascade-search.ps1 -MinSizeMB 10
    .\cascade-search.ps1 -IncludeImplicit
#>
[CmdletBinding()]
param(
    [int]$Last = 10,
    [string]$Since,
    [string]$Before,
    [double]$MinSizeMB = 0,
    [switch]$IncludeImplicit,
    [switch]$Raw
)

$ErrorActionPreference = 'Stop'

# Resolve cascade directory
$cascadeDir = Join-Path $env:USERPROFILE '.codeium\windsurf\cascade'
$implicitDir = Join-Path $env:USERPROFILE '.codeium\windsurf\implicit'

if (-not (Test-Path $cascadeDir)) {
    Write-Error "Cascade directory not found: $cascadeDir"
    return
}

# Collect .pb files
$files = Get-ChildItem -Path $cascadeDir -Filter '*.pb' -File

if ($IncludeImplicit -and (Test-Path $implicitDir)) {
    $implicitFiles = Get-ChildItem -Path $implicitDir -Filter '*.pb' -File
    $files = @($files) + @($implicitFiles)
}

# Apply filters
if ($Since) {
    $sinceDate = [datetime]::ParseExact($Since, 'yyyy-MM-dd', $null)
    $files = $files | Where-Object { $_.LastWriteTime -ge $sinceDate }
}

if ($Before) {
    $beforeDate = [datetime]::ParseExact($Before, 'yyyy-MM-dd', $null).AddDays(1)
    $files = $files | Where-Object { $_.LastWriteTime -lt $beforeDate }
}

if ($MinSizeMB -gt 0) {
    $minBytes = $MinSizeMB * 1MB
    $files = $files | Where-Object { $_.Length -ge $minBytes }
}

# Sort by date (newest first) and limit
$files = $files | Sort-Object LastWriteTime -Descending | Select-Object -First $Last

if ($files.Count -eq 0) {
    Write-Host 'No conversations found matching criteria.' -ForegroundColor Yellow
    return
}

# Build result objects
$results = @()
$index = 1
foreach ($f in $files) {
    $source = if ($f.DirectoryName -match 'implicit') { 'implicit' } else { 'cascade' }
    $sizeMB = [math]::Round($f.Length / 1MB, 1)
    $sizeLabel = if ($sizeMB -ge 1) { "${sizeMB} MB" } else { "$([math]::Round($f.Length / 1KB, 0)) KB" }
    $results += [PSCustomObject]@{
        Index        = $index
        Date         = $f.LastWriteTime.ToString('yyyy-MM-dd HH:mm')
        Size         = $sizeLabel
        SizeBytes    = $f.Length
        UUID         = $f.BaseName
        Source       = $source
        FullPath     = $f.FullName
    }
    $index++
}

if ($Raw) {
    return $results
}

# Display formatted output
Write-Host ''
Write-Host "Cascade Conversations ($($results.Count) found)" -ForegroundColor Cyan
Write-Host ('-' * 80)
Write-Host ('{0,-5} {1,-18} {2,-10} {3,-8} {4}' -f 'No.', 'Last Modified', 'Size', 'Source', 'UUID')
Write-Host ('-' * 80)

foreach ($r in $results) {
    $color = if ($r.Source -eq 'implicit') { 'DarkGray' } else { 'White' }
    Write-Host ('{0,-5} {1,-18} {2,-10} {3,-8} {4}' -f $r.Index, $r.Date, $r.Size, $r.Source, $r.UUID) -ForegroundColor $color
}

Write-Host ('-' * 80)
Write-Host "Total size: $([math]::Round(($results | Measure-Object -Property SizeBytes -Sum).Sum / 1MB, 1)) MB" -ForegroundColor DarkGray
Write-Host ''
Write-Host 'NOTE: Content is encrypted. Identification by date/size only.' -ForegroundColor Yellow
Write-Host 'Use cascade-delete.ps1 -Index <N> or -Before <date> to delete.' -ForegroundColor Yellow
