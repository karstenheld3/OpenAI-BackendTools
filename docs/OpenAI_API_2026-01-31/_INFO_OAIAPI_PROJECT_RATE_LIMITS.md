# INFO: OpenAI API - Project Rate Limits

**Doc ID**: OAIAPI-IN59
**Goal**: Document Project Rate Limits API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_PROJECTS.md [OAIAPI-IN33]` for context

## Summary

Project Rate Limits enables custom rate limit configuration per project. Override organization defaults for specific projects to allocate capacity.

## Key Facts

- **Customization**: Per-project rate limits [VERIFIED]
- **Limits**: RPM, TPM, RPD per model [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/organization/projects/{project_id}/rate_limits` - List limits
- `POST /v1/organization/projects/{project_id}/rate_limits/{id}` - Update limit

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

# Get current limits
limits = client.organization.projects.rate_limits.list(
    project_id="proj_abc123"
)

for limit in limits.data:
    print(f"{limit.model}: {limit.max_requests_per_minute} RPM")

# Update limit
client.organization.projects.rate_limits.update(
    project_id="proj_abc123",
    rate_limit_id="rl_xyz",
    max_requests_per_minute=1000,
    max_tokens_per_minute=100000
)
```

## Sources

- OAIAPI-IN01-SC-OAI-PROJRL - Official project rate limits documentation

## Document History

**[2026-01-30 11:40]**
- Initial documentation created
