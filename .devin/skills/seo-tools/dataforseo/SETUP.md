# DataForSEO Setup

## Prerequisites

- Account at https://app.dataforseo.com ($50 minimum deposit)
- PowerShell 7+ or Python 3.10+

## Credentials

1. Go to https://app.dataforseo.com/api-access
2. API login = registration email
3. API password = auto-generated (NOT account password)
4. Base64 = `login:password` encoded in Base64

Stored in: `E:\Dev\.tools\.api-keys.txt`
```
DATAFORSEO_LOGIN=your_email@example.com
DATAFORSEO_PASSWORD=your_api_password
DATAFORSEO_BASE64=base64_encoded_login:password
```

## Authentication Method

Basic HTTP Auth. Include in every request:
```
Authorization: Basic {DATAFORSEO_BASE64}
```

No OAuth. No token refresh. No expiry. Credentials valid until password is reset in dashboard.

## Verify Connection

PowerShell:
```powershell
$base64 = (Get-Content "E:\Dev\.tools\.api-keys.txt" | Where-Object { $_ -match "^DATAFORSEO_BASE64=" }) -replace "DATAFORSEO_BASE64=", ""
$headers = @{ Authorization = "Basic $base64" }
$result = Invoke-RestMethod -Uri "https://api.dataforseo.com/v3/appendix/user_data" -Headers $headers
Write-Host "Balance: $($result.tasks[0].result[0].money.balance)"
```

Expected: `Balance: 51` (or current balance > 0)

Python:
```python
import requests, os

api_keys = {}
with open(r"E:\Dev\.tools\.api-keys.txt") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            api_keys[k] = v

headers = {"Authorization": f"Basic {api_keys['DATAFORSEO_BASE64']}"}
r = requests.get("https://api.dataforseo.com/v3/appendix/user_data", headers=headers)
print(f"Balance: {r.json()['tasks'][0]['result'][0]['money']['balance']}")
```

## MCP Server Config

Add to `~/.codeium/windsurf/mcp_config.json`:
```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "npx",
      "args": ["-y", "@anthropic/dataforseo-mcp"],
      "env": {
        "DATAFORSEO_LOGIN": "your_email@example.com",
        "DATAFORSEO_PASSWORD": "your_api_password"
      }
    }
  }
}
```

Note: Verify exact MCP package name before installing. Alternative: use scripts directly (no MCP dependency).

## IP Whitelisting (Optional)

Dashboard > API Access > IP Access section. Leave empty for access from any IP. Add specific IPs only if running from fixed servers.

## Key Facts

- Base URL: `https://api.dataforseo.com/v3/`
- Auth: Basic HTTP (login:password Base64)
- Encoding: UTF-8 request, gzip response
- Format: JSON default, XML (append `.xml`), HTML (append `.html`)
- Rate limits: per-endpoint, check `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers
- Results storage: 30 days (Standard/task_post), not stored (Live)
- Minimum deposit: $50 (credits roll over indefinitely)
- No subscription, no monthly fee
