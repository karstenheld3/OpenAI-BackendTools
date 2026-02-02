# INFO: OpenAI API - Container Files

**Doc ID**: OAIAPI-IN47
**Goal**: Document Container Files API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_CONTAINERS.md [OAIAPI-IN46]` for context

## Summary

Container Files manages files within container environments. Files can be uploaded to, listed in, and downloaded from containers.

## Key Facts

- **Operations**: Upload, list, download, delete [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/containers/{container_id}/files` - Upload file
- `GET /v1/containers/{container_id}/files` - List files
- `GET /v1/containers/{container_id}/files/{path}` - Get file
- `DELETE /v1/containers/{container_id}/files/{path}` - Delete file

## Sources

- OAIAPI-IN01-SC-OAI-CONTFILE - Official container files documentation

## Document History

**[2026-01-30 11:20]**
- Initial documentation created
