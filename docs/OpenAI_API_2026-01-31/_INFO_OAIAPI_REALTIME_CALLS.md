# INFO: OpenAI API - Realtime Calls

**Doc ID**: OAIAPI-IN45
**Goal**: Document Realtime Calls API for telephony
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_REALTIME.md [OAIAPI-IN26]` for context

## Summary

Realtime Calls enable voice AI integration with telephony systems. This extends the Realtime API for phone-based interactions, handling call setup, audio routing, and call management.

## Key Facts

- **Use case**: Phone/telephony integration [VERIFIED]
- **Protocol**: WebSocket with call events [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/realtime/calls` - Initiate call
- `GET /v1/realtime/calls/{call_id}` - Get call status

## Sources

- OAIAPI-IN01-SC-OAI-RTCALLS - Official realtime calls documentation

## Document History

**[2026-01-30 11:15]**
- Initial documentation created
