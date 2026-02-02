# INFO: OpenAI API - Rate Limits

**Doc ID**: OAIAPI-IN12
**Goal**: Document rate limiting system, tiers, and handling strategies
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

OpenAI enforces rate limits to ensure fair access and API stability. Limits are applied at organization and project levels, measured in requests per minute (RPM), tokens per minute (TPM), and requests per day (RPD). Different models have different limits, and limits increase as organizations move through usage tiers (Free, Tier 1-5). Rate limit information is returned in response headers, enabling proactive management. When limits are exceeded, the API returns HTTP 429 errors. Strategies for handling rate limits include exponential backoff, request batching, and using the Batch API for non-time-sensitive workloads. Project-level rate limits can be customized via the Administration API.

## Key Facts

- **Limit types**: RPM (requests), TPM (tokens), RPD (requests/day) [VERIFIED]
- **Scope**: Organization and project level [VERIFIED]
- **HTTP error**: 429 Too Many Requests [VERIFIED]
- **Headers**: `x-ratelimit-*` in responses [VERIFIED]
- **Tiers**: Free, Tier 1, Tier 2, Tier 3, Tier 4, Tier 5 [VERIFIED]

## Use Cases

- **Capacity planning**: Understand limits before scaling
- **Error handling**: Implement retry logic for 429 errors
- **Optimization**: Batch requests to stay within limits
- **Cost management**: Use Batch API for 50% discount and higher limits

## Quick Reference

### Rate Limit Headers

- `x-ratelimit-limit-requests` - Max requests in window
- `x-ratelimit-limit-tokens` - Max tokens in window
- `x-ratelimit-remaining-requests` - Requests remaining
- `x-ratelimit-remaining-tokens` - Tokens remaining
- `x-ratelimit-reset-requests` - Time until request limit resets
- `x-ratelimit-reset-tokens` - Time until token limit resets

### Usage Tiers

| Tier | Qualification | Typical Limits |
|------|--------------|----------------|
| Free | New accounts | 3 RPM, 200 RPD |
| Tier 1 | $5+ paid | 500 RPM, 10K TPM |
| Tier 2 | $50+ paid, 7+ days | 5K RPM, 100K TPM |
| Tier 3 | $100+ paid, 7+ days | 5K RPM, 200K TPM |
| Tier 4 | $250+ paid, 14+ days | 10K RPM, 300K TPM |
| Tier 5 | $1000+ paid, 30+ days | Contact for custom |

*Limits vary by model - check dashboard for current limits*

### Model-Specific Limits

Different models have different limits:
- **gpt-4o**: Higher TPM than gpt-4
- **gpt-4o-mini**: Highest TPM among GPT models
- **Embeddings**: Very high TPM (1M+)
- **Reasoning models**: Lower limits due to compute

## Rate Limit Headers Example

```
x-ratelimit-limit-requests: 10000
x-ratelimit-remaining-requests: 9999
x-ratelimit-reset-requests: 6ms
x-ratelimit-limit-tokens: 100000
x-ratelimit-remaining-tokens: 99984
x-ratelimit-reset-tokens: 9ms
```

## Handling Strategies

### Exponential Backoff (Python)

```python
import time
import random
from openai import OpenAI, RateLimitError

client = OpenAI()

def make_request_with_retry(prompt, max_retries=5):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited. Waiting {wait:.1f}s...")
            time.sleep(wait)
```

### Using Tenacity Library

```python
from tenacity import retry, wait_exponential, retry_if_exception_type
from openai import OpenAI, RateLimitError

client = OpenAI()

@retry(
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type(RateLimitError)
)
def make_request(prompt):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
```

### Proactive Rate Limiting

```python
import time
from openai import OpenAI

client = OpenAI()

def rate_limited_requests(prompts, requests_per_minute=50):
    delay = 60.0 / requests_per_minute
    results = []
    
    for prompt in prompts:
        start = time.time()
        result = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        results.append(result)
        
        elapsed = time.time() - start
        if elapsed < delay:
            time.sleep(delay - elapsed)
    
    return results
```

### Batch API for High Volume

```python
from openai import OpenAI

client = OpenAI()

# Upload JSONL file with requests
batch_file = client.files.create(
    file=open("requests.jsonl", "rb"),
    purpose="batch"
)

# Create batch job (50% cost savings, higher limits)
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h"
)
```

## Error Response

### 429 Too Many Requests

```json
{
  "error": {
    "message": "Rate limit reached for gpt-4o in organization org-xxx on requests per min. Limit: 500, Used: 500, Requested: 1.",
    "type": "rate_limit_error",
    "param": null,
    "code": "rate_limit_exceeded"
  }
}
```

## Limitations and Known Issues

- **[COMMUNITY: OAIAPI-IN01-SC-SO-429]** - 429 errors can occur from billing issues (no credits), not just rate limits
- **[COMMUNITY: OAIAPI-IN01-SC-GH-RATELIM]** - TPM limits can be hit even with low RPM due to large prompts
- **[COMMUNITY: OAIAPI-IN01-SC-GH-TPM937]** - Azure OpenAI has different rate limit headers

## Gotchas and Quirks

- Token limits include both input and output tokens
- Streaming requests count tokens as they're generated
- Reset times are relative (e.g., "6ms", "1s"), not absolute
- Different models share organization limits but have separate model limits
- Free tier has very restrictive limits

## Related Endpoints

- `_INFO_OAIAPI_DEBUGGING.md` - Rate limit headers
- `_INFO_OAIAPI_BATCH.md` - Batch API for high volume
- `_INFO_OAIAPI_PROJECT_RATE_LIMITS.md` - Custom project limits

## Sources

- OAIAPI-IN01-SC-OAI-RATELIM - Official rate limits guide
- OAIAPI-IN01-SC-SO-429 - 429 error troubleshooting
- OAIAPI-IN01-SC-GH-RATELIM - Rate limit handling cookbook

## Document History

**[2026-01-30 09:50]**
- Initial documentation created with community insights
