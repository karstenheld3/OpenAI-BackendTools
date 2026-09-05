# Google Search Console MCP Setup

## Prerequisites

- Google Cloud project (free)
- GSC property verified for your domain
- Node.js 18+ (for MCP server via npx)

## Authentication

GSC uses OAuth 2.0 via service account (one-time setup, MCP handles refresh):

1. Go to https://console.cloud.google.com/
2. Create project (or use existing)
3. Enable "Search Console API"
4. Create service account: IAM > Service Accounts > Create
5. Download JSON key file
6. In GSC (https://search.google.com/search-console/): Settings > Users > Add user
7. Add service account email as Owner

Store JSON key at: `E:\Dev\.tools\gsc-service-account.json`

## MCP Server Options

### Option A: serpfire/gsc-mcp-server (recommended)
SQLite cache, 20+ analysis tools, content decay detection.
```json
{
  "mcpServers": {
    "gsc": {
      "command": "npx",
      "args": ["-y", "@serpfire/gsc-mcp-server"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "E:\\Dev\\.tools\\gsc-service-account.json",
        "GSC_PROPERTY": "https://yourdomain.com/"
      }
    }
  }
}
```

### Option B: AminForou/mcp-gsc (most starred)
1.1k stars, 20 tools, multi-property support.
```json
{
  "mcpServers": {
    "gsc": {
      "command": "npx",
      "args": ["-y", "mcp-gsc"],
      "env": {
        "GOOGLE_APPLICATION_CREDENTIALS": "E:\\Dev\\.tools\\gsc-service-account.json"
      }
    }
  }
}
```

## Verify Connection

After MCP config, restart Windsurf/Claude. Test by asking:
"Check GSC for quick wins on yourdomain.com"

Expected: Tool call to `quick_wins` returning keywords at positions 4-15.

## Key MCP Tools

- `quick_wins` - Keywords at positions 4-15 with high impressions
- `ctr_opportunities` - High impressions, low CTR pages
- `traffic_drops` - Diagnose ranking loss vs CTR collapse
- `content_decay` - Pages declining 3 consecutive periods
- `cannibalization_check` - Keywords with multiple competing pages
- `content_gaps` - Search demand without targeting content
- `submit_url` - Submit to Google Indexing API

## Key Facts

- Free (no billing required for Search Console API)
- OAuth handled by MCP server (no manual token management)
- One-time setup: ~15 minutes
- Data delay: GSC data is 2-3 days behind real-time
- Property types: Domain property (covers all subdomains) vs URL prefix
