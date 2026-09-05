# Plausible Analytics Setup

## Prerequisites

- Plausible account (cloud: https://plausible.io or self-hosted)
- Site added to Plausible dashboard
- Business plan or higher for Stats API access (cloud)

## Authentication

Bearer token from dashboard:

1. Go to https://plausible.io/settings/api-keys (cloud) or your instance
2. Create new API key
3. Copy token (shown once)

Store in: `E:\Dev\.tools\.api-keys.txt`
```
PLAUSIBLE_API_KEY=your_token_here
PLAUSIBLE_BASE_URL=https://plausible.io
```

## Verify Connection

```powershell
$token = (Get-Content "E:\Dev\.tools\.api-keys.txt" | Where-Object { $_ -match "^PLAUSIBLE_API_KEY=" }) -replace "PLAUSIBLE_API_KEY=", ""
$headers = @{ Authorization = "Bearer $token" }
Invoke-RestMethod -Uri "https://plausible.io/api/v2/query" -Headers $headers -Method Post -Body '{"site_id":"yourdomain.com","metrics":["visitors"],"date_range":"7d"}' -ContentType "application/json"
```

Expected: JSON with visitor count for last 7 days.

## Stats API v2 (Key Queries)

Base: `https://plausible.io/api/v2/query` (POST)

### Visitors last 30 days
```json
{
  "site_id": "yourdomain.com",
  "metrics": ["visitors", "pageviews", "bounce_rate", "visit_duration"],
  "date_range": "30d"
}
```

### Top pages
```json
{
  "site_id": "yourdomain.com",
  "metrics": ["visitors", "pageviews"],
  "date_range": "30d",
  "dimensions": ["event:page"],
  "order_by": [["visitors", "desc"]],
  "limit": 20
}
```

### Traffic sources
```json
{
  "site_id": "yourdomain.com",
  "metrics": ["visitors"],
  "date_range": "30d",
  "dimensions": ["visit:source"],
  "order_by": [["visitors", "desc"]]
}
```

### Goal conversions (demo requests, form submissions)
```json
{
  "site_id": "yourdomain.com",
  "metrics": ["visitors", "events"],
  "date_range": "30d",
  "dimensions": ["event:goal"],
  "filters": [["is", "event:goal", ["Demo Request", "Whitepaper Download"]]]
}
```

## Key Facts

- Auth: Bearer token in Authorization header
- API: Stats API v2 (POST-based query interface)
- Rate limit: 600 requests/hour (cloud)
- No cookie consent required (privacy-first)
- GDPR/PECR/CCPA compliant by default
- Cloud: from $9/month (Stats API on Business plan)
- Self-hosted: free (Docker), Stats API included
