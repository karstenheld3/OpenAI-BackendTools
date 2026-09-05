# IndexNow URL Submission Script
# Usage: Run after publishing new content. Replace {{PLACEHOLDERS}} with values.
# Docs: https://www.indexnow.org/documentation

param(
    [Parameter(Mandatory = $true)]
    [string[]]$Urls,

    [string]$Key = "{{INDEXNOW_KEY}}",
    [string]$SiteHost = "{{YOUR_DOMAIN}}",
    [string]$KeyLocation = "https://{{YOUR_DOMAIN}}/{{INDEXNOW_KEY}}.txt"
)

$endpoint = "https://api.indexnow.org/IndexNow"

if ($Urls.Count -eq 1) {
    # Single URL: use GET
    $submitUrl = "https://api.indexnow.org/indexnow?url=$($Urls[0])&key=$Key"
    Write-Host "Submitting URL '$($Urls[0])'..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri $submitUrl -Method Get -TimeoutSec 15
}
else {
    # Batch: use POST (up to 10,000 URLs)
    $body = @{
        host        = $SiteHost
        key         = $Key
        keyLocation = $KeyLocation
        urlList     = $Urls
    } | ConvertTo-Json -Depth 3

    Write-Host "Submitting $($Urls.Count) URLs to IndexNow..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri $endpoint -Method Post -Body $body -ContentType "application/json; charset=utf-8" -TimeoutSec 30
}

switch ($response.StatusCode) {
    200 { Write-Host "OK. URLs submitted." -ForegroundColor Green }
    202 { Write-Host "OK. Accepted -> key pending verification. Retry in a few minutes." -ForegroundColor Cyan }
    400 { Write-Error "Submission failed -> Bad request -> Check URL format." }
    403 { Write-Error "Submission failed -> Forbidden -> Key file not accessible at '$KeyLocation'." }
    422 { Write-Error "Submission failed -> Unprocessable -> Invalid key or URL." }
    default { Write-Warning "Unexpected status: $($response.StatusCode)." }
}
