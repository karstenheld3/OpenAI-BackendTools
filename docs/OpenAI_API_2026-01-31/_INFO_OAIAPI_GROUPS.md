# INFO: OpenAI API - Groups

**Doc ID**: OAIAPI-IN52
**Goal**: Document Groups API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

Groups organize users for simplified access control. Assign roles to groups, then add users to groups instead of managing individual permissions.

## Key Facts

- **Purpose**: Simplified access management [VERIFIED]
- **Hierarchy**: Groups contain users [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/groups` - Create group
- `GET /v1/organization/groups` - List groups
- `GET /v1/organization/groups/{id}` - Get group
- `POST /v1/organization/groups/{id}` - Modify group
- `DELETE /v1/organization/groups/{id}` - Delete group

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

# Create group
group = client.organization.groups.create(
    name="Engineering Team"
)

# Add user to group
client.organization.groups.members.create(
    group_id=group.id,
    user_id="user_abc123"
)
```

## Sources

- OAIAPI-IN01-SC-OAI-GROUPS - Official groups documentation

## Document History

**[2026-01-30 11:30]**
- Initial documentation created
