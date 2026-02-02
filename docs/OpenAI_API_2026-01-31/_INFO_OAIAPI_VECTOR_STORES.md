# INFO: OpenAI API - Vector Stores

**Doc ID**: OAIAPI-IN22
**Goal**: Document Vector Stores API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

Vector Stores enable semantic search over documents for the Assistants API file_search tool. Files are automatically chunked, embedded, and indexed when added to a vector store. The API supports creating, managing, and configuring stores with expiration policies. Vector stores can be attached to assistants or threads for retrieval-augmented generation (RAG). Files are processed asynchronously after addition, with status tracking available. Expiration policies automatically clean up unused stores.

## Key Facts

- **Max files**: 10,000 per vector store [VERIFIED]
- **Max size**: 100 GB per vector store [VERIFIED]
- **Chunking**: Automatic, configurable [VERIFIED]
- **Expiration**: Configurable auto-deletion [VERIFIED]

## Use Cases

- **Knowledge bases**: Search documentation, FAQs
- **Document Q&A**: Answer questions from PDFs
- **Research**: Search across papers, articles
- **Support**: Search previous tickets, solutions

## Quick Reference

### Endpoints

- `POST /v1/vector_stores` - Create vector store
- `GET /v1/vector_stores` - List vector stores
- `GET /v1/vector_stores/{id}` - Get vector store
- `POST /v1/vector_stores/{id}` - Modify vector store
- `DELETE /v1/vector_stores/{id}` - Delete vector store

### File Statuses

- `in_progress` - Being processed
- `completed` - Ready for search
- `cancelled` - Processing cancelled
- `failed` - Processing failed

## Endpoints

### Create Vector Store

**Request**

```
POST /v1/vector_stores
```

**Parameters**

- `name` (string, optional) - Store name
- `file_ids` (array, optional) - Files to add initially
- `expires_after` (object, optional) - Expiration policy
  - `anchor` (string) - `last_active_at`
  - `days` (integer) - Days until expiration
- `chunking_strategy` (object, optional) - Chunking config
- `metadata` (object, optional) - Custom key-value pairs

### Get Vector Store

```
GET /v1/vector_stores/{vector_store_id}
```

### Modify Vector Store

```
POST /v1/vector_stores/{vector_store_id}
```

### Delete Vector Store

```
DELETE /v1/vector_stores/{vector_store_id}
```

## Request Examples

### Create Vector Store (Python)

```python
from openai import OpenAI

client = OpenAI()

vector_store = client.beta.vector_stores.create(
    name="My Knowledge Base"
)

print(f"Vector Store ID: {vector_store.id}")
```

### With Files

```python
from openai import OpenAI

client = OpenAI()

# Upload file first
file = client.files.create(
    file=open("document.pdf", "rb"),
    purpose="assistants"
)

# Create store with file
vector_store = client.beta.vector_stores.create(
    name="Knowledge Base",
    file_ids=[file.id]
)
```

### With Expiration

```python
from openai import OpenAI

client = OpenAI()

vector_store = client.beta.vector_stores.create(
    name="Temp Store",
    expires_after={
        "anchor": "last_active_at",
        "days": 7  # Delete after 7 days of inactivity
    }
)
```

### Add File to Store

```python
from openai import OpenAI

client = OpenAI()

# Add file to existing store
vector_store_file = client.beta.vector_stores.files.create(
    vector_store_id="vs_abc123",
    file_id="file-xyz789"
)

# Check processing status
print(f"Status: {vector_store_file.status}")
```

### Poll for File Processing

```python
from openai import OpenAI
import time

client = OpenAI()

file = client.beta.vector_stores.files.create(
    vector_store_id="vs_abc123",
    file_id="file-xyz789"
)

while file.status == "in_progress":
    time.sleep(1)
    file = client.beta.vector_stores.files.retrieve(
        vector_store_id="vs_abc123",
        file_id=file.id
    )

print(f"Final status: {file.status}")
```

### Batch File Upload

```python
from openai import OpenAI

client = OpenAI()

# Upload multiple files
file_ids = []
for filename in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    file = client.files.create(
        file=open(filename, "rb"),
        purpose="assistants"
    )
    file_ids.append(file.id)

# Create batch
batch = client.beta.vector_stores.file_batches.create(
    vector_store_id="vs_abc123",
    file_ids=file_ids
)

print(f"Batch ID: {batch.id}")
```

### Use with Assistant

```python
from openai import OpenAI

client = OpenAI()

# Create assistant with vector store
assistant = client.beta.assistants.create(
    name="Research Assistant",
    instructions="Answer questions using the provided documents.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {
            "vector_store_ids": ["vs_abc123"]
        }
    }
)
```

## Response Examples

### Vector Store Object

```json
{
  "id": "vs_abc123",
  "object": "vector_store",
  "created_at": 1700000000,
  "name": "My Knowledge Base",
  "usage_bytes": 1024000,
  "file_counts": {
    "in_progress": 0,
    "completed": 10,
    "failed": 0,
    "cancelled": 0,
    "total": 10
  },
  "status": "completed",
  "expires_after": null,
  "expires_at": null,
  "last_active_at": 1700000000,
  "metadata": {}
}
```

## Error Codes

- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Vector store not found
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- Vector stores API is in beta (`client.beta.vector_stores`)
- File processing is async - poll for completion
- Chunking strategy affects search quality
- Expired stores are deleted automatically
- Deleting store doesn't delete source files

## Related Endpoints

- `_INFO_OAIAPI_VECTOR_STORE_FILES.md` - File operations
- `_INFO_OAIAPI_ASSISTANTS.md` - Using with assistants
- `_INFO_OAIAPI_FILES.md` - File upload

## Sources

- OAIAPI-IN01-SC-OAI-VSTORE - Official vector stores documentation

## Document History

**[2026-01-30 10:20]**
- Initial documentation created
