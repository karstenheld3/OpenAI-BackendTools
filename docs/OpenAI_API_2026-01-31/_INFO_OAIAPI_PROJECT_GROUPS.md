# INFO: OpenAI API - Project Groups

**Doc ID**: OAIAPI-IN56
**Goal**: Document Project Groups API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_PROJECTS.md [OAIAPI-IN33]` for context

## Summary

Project Groups manages group membership within projects. Add groups to projects for team-based access control.

## Key Facts

- **Scope**: Project-level group management [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/projects/{project_id}/groups` - Add group
- `GET /v1/organization/projects/{project_id}/groups` - List groups
- `DELETE /v1/organization/projects/{project_id}/groups/{group_id}` - Remove group

## Sources

- OAIAPI-IN01-SC-OAI-PROJGRP - Official project groups documentation

## Document History

**[2026-01-30 11:35]**
- Initial documentation created
