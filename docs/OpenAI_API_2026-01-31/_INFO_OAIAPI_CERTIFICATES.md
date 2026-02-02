# INFO: OpenAI API - Certificates

**Doc ID**: OAIAPI-IN61
**Goal**: Document Certificates API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

Certificates API manages mTLS certificates for enhanced security. Upload client certificates to enable mutual TLS authentication for API requests.

## Key Facts

- **Purpose**: mTLS authentication [VERIFIED]
- **Security**: Enhanced request authentication [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/organization/certificates` - Upload certificate
- `GET /v1/organization/certificates` - List certificates
- `GET /v1/organization/certificates/{id}` - Get certificate
- `DELETE /v1/organization/certificates/{id}` - Delete certificate

## Sources

- OAIAPI-IN01-SC-OAI-CERTS - Official certificates documentation

## Document History

**[2026-01-30 11:45]**
- Initial documentation created
