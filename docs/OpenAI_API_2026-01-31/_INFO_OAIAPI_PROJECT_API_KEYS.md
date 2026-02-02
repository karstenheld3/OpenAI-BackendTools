# INFO: OpenAI API - Project API Keys

**Doc ID**: OAIAPI-IN58
**Goal**: Document Project API Keys API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_PROJECTS.md [OAIAPI-IN33]` for context

## Summary

Project API Keys manages API keys scoped to specific projects. Keys can be listed and deleted but not created via API (use service accounts or dashboard).

## Key Facts

- **Scope**: Project-level API keys [VERIFIED]
- **Management**: List and delete only via API [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/organization/projects/{project_id}/api_keys` - List keys
- `GET /v1/organization/projects/{project_id}/api_keys/{key_id}` - Get key
- `DELETE /v1/organization/projects/{project_id}/api_keys/{key_id}` - Delete key

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

# List project API keys
keys = client.organization.projects.api_keys.list(
    project_id="proj_abc123"
)

for key in keys.data:
    print(f"{key.id}: {key.name} (last used: {key.last_used_at})")

# Delete key
client.organization.projects.api_keys.delete(
    project_id="proj_abc123",
    key_id="key_xyz789"
)
```

## Sources

- OAIAPI-IN01-SC-OAI-PROJKEY - Official project API keys documentation

## Document History

**[2026-01-30 11:40]**
- Initial documentation created
