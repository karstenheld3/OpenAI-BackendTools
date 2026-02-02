# INFO: OpenAI API - Project Service Accounts

**Doc ID**: OAIAPI-IN57
**Goal**: Document Project Service Accounts API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_PROJECTS.md [OAIAPI-IN33]` for context

## Summary

Project Service Accounts are non-user identities for automated systems. They have their own API keys and are scoped to specific projects.

## Key Facts

- **Purpose**: Machine/automated access [VERIFIED]
- **Scope**: Project-level [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/projects/{project_id}/service_accounts` - Create
- `GET /v1/organization/projects/{project_id}/service_accounts` - List
- `GET /v1/organization/projects/{project_id}/service_accounts/{id}` - Get
- `DELETE /v1/organization/projects/{project_id}/service_accounts/{id}` - Delete

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

# Create service account
sa = client.organization.projects.service_accounts.create(
    project_id="proj_abc123",
    name="CI/CD Pipeline"
)

# Returns API key - save securely!
print(f"API Key: {sa.api_key.value}")
```

## Sources

- OAIAPI-IN01-SC-OAI-PROJSA - Official project service accounts documentation

## Document History

**[2026-01-30 11:35]**
- Initial documentation created
