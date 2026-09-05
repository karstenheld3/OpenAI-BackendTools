---
name: seo-tools
description: SEO data APIs and search engine tools. Apply when researching keywords, analyzing competitors, tracking rankings, submitting URLs for indexing, or querying web analytics.
compatibility: Windows, PowerShell 7+, Python 3.10+ (for DataForSEO client). Node.js 18+ (for MCP servers).
---

# SEO Tools Skill

SEO data retrieval, keyword research, competitor analysis, URL indexing, and analytics via API.

**References** (loaded on demand per platform):
- `{platform}/SETUP.md` - Authentication and configuration
- `{platform}/ENDPOINTS.md` - API endpoint reference (where applicable)
- `dataforseo/query.ps1` - PowerShell: query DataForSEO API
- `dataforseo/query.py` - Python: query DataForSEO API
- `indexnow/submit.ps1` - PowerShell: submit URLs to IndexNow

## MUST-NOT-FORGET

1. DataForSEO costs money per query - estimate cost before batch operations
2. Never hardcode credentials - load from `E:\Dev\.tools\.api-keys.txt` (keys: DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD, DATAFORSEO_BASE64)
3. Check balance before large operations: `python query.py balance`
4. Account must be verified at https://app.dataforseo.com/ before data endpoints work (balance endpoint works without verification)
5. Location codes required for geo-targeted queries: 2276=Germany, 2840=US, 2826=UK, 2250=France
6. Rate limits in response headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`) - respect them
7. Standard method stores results 30 days; Live method does not store results
8. IndexNow key file must be HTTPS-accessible at domain root - verify after deploy

## Intent Lookup

**User wants to...**
- **Research keywords for a topic** -> `python query.py keywords "SEED"` or `.\query.ps1 -Action keywords -Keyword "SEED"`
- **Check who ranks for a keyword** -> `python query.py serp "KEYWORD"` or `.\query.ps1 -Action serp -Keyword "KEYWORD"`
- **Find competitor domains** -> `python query.py competitors DOMAIN` or `.\query.ps1 -Action competitors -Domain DOMAIN`
- **Analyze backlink profile** -> `python query.py backlinks DOMAIN` or `.\query.ps1 -Action backlinks -Domain DOMAIN`
- **Track brand in LLM responses** -> `dataforseo/ENDPOINTS.md` (AI Optimization API: llm_mentions)
- **Monitor search rankings** -> `google-search-console/` (MCP: quick_wins, traffic_drops)
- **Find content decay** -> `google-search-console/` (MCP: content_decay)
- **Submit URL to Google** -> `google-search-console/` (MCP: submit_url)
- **Submit URL to Bing/Yandex** -> `.\submit.ps1 -Urls "URL"` (indexnow/)
- **Check site traffic/conversions** -> `plausible/` (Stats API v2)
- **Check DataForSEO balance** -> `python query.py balance` or `.\query.ps1 -Action balance`

## Platform Registry

- **dataforseo/** - Keyword research, SERP data, competitor analysis, backlinks, AI/GEO optimization. Pay-per-query ($0.0006-$0.002). Basic Auth.
- **google-search-console/** - Ranking monitoring, quick wins, content decay detection, URL submission. Free. OAuth via MCP.
- **indexnow/** - Instant URL notification to Bing, Yandex, Seznam, Naver. Free. Key file auth.
- **plausible/** - Privacy-first web analytics. Stats API v2. Bearer token. $0-9/month.

## Core Procedures

### 1. Quick Keyword Research

```powershell
# Python
python query.py keywords "AI compliance" --location 2276 --lang en --limit 30

# PowerShell
.\query.ps1 -Action keywords -Keyword "AI compliance" -Location 2276 -Lang en -Limit 30
```

Output: table with Keyword, Volume, Difficulty, CPC, Intent. Cost: $0.0006/task.

### 2. Check SERP for Keyword

```powershell
# Python
python query.py serp "regulatory reporting automation" --device desktop

# PowerShell
.\query.ps1 -Action serp -Keyword "regulatory reporting automation" -Device desktop
```

Output: top 10 organic results (position, domain, title) + AI Overview indicator. Cost: $0.002/task.

### 3. Find Competitors

```powershell
# Python
python query.py competitors yourdomain.com --limit 20

# PowerShell
.\query.ps1 -Action competitors -Domain yourdomain.com -Limit 20
```

Output: competing domains with keyword overlap, traffic estimate, avg position. Cost: $0.0006/task.

### 4. Backlink Analysis

```powershell
# Python
python query.py backlinks competitor.com

# PowerShell
.\query.ps1 -Action backlinks -Domain competitor.com
```

Output: total backlinks, referring domains, IPs, subnets, rank, broken links. Cost: $0.002/task.

### 5. Submit URL After Publishing

```powershell
# IndexNow (Bing/Yandex) - replace key and domain
.\submit.ps1 -Urls "https://yourdomain.com/blog/new-post" -Key YOUR_KEY -SiteHost yourdomain.com

# Google (via GSC MCP): Use submit_url tool with the published URL
```

Cost: Free (both).

### 6. Check Balance

```powershell
python query.py balance
.\query.ps1 -Action balance
```

Output: current balance, total spent.

## Gotchas

- **DataForSEO sandbox also requires verification** - Both sandbox and production return 403 until account is verified. Use `--sandbox` flag in query.py for dummy data testing after verification.
- **Location codes are NOT country codes** - Germany is 2276, not "DE". Use `/v3/appendix/locations` to look up.
- **Keywords Data vs Labs** - Keywords Data API uses Google Ads data (official volumes). Labs API uses clickstream + SERP data (broader, includes keyword suggestions). Different data sources, different costs.
- **SERP task_post vs live** - task_post is 3x cheaper but async (poll for results). live returns immediately. For single queries use live; for batch use task_post.
- **IndexNow key file casing** - Key and filename must match exactly (case-sensitive on Linux hosts).
- **GSC MCP server variety** - Multiple community servers exist with different tool sets. Check SETUP.md for recommended one.

## Quick Config

Verify setup:
```powershell
# Python (from dataforseo/ folder)
python query.py balance

# PowerShell (from dataforseo/ folder)
.\query.ps1 -Action balance

# Use sandbox for dummy data (still requires account verification)
python query.py --sandbox keywords "test"
```

Script locations: `E:\Dev\KarstensWorkspace\.devin\skills\seo-tools\dataforseo\`
