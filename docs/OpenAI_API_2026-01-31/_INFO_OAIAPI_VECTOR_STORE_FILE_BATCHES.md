# INFO: OpenAI API - Vector Store File Batches

**Doc ID**: OAIAPI-IN41
**Goal**: Document Vector Store File Batches API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_VECTOR_STORES.md [OAIAPI-IN22]` for context

## Summary

Vector Store File Batches enable bulk file operations on vector stores. Instead of adding files one at a time, batches add multiple files in a single operation with unified status tracking.

## Key Facts

- **Bulk operations**: Add multiple files at once [VERIFIED]
- **Status tracking**: Unified batch status [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/vector_stores/{vs_id}/file_batches` - Create batch
- `GET /v1/vector_stores/{vs_id}/file_batches/{batch_id}` - Get batch
- `POST /v1/vector_stores/{vs_id}/file_batches/{batch_id}/cancel` - Cancel batch
- `GET /v1/vector_stores/{vs_id}/file_batches/{batch_id}/files` - List batch files

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

# Create file batch
batch = client.beta.vector_stores.file_batches.create(
    vector_store_id="vs_abc123",
    file_ids=["file-1", "file-2", "file-3"]
)

# Check status
batch = client.beta.vector_stores.file_batches.retrieve(
    vector_store_id="vs_abc123",
    batch_id=batch.id
)

print(f"Status: {batch.status}")
print(f"Completed: {batch.file_counts.completed}/{batch.file_counts.total}")
```

## Sources

- OAIAPI-IN01-SC-OAI-VSBATCH - Official vector store file batches documentation

## Document History

**[2026-01-30 11:05]**
- Initial documentation created
