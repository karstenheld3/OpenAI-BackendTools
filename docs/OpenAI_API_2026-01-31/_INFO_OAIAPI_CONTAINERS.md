# INFO: OpenAI API - Containers

**Doc ID**: OAIAPI-IN46
**Goal**: Document Containers API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

Containers provide isolated execution environments for code and file operations. They extend the code interpreter capability with persistent file systems and custom configurations.

## Key Facts

- **Isolation**: Sandboxed execution [VERIFIED]
- **Persistence**: Files persist within container [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/containers` - Create container
- `GET /v1/containers` - List containers
- `GET /v1/containers/{id}` - Get container
- `DELETE /v1/containers/{id}` - Delete container

## Sources

- OAIAPI-IN01-SC-OAI-CONTAIN - Official containers documentation

## Document History

**[2026-01-30 11:20]**
- Initial documentation created
