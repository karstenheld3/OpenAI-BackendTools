# DataForSEO API Query Script
# Usage: .\query.ps1 -Action balance|keywords|serp|competitors|backlinks
# Docs: https://docs.dataforseo.com/v3/
#
# Examples:
#   .\query.ps1 -Action balance
#   .\query.ps1 -Action keywords -Keyword "AI compliance"
#   .\query.ps1 -Action keywords -Keyword "regulatory reporting" -Location 2840 -Lang de -Limit 30
#   .\query.ps1 -Action serp -Keyword "DORA automation software"
#   .\query.ps1 -Action competitors -Domain yourdomain.com
#   .\query.ps1 -Action backlinks -Domain competitor.com

param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("balance", "keywords", "serp", "competitors", "backlinks")]
    [string]$Action,

    [string]$Keyword,
    [string]$Domain,
    [int]$Location = 2276,
    [string]$Lang = "en",
    [int]$Limit = 30,
    [string]$Device = "desktop",
    [string]$ApiKeysPath = "E:\Dev\.tools\.api-keys.txt"
)

$ErrorActionPreference = "Stop"
$baseUrl = "https://api.dataforseo.com/v3"

# --- Load credentials ---
$base64 = (Get-Content $ApiKeysPath | Where-Object { $_ -match "^DATAFORSEO_BASE64=" }) -replace "DATAFORSEO_BASE64=", ""
if (-not $base64) {
    Write-Error "Credential load failed -> DATAFORSEO_BASE64 not found in '$ApiKeysPath'"
    exit 1
}

$headers = @{
    "Authorization" = "Basic $base64"
    "Content-Type"  = "application/json"
}

# --- Helper: POST to API ---
function Invoke-DfsApi {
    param([string]$Endpoint, [array]$Body)

    Write-Host "Querying '$Endpoint'..." -ForegroundColor DarkGray
    $jsonBody = ConvertTo-Json -InputObject $Body -Depth 10 -Compress
    try {
        $response = Invoke-RestMethod -Uri "$baseUrl/$Endpoint" -Headers $headers -Method Post -Body $jsonBody -TimeoutSec 30
    }
    catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 403) {
            Write-Error "Account not verified. Verify at: 'https://app.dataforseo.com/'"
        }
        else {
            Write-Error "Request failed -> HTTP $statusCode -> $_"
        }
        exit 1
    }

    if ($response.status_code -ne 20000) {
        Write-Error "API error -> $($response.status_code) -> $($response.status_message)"
        Write-Host "HINT: If account is unverified, all data endpoints fail. Verify at: 'https://app.dataforseo.com/'" -ForegroundColor DarkYellow
        exit 1
    }
    $task = $response.tasks[0]
    if ($task.status_code -ne 20000) {
        Write-Error "Task error -> $($task.status_code) -> $($task.status_message)"
        Write-Host "HINT: If account is unverified, all data endpoints fail. Verify at: 'https://app.dataforseo.com/'" -ForegroundColor DarkYellow
        exit 1
    }
    return $task
}

