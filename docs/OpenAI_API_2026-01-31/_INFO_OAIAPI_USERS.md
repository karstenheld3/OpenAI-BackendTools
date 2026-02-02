# INFO: OpenAI API - Users

**Doc ID**: OAIAPI-IN51
**Goal**: Document Users API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

The Users API manages organization members. List users, update roles, and remove members from the organization.

## Key Facts

- **Scope**: Organization-level user management [VERIFIED]
- **Roles**: owner, member, reader [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/organization/users` - List users
- `GET /v1/organization/users/{user_id}` - Get user
- `POST /v1/organization/users/{user_id}` - Modify user
- `DELETE /v1/organization/users/{user_id}` - Remove user

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

# List users
users = client.organization.users.list()
for user in users.data:
    print(f"{user.email}: {user.role}")

# Update role
client.organization.users.update(
    user_id="user_abc123",
    role="member"
)

# Remove user
client.organization.users.delete("user_abc123")
```

## Sources

- OAIAPI-IN01-SC-OAI-USERS - Official users documentation

## Document History

**[2026-01-30 11:25]**
- Initial documentation created
