# INFO: OpenAI API - Realtime Sessions

**Doc ID**: OAIAPI-IN42
**Goal**: Document Realtime Sessions API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_REALTIME.md [OAIAPI-IN26]` for context

## Summary

Realtime Sessions creates client secrets for WebSocket connections. The REST endpoint generates a short-lived secret that clients use to establish authenticated WebSocket connections for real-time voice interactions.

## Key Facts

- **Purpose**: Get client secret for WebSocket auth [VERIFIED]
- **Expiration**: Short-lived tokens [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/realtime/sessions` - Create session

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

session = client.realtime.sessions.create(
    model="gpt-4o-realtime-preview",
    voice="alloy",
    instructions="You are a helpful voice assistant."
)

# Use client_secret for WebSocket connection
print(f"Client secret: {session.client_secret.value}")
print(f"Expires at: {session.client_secret.expires_at}")
```

## Response Examples

```json
{
  "id": "sess_abc123",
  "object": "realtime.session",
  "model": "gpt-4o-realtime-preview",
  "voice": "alloy",
  "client_secret": {
    "value": "ek_...",
    "expires_at": 1700000600
  }
}
```

## Sources

- OAIAPI-IN01-SC-OAI-RTSESS - Official realtime sessions documentation

## Document History

**[2026-01-30 11:10]**
- Initial documentation created
