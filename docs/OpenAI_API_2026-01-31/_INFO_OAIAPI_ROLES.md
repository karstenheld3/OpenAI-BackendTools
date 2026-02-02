# INFO: OpenAI API - Roles

**Doc ID**: OAIAPI-IN53
**Goal**: Document Roles API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

Roles define permission sets that can be assigned to users or groups. List available roles to understand permission options.

## Key Facts

- **Types**: owner, member, reader, custom [VERIFIED]
- **Scope**: Organization and project level [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/organization/roles` - List roles
- `GET /v1/organization/roles/{role_id}` - Get role

## Built-in Roles

- **owner** - Full organization access
- **member** - API usage, limited admin
- **reader** - Read-only access

## Sources

- OAIAPI-IN01-SC-OAI-ROLES - Official roles documentation

## Document History

**[2026-01-30 11:30]**
- Initial documentation created
