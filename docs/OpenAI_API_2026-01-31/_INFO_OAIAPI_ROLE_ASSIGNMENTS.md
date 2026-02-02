# INFO: OpenAI API - Role Assignments

**Doc ID**: OAIAPI-IN54
**Goal**: Document Role Assignments API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ROLES.md [OAIAPI-IN53]` for context

## Summary

Role Assignments bind roles to users or groups at organization or project scope. This determines what actions principals can perform.

## Key Facts

- **Principals**: Users or groups [VERIFIED]
- **Scope**: Organization or project level [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/role_assignments` - Create assignment
- `GET /v1/organization/role_assignments` - List assignments
- `DELETE /v1/organization/role_assignments/{id}` - Delete assignment

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Admin API key

# Assign role to user
assignment = client.organization.role_assignments.create(
    principal_id="user_abc123",
    principal_type="user",
    role_id="role_member",
    scope_type="organization"
)

# Assign role at project scope
assignment = client.organization.role_assignments.create(
    principal_id="group_xyz",
    principal_type="group",
    role_id="role_member",
    scope_type="project",
    scope_id="proj_123"
)
```

## Sources

- OAIAPI-IN01-SC-OAI-ROLEASS - Official role assignments documentation

## Document History

**[2026-01-30 11:30]**
- Initial documentation created
