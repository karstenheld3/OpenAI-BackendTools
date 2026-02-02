# INFO: OpenAI API - Administration

**Doc ID**: OAIAPI-IN30
**Goal**: Document Administration API overview
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Administration API enables programmatic management of OpenAI organizations, projects, users, and access control. It requires Admin API keys with elevated permissions. Key capabilities include managing organization members, creating projects, configuring rate limits, and accessing audit logs. This is essential for enterprise deployments requiring automated governance and compliance.

## Key Facts

- **Authentication**: Admin API keys required [VERIFIED]
- **Scope**: Organization-level management [VERIFIED]
- **Capabilities**: Users, projects, roles, audit logs [VERIFIED]

## Admin API Key

Admin API keys have elevated permissions and are created in the organization settings dashboard. They are required for all administration endpoints.

## Capabilities

- **Users**: Invite, list, modify, remove organization members
- **Groups**: Create and manage user groups
- **Roles**: Define and assign roles
- **Projects**: Create, archive, configure projects
- **Rate limits**: Configure per-project rate limits
- **Audit logs**: Query organization activity
- **Certificates**: Manage mTLS certificates

## Endpoints Overview

- `/v1/organization/admin_api_keys` - Manage admin keys
- `/v1/organization/invites` - User invitations
- `/v1/organization/users` - Organization members
- `/v1/organization/groups` - User groups
- `/v1/organization/roles` - Role definitions
- `/v1/organization/projects` - Project management
- `/v1/organization/audit_logs` - Activity logs
- `/v1/organization/usage` - Usage metrics

## Sources

- OAIAPI-IN01-SC-OAI-ADMIN - Official administration documentation

## Document History

**[2026-01-30 10:40]**
- Initial documentation created