# --- Actions ---
switch ($Action) {
    "balance" {
        Write-Host "Fetching account balance..." -ForegroundColor DarkGray
        $userData = Invoke-RestMethod -Uri "$baseUrl/appendix/user_data" -Headers $headers -Method Get -TimeoutSec 15
        $money = $userData.tasks[0].result[0].money
        Write-Host "Balance:      `$$($money.balance)" -ForegroundColor Cyan
        Write-Host "Total spent:  `$$($money.total)"
    }

    "keywords" {
        if (-not $Keyword) { Write-Error "-Keyword required for 'keywords' action"; exit 1 }
        $task = Invoke-DfsApi -Endpoint "dataforseo_labs/google/keyword_suggestions/live" -Body @(
            @{
                keyword              = $Keyword
                location_code        = $Location
                language_code        = $Lang
                limit                = $Limit
                include_seed_keyword = $true
            }
        )
        $items = $task.result[0].items
        if (-not $items) { Write-Host "0 suggestions found."; return }

        $items | ForEach-Object {
            [PSCustomObject]@{
                Keyword    = $_.keyword
                Volume     = $_.keyword_info.search_volume
                Difficulty = $_.keyword_properties.keyword_difficulty
                CPC        = [math]::Round(($_.keyword_info.cpc -as [double]), 2)
                Intent     = $_.search_intent_info.main_intent
            }
        } | Sort-Object Volume -Descending | Select-Object -First $Limit | Format-Table -AutoSize

        Write-Host "$($items.Count) suggestions found. Cost: ~`$0.0006." -ForegroundColor Green
    }

    "serp" {
        if (-not $Keyword) { Write-Error "-Keyword required for 'serp' action"; exit 1 }
        $task = Invoke-DfsApi -Endpoint "serp/google/organic/live/advanced" -Body @(
            @{
                keyword       = $Keyword
                location_code = $Location
                language_code = $Lang
                device        = $Device
            }
        )
        $result = $task.result[0]
        $items = $result.items
        $organics = $items | Where-Object { $_.type -eq "organic" } | Select-Object -First 10

        Write-Host "SERP for: keyword='$Keyword' (location=$Location, device='$Device')" -ForegroundColor Yellow
        Write-Host "$($result.se_results_count) total results."
        $organics | ForEach-Object {
            [PSCustomObject]@{
                Position = $_.rank_absolute
                Domain   = $_.domain
                Title    = if ($_.title.Length -gt 50) { $_.title.Substring(0, 50) } else { $_.title }
            }
        } | Format-Table -AutoSize

        $aiOverview = $items | Where-Object { $_.type -eq "ai_overview" }
        if ($aiOverview) { Write-Host "[AI Overview present]" -ForegroundColor Magenta }
        Write-Host "Cost: ~`$0.002." -ForegroundColor Green
    }

    "competitors" {
        if (-not $Domain) { Write-Error "-Domain required for 'competitors' action"; exit 1 }
        $task = Invoke-DfsApi -Endpoint "dataforseo_labs/google/competitors_domain/live" -Body @(
            @{
                target        = $Domain
                location_code = $Location
                language_code = $Lang
                limit         = $Limit
            }
        )
        $items = $task.result[0].items
        if (-not $items) { Write-Host "0 competitors found for '$Domain'."; return }

        Write-Host "Competitors for: target='$Domain' (location=$Location)" -ForegroundColor Yellow
        $items | Select-Object -First $Limit | ForEach-Object {
            [PSCustomObject]@{
                Domain   = $_.domain
                AvgPos   = [math]::Round(($_.avg_position -as [double]), 1)
                Overlap  = $_.intersections
                Keywords = $_.full_domain_metrics.organic.count
                Traffic  = [math]::Round(($_.full_domain_metrics.organic.etv -as [double]), 0)
            }
        } | Format-Table -AutoSize

        Write-Host "$($items.Count) competitors found. Cost: ~`$0.0006." -ForegroundColor Green
    }

    "backlinks" {
        if (-not $Domain) { Write-Error "-Domain required for 'backlinks' action"; exit 1 }
        $task = Invoke-DfsApi -Endpoint "backlinks/summary/live" -Body @(
            @{
                target               = $Domain
                internal_list_limit  = 0
                backlinks_status_type = "all"
            }
        )
        $r = $task.result[0]
        Write-Host "Backlink summary for: target='$Domain'" -ForegroundColor Yellow
        Write-Host "  Total backlinks:   $($r.backlinks)"
        Write-Host "  Referring domains: $($r.referring_domains)"
        Write-Host "  Referring IPs:     $($r.referring_ips)"
        Write-Host "  Domain rank:       $($r.rank)"
        Write-Host "  Broken backlinks:  $($r.broken_backlinks)"
        Write-Host "`nCost: ~`$0.002." -ForegroundColor Green
    }
}
