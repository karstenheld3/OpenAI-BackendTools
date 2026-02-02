# INFO: OpenAI API - Project Users

**Doc ID**: OAIAPI-IN55
**Goal**: Document Project Users API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_PROJECTS.md [OAIAPI-IN33]` for context

## Summary

Project Users manages user membership within projects. Add, list, update, and remove users from specific projects.

## Key Facts

- **Scope**: Project-level user management [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/projects/{project_id}/users` - Add user
- `GET /v1/organization/projects/{project_id}/users` - List users
- `GET /v1/organization/projects/{project_id}/users/{user_id}` - Get user
- `POST /v1/organization/projects/{project_id}/users/{user_id}` - Update user
- `DELETE /v1/organization/projects/{project_id}/users/{user_id}` - Remove user

## Sources

- OAIAPI-IN01-SC-OAI-PROJUSER - Official project users documentation

## Document History

**[2026-01-30 11:35]**
- Initial documentation created
