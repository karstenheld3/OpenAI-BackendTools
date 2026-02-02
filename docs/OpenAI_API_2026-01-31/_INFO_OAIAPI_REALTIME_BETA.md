# INFO: OpenAI API - Realtime Beta (Legacy)

**Doc ID**: OAIAPI-IN63
**Goal**: Document legacy Realtime Beta API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_REALTIME.md [OAIAPI-IN26]` for context

## Summary

Realtime Beta is the legacy version of the Realtime API. It has been superseded by the GA Realtime API with improved features and stability. Legacy endpoints remain for backward compatibility but new development should use the current Realtime API.

## Key Facts

- **Status**: Legacy (superseded by Realtime GA) [VERIFIED]
- **Migration**: Use current Realtime API for new development [VERIFIED]

## Legacy Endpoints

- `POST /v1/realtime/sessions` (beta) - Create session
- WebSocket with beta client/server events

## Migration Guide

Update to current Realtime API:
- Use `/v1/realtime/sessions` (GA version)
- Update event types to GA format
- Use new session configuration options

## Sources

- OAIAPI-IN01-SC-OAI-RTBETA - Official realtime beta documentation

## Document History

**[2026-01-30 11:45]**
- Initial documentation created
