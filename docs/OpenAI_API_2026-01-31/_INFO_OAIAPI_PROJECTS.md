# INFO: OpenAI API - Projects

**Doc ID**: OAIAPI-IN33
**Goal**: Document Projects API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

Projects provide isolation within an organization for access control, billing, and rate limits. Each project has its own API keys, service accounts, and configurable rate limits. Projects help separate development environments, teams, or applications while maintaining centralized organization management.

## Key Facts

- **Isolation**: Separate API keys and usage tracking [VERIFIED]
- **Rate limits**: Configurable per project [VERIFIED]
- **Archive**: Projects can be archived instead of deleted [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/projects` - Create project
- `GET /v1/organization/projects` - List projects
- `GET /v1/organization/projects/{id}` - Get project
- `POST /v1/organization/projects/{id}` - Modify project
- `POST /v1/organization/projects/{id}/archive` - Archive project

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Using admin API key

# Create project
project = client.organization.projects.create(
    name="Production App"
)

# List projects
projects = client.organization.projects.list()
for p in projects.data:
    print(f"{p.id}: {p.name}")

# Archive project
client.organization.projects.archive(project.id)
```

## Response Examples

```json
{
  "id": "proj_abc123",
  "object": "organization.project",
  "name": "Production App",
  "created_at": 1700000000,
  "archived_at": null,
  "status": "active"
}
```

## Sources

- OAIAPI-IN01-SC-OAI-PROJ - Official projects documentation

## Document History

**[2026-01-30 10:50]**
- Initial documentation created
