# INFO: OpenAI API - Audit Logs

**Doc ID**: OAIAPI-IN34
**Goal**: Document Audit Logs API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

Audit Logs provide a comprehensive record of organization activities for compliance and security monitoring. Logs capture user actions, API key usage, project changes, and administrative operations. Logs can be filtered by date range, event type, actor, and project.

## Key Facts

- **Retention**: 90 days [VERIFIED]
- **Events**: User, API, admin actions [VERIFIED]
- **Filtering**: By date, type, actor, project [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/organization/audit_logs` - List audit logs

### Event Categories

- `api_key.created` / `deleted` - API key events
- `invite.sent` / `accepted` / `deleted` - Invite events
- `user.added` / `deleted` / `updated` - User events
- `project.created` / `archived` - Project events
- `service_account.created` / `deleted` - Service account events

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Using admin API key

# List recent logs
logs = client.organization.audit_logs.list(limit=100)

for log in logs.data:
    print(f"{log.effective_at}: {log.type} by {log.actor.email}")

# Filter by event type
logs = client.organization.audit_logs.list(
    event_types=["api_key.created", "api_key.deleted"]
)

# Filter by date range
logs = client.organization.audit_logs.list(
    effective_at_gte="2026-01-01T00:00:00Z",
    effective_at_lte="2026-01-31T23:59:59Z"
)
```

## Response Examples

```json
{
  "id": "audit_abc123",
  "type": "api_key.created",
  "effective_at": "2026-01-30T10:00:00Z",
  "actor": {
    "type": "user",
    "user": {
      "id": "user_xyz",
      "email": "admin@example.com"
    }
  },
  "project": {
    "id": "proj_123",
    "name": "Production"
  }
}
```

## Sources

- OAIAPI-IN01-SC-OAI-AUDIT - Official audit logs documentation

## Document History

**[2026-01-30 10:50]**
- Initial documentation created
