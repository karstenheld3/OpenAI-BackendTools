# INFO: OpenAI API - Authentication

**Doc ID**: OAIAPI-IN03
**Goal**: Document API key authentication and authorization headers
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The OpenAI API uses API keys for authentication, provided via HTTP Bearer authentication in the `Authorization` header. API keys are secrets that must never be exposed in client-side code, version control, or shared publicly. Keys should be loaded from environment variables or secure key management services. For users belonging to multiple organizations or accessing projects through legacy user API keys, additional headers (`OpenAI-Organization` and `OpenAI-Project`) can specify which organization and project to use for billing and access control. Organization IDs are found in organization settings, while Project IDs are found in project-specific settings. All API usage counts against the specified organization and project's quota.

## Key Facts

- **Authentication method**: HTTP Bearer token [VERIFIED]
- **Header name**: `Authorization: Bearer $OPENAI_API_KEY` [VERIFIED]
- **Organization header**: `OpenAI-Organization: $ORGANIZATION_ID` (optional) [VERIFIED]
- **Project header**: `OpenAI-Project: $PROJECT_ID` (optional) [VERIFIED]
- **Key management**: https://platform.openai.com/settings/organization/api-keys [VERIFIED]

## Use Cases

- **Single organization**: Use API key only, org is inferred
- **Multiple organizations**: Add `OpenAI-Organization` header to select org
- **Project isolation**: Add `OpenAI-Project` header to scope usage to project
- **Service accounts**: Use project-specific service account keys

## Quick Reference

### Required Header

```
Authorization: Bearer OPENAI_API_KEY
```

### Optional Headers

- `OpenAI-Organization` - Specify organization for multi-org users
- `OpenAI-Project` - Specify project for usage tracking and access control

### Key Types

- **User API keys** - Legacy, associated with user account
- **Project API keys** - Scoped to specific project (recommended)
- **Service account keys** - For automated systems
- **Admin API keys** - For organization administration

## Request Examples

### Basic Authentication (cURL)

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### With Organization and Project (cURL)

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "OpenAI-Organization: $ORGANIZATION_ID" \
  -H "OpenAI-Project: $PROJECT_ID"
```

### Python

```python
from openai import OpenAI

# Using environment variable (recommended)
client = OpenAI()  # Uses OPENAI_API_KEY env var

# Explicit key (not recommended for production)
client = OpenAI(api_key="sk-...")

# With organization
client = OpenAI(organization="org-...")
```

### TypeScript/Node.js

```typescript
import OpenAI from "openai";

// Using environment variable
const client = new OpenAI();

// With explicit configuration
const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
  organization: "org-...",
  project: "proj-...",
});
```

## Error Codes

- `401 Unauthorized` - Invalid API key, expired key, or missing Authorization header
- `403 Forbidden` - Valid key but lacks permission for requested resource
- `429 Too Many Requests` - Rate limit exceeded for organization/project

## Security Best Practices

- **Never hardcode keys** - Use environment variables or secret managers
- **Never expose in client-side code** - Keys should only be used server-side
- **Rotate keys regularly** - Revoke and regenerate keys periodically
- **Use project-scoped keys** - Minimize blast radius of key compromise
- **Monitor usage** - Check usage dashboard for anomalies

## Limitations and Known Issues

- **[COMMUNITY: OAIAPI-IN01-SC-SO-AUTH]** - Authentication errors can occur if API key format is incorrect or contains extra whitespace
- **Legacy user keys** - Being phased out in favor of project API keys

## Related Endpoints

- `_INFO_OAIAPI_ADMINISTRATION.md` - Admin API key management
- `_INFO_OAIAPI_PROJECT_API_KEYS.md` - Project-scoped API keys
- `_INFO_OAIAPI_PROJECT_SERVICE_ACCOUNTS.md` - Service accounts

## Sources

- OAIAPI-IN01-SC-OAI-AUTH - Official authentication documentation
- OAIAPI-IN01-SC-SO-AUTH - Stack Overflow authentication issues

## Document History

**[2026-01-30 09:25]**
- Initial documentation created from API reference
