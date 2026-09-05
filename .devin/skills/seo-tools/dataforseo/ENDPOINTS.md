# DataForSEO Endpoints Reference

Base URL: `https://api.dataforseo.com/v3/`

All endpoints require `Authorization: Basic {DATAFORSEO_BASE64}` header.

## Request Patterns

- **task_post** - Submit task, get task_id, retrieve later. Cheaper ($0.0006). Async.
- **live** - Submit and get results immediately. More expensive ($0.002). Sync.
- **task_get/{id}** - Retrieve completed task results. Free (included in task_post cost).

## SERP API

Endpoint: `/v3/serp/google/organic/`

### Live Advanced (real-time SERP)
```
POST /v3/serp/google/organic/live/advanced
{
  "keyword": "AI compliance software",
  "location_code": 2276,
  "language_code": "en",
  "device": "desktop",
  "load_async_ai_overview": true
}
```
Cost: $0.002/task. Returns: organic results, featured snippets, People Also Ask, AI Overview.

### Task Post (queued, cheaper)
```
POST /v3/serp/google/organic/task_post
[{
  "keyword": "regulatory change management",
  "location_code": 2276,
  "language_code": "en",
  "tag": "my_research"
}]
```
Cost: $0.0006/task. Poll with: `GET /v3/serp/google/organic/task_get/advanced/{task_id}`

### SERP Screenshots
```
POST /v3/serp/screenshot
{"url": "https://www.google.com/search?q=...", "full_page": true}
```

## Keywords Data API

### Search Volume
```
POST /v3/keywords_data/google_ads/search_volume/live
[{
  "keywords": ["AI compliance", "DORA automation", "regulatory reporting software"],
  "location_code": 2276,
  "language_code": "en"
}]
```
Cost: $0.0006/keyword. Returns: monthly_searches, competition, cpc, search_volume trends.
Max 700 keywords per request.

### Keywords for Site
```
POST /v3/keywords_data/google_ads/keywords_for_site/live
[{
  "target": "competitor-domain.com",
  "location_code": 2276,
  "language_code": "en"
}]
```
Cost: $0.0006/task. Returns keywords the domain likely targets.

### Keywords for Keywords (related)
```
POST /v3/keywords_data/google_ads/keywords_for_keywords/live
[{
  "keywords": ["compliance automation"],
  "location_code": 2276,
  "language_code": "en"
}]
```

## DataForSEO Labs API

### Keyword Suggestions
```
POST /v3/dataforseo_labs/google/keyword_suggestions/live
[{
  "keyword": "AI compliance",
  "location_code": 2276,
  "language_code": "en",
  "limit": 100,
  "include_seed_keyword": true
}]
```
Cost: $0.0006/task. Returns: keyword + volume + difficulty + cpc + competition + intent.

### Keyword Ideas (broader)
```
POST /v3/dataforseo_labs/google/keyword_ideas/live
[{
  "keywords": ["compliance", "regulatory", "fintech"],
  "location_code": 2276,
  "language_code": "en",
  "limit": 200
}]
```

### Competitors Domain
```
POST /v3/dataforseo_labs/google/competitors_domain/live
[{
  "target": "yourdomain.com",
  "location_code": 2276,
  "language_code": "en",
  "limit": 20
}]
```
Returns domains competing for same keywords.

### SERP Competitors
```
POST /v3/dataforseo_labs/google/serp_competitors/live
[{
  "keywords": ["AI compliance finance", "DORA automation"],
  "location_code": 2276,
  "language_code": "en"
}]
```
Returns who ranks for these specific keywords.

### Domain Rank Overview
```
POST /v3/dataforseo_labs/google/domain_rank_overview/live
[{
  "target": "competitor.com",
  "location_code": 2276,
  "language_code": "en"
}]
```
Returns: organic traffic estimate, keyword count, backlinks, rank.

### Relevant Pages
```
POST /v3/dataforseo_labs/google/relevant_pages/live
[{
  "target": "competitor.com",
  "location_code": 2276,
  "language_code": "en",
  "limit": 50
}]
```
Returns top-performing pages for a domain.

## AI Optimization API (GEO)

### LLM Mentions (track brand in AI responses)
```
POST /v3/ai_optimization/llm_mentions/task_post
[{
  "keyword": "best compliance automation software",
  "target": "yourdomain.com",
  "llm_type": "chatgpt"
}]
```
LLM types: `chatgpt`, `claude`, `gemini`, `perplexity`

### AI Keyword Data
```
POST /v3/ai_optimization/ai_keyword_data/live
[{
  "keywords": ["compliance automation", "regulatory AI"],
  "location_code": 2276,
  "language_code": "en"
}]
```
Returns AI-specific keyword metrics (how keywords perform in LLM contexts).

## Backlinks API

### Summary
```
POST /v3/backlinks/summary/live
[{"target": "competitor.com", "internal_list_limit": 10, "external_list_limit": 10}]
```
Cost: $0.002/task. Returns: total backlinks, referring domains, rank, broken links.

### Domain Intersection (Link Gap)
```
POST /v3/backlinks/domain_intersection/live
[{
  "targets": {"1": "yourdomain.com", "2": "competitor1.com", "3": "competitor2.com"},
  "exclude_targets": ["1"]
}]
```
Returns domains linking to competitors but NOT to you. Critical for link building strategy.

### Competitors
```
POST /v3/backlinks/competitors/live
[{"target": "yourdomain.com"}]
```
Returns domains with similar backlink profiles.

## Appendix (Utility - Free)

### Check Balance
```
GET /v3/appendix/user_data
```

### Location Codes
```
GET /v3/appendix/locations
```
Key codes: 2276 (Germany), 2840 (US), 2826 (UK), 2250 (France), 2756 (Switzerland), 2040 (Austria)

### Language Codes
```
GET /v3/appendix/languages
```
Key codes: "en", "de", "fr", "es", "pt"

## Cost Summary

- **SERP** - Standard: $0.0006/task, Live: $0.002/task
- **Keywords Data** - $0.0006/keyword (same for standard and live)
- **Labs** - $0.0006/task (same for standard and live)
- **AI Optimization** - varies per task
- **Backlinks** - $0.002/task (same for standard and live)
- **OnPage** - $0.002/task (same for standard and live)
- **Appendix** - free

Typical session (50 keyword research + 10 SERP checks + 1 competitor analysis):
$0.0006 * 50 + $0.002 * 10 + $0.0006 * 1 = $0.03 + $0.02 + $0.0006 = ~$0.05 per session
