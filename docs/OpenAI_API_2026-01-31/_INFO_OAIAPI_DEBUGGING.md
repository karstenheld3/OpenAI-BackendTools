# INFO: OpenAI API - Debugging Requests

**Doc ID**: OAIAPI-IN04
**Goal**: Document request tracing, response headers, and troubleshooting
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The OpenAI API provides comprehensive debugging capabilities through HTTP response headers that include request identifiers, processing metrics, and rate limit information. The `x-request-id` header contains a unique identifier for each API request, essential for troubleshooting with OpenAI support. Clients can also supply their own request ID via the `X-Client-Request-Id` request header for custom tracing and correlation. Rate limit headers provide real-time information about quota consumption and reset times. OpenAI strongly recommends logging request IDs in production deployments to facilitate efficient debugging. Official SDKs expose the request ID through response object properties.

## Key Facts

- **Server request ID**: `x-request-id` response header [VERIFIED]
- **Client request ID**: `X-Client-Request-Id` request header (optional) [VERIFIED]
- **Max client ID length**: 512 ASCII characters [VERIFIED]
- **Processing time**: `openai-processing-ms` header [VERIFIED]
- **API version**: `openai-version` header (currently `2020-10-01`) [VERIFIED]

## Use Cases

- **Support tickets**: Provide `x-request-id` when contacting OpenAI support
- **Distributed tracing**: Use `X-Client-Request-Id` to correlate with your trace IDs
- **Performance monitoring**: Track `openai-processing-ms` for latency analysis
- **Rate limit management**: Monitor rate limit headers to avoid 429 errors

## Quick Reference

### API Meta Headers (Response)

- `openai-organization` - Organization associated with the request
- `openai-processing-ms` - Server-side processing time in milliseconds
- `openai-version` - REST API version (currently `2020-10-01`)
- `x-request-id` - Unique request identifier for troubleshooting

### Rate Limit Headers (Response)

- `x-ratelimit-limit-requests` - Maximum requests allowed
- `x-ratelimit-limit-tokens` - Maximum tokens allowed
- `x-ratelimit-remaining-requests` - Requests remaining in window
- `x-ratelimit-remaining-tokens` - Tokens remaining in window
- `x-ratelimit-reset-requests` - Time until request limit resets
- `x-ratelimit-reset-tokens` - Time until token limit resets

### Client Request ID (Request)

- `X-Client-Request-Id` - Your custom identifier (max 512 ASCII chars)

## Request Examples

### Sending Custom Request ID (cURL)

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "X-Client-Request-Id: 123e4567-e89b-12d3-a456-426614174000" \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Logging Request ID (Python)

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Access request ID from response
print(f"Request ID: {response._request_id}")
```

### Logging Request ID (TypeScript)

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function main() {
  const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Hello" }],
  });
  
  // Access request ID from response headers
  console.log(`Request ID: ${response._request_id}`);
}
```

## X-Client-Request-Id Rules

- Must contain only ASCII characters
- Maximum 512 characters
- Should be unique per request (UUID recommended)
- Requests with invalid format return 400 error
- Logged by OpenAI for supported endpoints (chat/completions, embeddings, responses, etc.)
- Useful for timeout/network error debugging when server response is unavailable

## Error Codes

- `400 Bad Request` - Invalid `X-Client-Request-Id` format (non-ASCII or >512 chars)

## Gotchas and Quirks

- `openai-processing-ms` measures server-side time only, not network latency
- Rate limit headers may not be present on all endpoints
- `x-request-id` format is opaque and may change

## Related Endpoints

- `_INFO_OAIAPI_RATE_LIMITS.md` - Rate limiting details
- `_INFO_OAIAPI_ERROR_HANDLING.md` - Error code reference

## Sources

- OAIAPI-IN01-SC-OAI-DEBUG - Official debugging documentation

## Document History

**[2026-01-30 09:25]**
- Initial documentation created from API reference
