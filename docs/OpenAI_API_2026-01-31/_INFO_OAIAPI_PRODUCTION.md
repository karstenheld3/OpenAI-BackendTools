# INFO: OpenAI API - Production Best Practices

**Doc ID**: OAIAPI-IN14
**Goal**: Document production deployment best practices
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

Deploying OpenAI API in production requires careful attention to security, reliability, and cost management. Key practices include secure API key management using environment variables or secret managers, implementing proper error handling with exponential backoff, monitoring usage and costs, and setting up organization structure with projects for access control. Safety best practices include content moderation, rate limiting user inputs, and implementing guardrails. Production systems should log request IDs for debugging, use pinned model versions for consistency, and implement fallback strategies for high availability.

## Key Facts

- **API key security**: Never expose in client-side code [VERIFIED]
- **Model pinning**: Use versioned models (e.g., `gpt-4o-2024-08-06`) [VERIFIED]
- **Request logging**: Log `x-request-id` for debugging [VERIFIED]
- **Moderation**: Free for monitoring OpenAI API content [VERIFIED]

## Security Best Practices

### API Key Management

- Store keys in environment variables or secret managers
- Never commit keys to version control
- Use project-scoped keys instead of user keys
- Rotate keys periodically
- Set up key rotation procedures

```python
import os
from openai import OpenAI

# Good: Use environment variable
client = OpenAI()  # Uses OPENAI_API_KEY

# Good: Use secret manager
from azure.keyvault.secrets import SecretClient
key = secret_client.get_secret("openai-api-key").value
client = OpenAI(api_key=key)

# BAD: Hardcoded key
# client = OpenAI(api_key="sk-...")  # NEVER do this
```

### Access Control

- Create separate projects for different environments (dev, staging, prod)
- Use service accounts for automated systems
- Implement least-privilege access
- Monitor usage per project

## Reliability Best Practices

### Error Handling

```python
from openai import OpenAI, RateLimitError, APIError
import time

client = OpenAI()

def reliable_completion(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4o-2024-08-06",  # Pinned version
                messages=[{"role": "user", "content": prompt}],
                timeout=30.0
            )
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except APIError as e:
            if e.status_code >= 500:
                time.sleep(2 ** attempt)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Request Logging

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Log for debugging with OpenAI support
print(f"Request ID: {response._request_id}")
```

### Timeout Configuration

```python
from openai import OpenAI

# Set reasonable timeouts
client = OpenAI(
    timeout=60.0,  # 60 second timeout
    max_retries=2  # Built-in retry
)
```

## Safety Best Practices

### Input Moderation

```python
from openai import OpenAI

client = OpenAI()

def safe_completion(user_input):
    # Check input before processing
    moderation = client.moderations.create(input=user_input)
    
    if moderation.results[0].flagged:
        return "I cannot process this request."
    
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_input}]
    )
```

### Output Moderation

```python
def moderated_completion(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    
    output = response.choices[0].message.content
    
    # Check output before returning
    moderation = client.moderations.create(input=output)
    
    if moderation.results[0].flagged:
        return "Response filtered for safety."
    
    return output
```

### Rate Limiting Users

```python
from collections import defaultdict
import time

user_requests = defaultdict(list)
RATE_LIMIT = 10  # requests per minute

def check_user_rate_limit(user_id):
    now = time.time()
    minute_ago = now - 60
    
    # Clean old requests
    user_requests[user_id] = [
        t for t in user_requests[user_id] if t > minute_ago
    ]
    
    if len(user_requests[user_id]) >= RATE_LIMIT:
        return False
    
    user_requests[user_id].append(now)
    return True
```

## Cost Management

### Monitor Usage

- Set up usage alerts in OpenAI dashboard
- Track costs per project
- Use `usage` field in responses for tracking

```python
total_tokens = 0

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}]
)

total_tokens += response.usage.total_tokens
print(f"Total tokens used: {total_tokens}")
```

### Optimize Costs

- Use smaller models when appropriate (gpt-4o-mini)
- Cache common responses
- Use Batch API for 50% discount on async workloads
- Set `max_tokens` to prevent runaway costs

## Organization Setup

### Project Structure

```
Organization
├── Production Project
│   ├── Service Account (backend)
│   └── Rate limits: High
├── Staging Project
│   ├── Service Account (CI/CD)
│   └── Rate limits: Medium
└── Development Project
    ├── Developer keys
    └── Rate limits: Low
```

### Service Accounts

- Create dedicated service accounts for each application
- Use project-scoped API keys
- Don't share keys between environments

## Monitoring Checklist

- [ ] Request ID logging enabled
- [ ] Error rate monitoring
- [ ] Latency tracking
- [ ] Token usage tracking
- [ ] Cost alerts configured
- [ ] Rate limit monitoring
- [ ] Moderation flagging rates

## Related Endpoints

- `_INFO_OAIAPI_AUTHENTICATION.md` - API key setup
- `_INFO_OAIAPI_RATE_LIMITS.md` - Rate limiting
- `_INFO_OAIAPI_ERROR_HANDLING.md` - Error handling
- `_INFO_OAIAPI_MODERATIONS.md` - Content moderation

## Sources

- OAIAPI-IN01-SC-OAI-PRODBP - Production best practices
- OAIAPI-IN01-SC-OAI-SAFETY - Safety best practices

## Document History

**[2026-01-30 09:55]**
- Initial documentation created
