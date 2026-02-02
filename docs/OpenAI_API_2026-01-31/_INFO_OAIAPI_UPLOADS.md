# INFO: OpenAI API - Uploads

**Doc ID**: OAIAPI-IN36
**Goal**: Document Uploads API for large files
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_FILES.md [OAIAPI-IN18]` for context

## Summary

The Uploads API enables uploading large files in parts when the standard Files API 512MB limit is insufficient. Files are uploaded by creating an upload, sending parts, and completing the upload. This supports files up to 8GB. Incomplete uploads can be cancelled.

## Key Facts

- **Max size**: 8 GB [VERIFIED]
- **Part size**: 64 MB max per part [VERIFIED]
- **Workflow**: Create → Add Parts → Complete [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/uploads` - Create upload
- `POST /v1/uploads/{upload_id}/parts` - Add part
- `POST /v1/uploads/{upload_id}/complete` - Complete upload
- `POST /v1/uploads/{upload_id}/cancel` - Cancel upload

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

# 1. Create upload
upload = client.uploads.create(
    purpose="fine-tune",
    filename="large_dataset.jsonl",
    bytes=5_000_000_000,  # 5GB
    mime_type="application/jsonl"
)

# 2. Upload parts
with open("large_dataset.jsonl", "rb") as f:
    part_number = 0
    while chunk := f.read(64 * 1024 * 1024):  # 64MB chunks
        part = client.uploads.parts.create(
            upload_id=upload.id,
            data=chunk
        )
        part_number += 1

# 3. Complete upload
file = client.uploads.complete(
    upload_id=upload.id,
    part_ids=[p.id for p in parts]
)

print(f"File ID: {file.id}")
```

## Response Examples

```json
{
  "id": "upload_abc123",
  "object": "upload",
  "bytes": 5000000000,
  "created_at": 1700000000,
  "filename": "large_dataset.jsonl",
  "purpose": "fine-tune",
  "status": "pending",
  "expires_at": 1700086400
}
```

## Sources

- OAIAPI-IN01-SC-OAI-UPLOAD - Official uploads documentation

## Document History

**[2026-01-30 10:55]**
- Initial documentation created
