# INFO: OpenAI API - Invites

**Doc ID**: OAIAPI-IN50
**Goal**: Document Invites API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

The Invites API manages organization membership invitations. Invitations are sent via email and can be tracked, resent, or deleted.

## Key Facts

- **Method**: Email-based invitations [VERIFIED]
- **Roles**: Assignable during invite [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/invites` - Create invite
- `GET /v1/organization/invites` - List invites
- `GET /v1/organization/invites/{id}` - Get invite
- `DELETE /v1/organization/invites/{id}` - Delete invite

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

invite = client.organization.invites.create(
    email="user@example.com",
    role="member"
)

# List pending invites
invites = client.organization.invites.list()
```

## Sources

- OAIAPI-IN01-SC-OAI-INVITE - Official invites documentation

## Document History

**[2026-01-30 11:25]**
- Initial documentation created
