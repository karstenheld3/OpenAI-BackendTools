# INFO: OpenAI API - Vector Store Files

**Doc ID**: OAIAPI-IN40
**Goal**: Document Vector Store Files API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_VECTOR_STORES.md [OAIAPI-IN22]` for context

## Summary

Vector Store Files manages individual files within vector stores. Files are added, processed (chunked and embedded), and can be removed. Processing is asynchronous with status tracking. Chunking strategy can be configured per file or inherited from store defaults.

## Key Facts

- **Processing**: Async chunking and embedding [VERIFIED]
- **Statuses**: in_progress, completed, failed, cancelled [VERIFIED]
- **Chunking**: Configurable per file [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/vector_stores/{vs_id}/files` - Add file
- `GET /v1/vector_stores/{vs_id}/files` - List files
- `GET /v1/vector_stores/{vs_id}/files/{file_id}` - Get file
- `DELETE /v1/vector_stores/{vs_id}/files/{file_id}` - Remove file

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

# Add file to vector store
vs_file = client.beta.vector_stores.files.create(
    vector_store_id="vs_abc123",
    file_id="file-xyz789"
)

# With custom chunking
vs_file = client.beta.vector_stores.files.create(
    vector_store_id="vs_abc123",
    file_id="file-xyz789",
    chunking_strategy={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 800,
            "chunk_overlap_tokens": 400
        }
    }
)

# List files
files = client.beta.vector_stores.files.list(
    vector_store_id="vs_abc123"
)

# Remove file
client.beta.vector_stores.files.delete(
    vector_store_id="vs_abc123",
    file_id="file-xyz789"
)
```

## Sources

- OAIAPI-IN01-SC-OAI-VSFILE - Official vector store files documentation

## Document History

**[2026-01-30 11:05]**
- Initial documentation created
