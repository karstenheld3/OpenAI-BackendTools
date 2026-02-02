# INFO: OpenAI API - Error Handling

**Doc ID**: OAIAPI-IN13
**Goal**: Document error codes, types, and handling strategies
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The OpenAI API returns standard HTTP status codes and structured JSON error objects to communicate failures. Common errors include authentication failures (401), invalid requests (400), rate limiting (429), and server errors (500). The Python SDK provides typed exceptions for each error category, enabling precise error handling. Best practices include implementing exponential backoff for retryable errors, validating inputs before requests, and logging request IDs for debugging. Error responses include a message, type, param (if applicable), and code for programmatic handling.

## Key Facts

- **Error format**: JSON with `error` object [VERIFIED]
- **Error fields**: `message`, `type`, `param`, `code` [VERIFIED]
- **Retryable errors**: 429, 500, 502, 503, 504 [VERIFIED]
- **Non-retryable**: 400, 401, 403, 404 [VERIFIED]

## Error Response Format

```json
{
  "error": {
    "message": "Human-readable error description",
    "type": "error_type",
    "param": "parameter_name",
    "code": "error_code"
  }
}
```

## HTTP Status Codes

### 4xx Client Errors

| Code | Name | Cause | Action |
|------|------|-------|--------|
| 400 | Bad Request | Invalid parameters, malformed JSON | Fix request |
| 401 | Unauthorized | Invalid/missing API key | Check API key |
| 403 | Forbidden | No access to resource | Check permissions |
| 404 | Not Found | Resource doesn't exist | Check ID/endpoint |
| 409 | Conflict | Concurrent modification conflict | Retry with backoff |
| 422 | Unprocessable Entity | Semantic error in request | Fix content |
| 429 | Too Many Requests | Rate limit exceeded | Wait and retry |

### 5xx Server Errors

| Code | Name | Cause | Action |
|------|------|-------|--------|
| 500 | Internal Server Error | OpenAI server issue | Retry with backoff |
| 502 | Bad Gateway | Upstream server issue | Retry with backoff |
| 503 | Service Unavailable | Temporary overload | Retry with backoff |
| 504 | Gateway Timeout | Request timeout | Retry with backoff |

## Common Error Types

- `invalid_request_error` - Malformed request or invalid parameters
- `authentication_error` - Invalid API key
- `permission_error` - Insufficient permissions
- `not_found_error` - Resource not found
- `rate_limit_error` - Rate limit exceeded
- `api_error` - OpenAI server error
- `timeout_error` - Request timed out

## Python SDK Exceptions

```python
from openai import (
    OpenAI,
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
    BadRequestError,
    NotFoundError,
    PermissionDeniedError,
    UnprocessableEntityError,
)

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded - implement backoff")
except BadRequestError as e:
    print(f"Invalid request: {e.message}")
except NotFoundError:
    print("Model or resource not found")
except PermissionDeniedError:
    print("No permission to access this resource")
except APIConnectionError:
    print("Network connectivity issue")
except APIError as e:
    print(f"OpenAI API error: {e.status_code}")
```

## Error Handling Patterns

### Comprehensive Handler

```python
import time
from openai import OpenAI, APIError, RateLimitError, APIConnectionError

client = OpenAI()

def robust_completion(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError:
            wait = 2 ** attempt
            print(f"Rate limited. Retrying in {wait}s...")
            time.sleep(wait)
        except APIConnectionError:
            print("Connection error. Retrying...")
            time.sleep(1)
        except APIError as e:
            if e.status_code >= 500:
                wait = 2 ** attempt
                print(f"Server error {e.status_code}. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                raise  # Non-retryable error
    
    raise Exception("Max retries exceeded")
```

### TypeScript/Node.js

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function robustCompletion(prompt: string): Promise<string> {
  const maxRetries = 3;
  
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await client.chat.completions.create({
        model: "gpt-4o",
        messages: [{ role: "user", content: prompt }],
      });
      return response.choices[0].message.content || "";
    } catch (error) {
      if (error instanceof OpenAI.RateLimitError) {
        const wait = Math.pow(2, attempt) * 1000;
        console.log(`Rate limited. Retrying in ${wait}ms...`);
        await new Promise(r => setTimeout(r, wait));
      } else if (error instanceof OpenAI.APIError && error.status >= 500) {
        const wait = Math.pow(2, attempt) * 1000;
        console.log(`Server error. Retrying in ${wait}ms...`);
        await new Promise(r => setTimeout(r, wait));
      } else {
        throw error;
      }
    }
  }
  throw new Error("Max retries exceeded");
}
```

## Specific Error Scenarios

### Token Limit Exceeded

```json
{
  "error": {
    "message": "This model's maximum context length is 128000 tokens. However, your messages resulted in 150000 tokens.",
    "type": "invalid_request_error",
    "param": "messages",
    "code": "context_length_exceeded"
  }
}
```

**Solution**: Reduce input length or use a model with larger context.

### Invalid Model

```json
{
  "error": {
    "message": "The model 'gpt-5-turbo' does not exist",
    "type": "invalid_request_error",
    "param": "model",
    "code": "model_not_found"
  }
}
```

**Solution**: Check model name spelling and availability.

### Content Filter

```json
{
  "error": {
    "message": "Your request was rejected as a result of our safety system.",
    "type": "invalid_request_error",
    "code": "content_policy_violation"
  }
}
```

**Solution**: Modify content to comply with usage policies.

## Limitations and Known Issues

- **[COMMUNITY: OAIAPI-IN01-SC-SO-AUTH]** - Authentication errors can occur from whitespace in API keys
- **[COMMUNITY: OAIAPI-IN01-SC-SO-400]** - 400 errors may lack specific param info for complex requests

## Gotchas and Quirks

- `param` field is null for many errors
- Rate limit 429 can mean billing issue, not just quota
- Streaming errors may occur mid-stream
- Request ID in headers even on errors - log for support

## Related Endpoints

- `_INFO_OAIAPI_DEBUGGING.md` - Request ID logging
- `_INFO_OAIAPI_RATE_LIMITS.md` - Rate limit handling

## Sources

- OAIAPI-IN01-SC-OAI-ERRCODES - Official error codes
- OAIAPI-IN01-SC-SO-ERRHNDL - Error handling patterns
- OAIAPI-IN01-SC-SO-400 - Bad request troubleshooting

## Document History

**[2026-01-30 09:50]**
- Initial documentation created with community insights
