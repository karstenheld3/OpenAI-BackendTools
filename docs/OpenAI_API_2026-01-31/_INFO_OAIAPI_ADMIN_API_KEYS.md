# INFO: OpenAI API - Admin API Keys

**Doc ID**: OAIAPI-IN60
**Goal**: Document Admin API Keys API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

Admin API Keys are elevated-privilege keys for organization management. They provide access to all administration endpoints and can be created, listed, and deleted.

## Key Facts

- **Privileges**: Full admin access [VERIFIED]
- **Creation**: Via dashboard or API [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/admin_api_keys` - Create key
- `GET /v1/organization/admin_api_keys` - List keys
- `GET /v1/organization/admin_api_keys/{key_id}` - Get key
- `DELETE /v1/organization/admin_api_keys/{key_id}` - Delete key

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Existing admin API key

# Create new admin key
key = client.organization.admin_api_keys.create(
    name="Automation Admin Key"
)

# Save the key value securely - only shown once!
print(f"New key: {key.value}")

# List admin keys
keys = client.organization.admin_api_keys.list()

# Delete key
client.organization.admin_api_keys.delete("key_abc123")
```

## Sources

- OAIAPI-IN01-SC-OAI-ADMKEY - Official admin API keys documentation

## Document History

**[2026-01-30 11:40]**
- Initial documentation created
