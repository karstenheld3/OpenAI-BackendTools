# INFO: OpenAI API - Files

**Doc ID**: OAIAPI-IN18
**Goal**: Document Files API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Files API manages file uploads for use with other OpenAI features including fine-tuning, assistants, and batch processing. Files are uploaded with a purpose that determines their allowed uses. The API supports listing, retrieving metadata, downloading content, and deleting files. File size limits vary by purpose, with a general limit of 512 MB per file. Files are stored securely and can be referenced by ID in subsequent API calls.

## Key Facts

- **Max file size**: 512 MB [VERIFIED]
- **Fine-tuning format**: JSONL [VERIFIED]
- **Batch format**: JSONL [VERIFIED]
- **Assistants formats**: Various (txt, pdf, images, etc.) [VERIFIED]

## Use Cases

- **Fine-tuning**: Upload training data
- **Assistants**: Provide files for code interpreter or retrieval
- **Batch processing**: Upload batch request files
- **Vector stores**: Source files for embeddings

## Quick Reference

### Endpoints

- `POST /v1/files` - Upload file
- `GET /v1/files` - List files
- `GET /v1/files/{file_id}` - Get file metadata
- `GET /v1/files/{file_id}/content` - Download file content
- `DELETE /v1/files/{file_id}` - Delete file

### Purpose Values

- `assistants` - For Assistants API (retrieval, code interpreter)
- `assistants_output` - Output from Assistants
- `batch` - Batch API input
- `batch_output` - Batch API output
- `fine-tune` - Fine-tuning training data
- `fine-tune-results` - Fine-tuning results
- `vision` - Image inputs for vision models

## Endpoints

### Upload File

**Request**

```
POST /v1/files
Content-Type: multipart/form-data
```

**Parameters**

- `file` (file, required) - File to upload
- `purpose` (string, required) - Purpose of the file

**Response**

- `id` (string) - File ID
- `object` (string) - Always `file`
- `bytes` (integer) - File size
- `created_at` (integer) - Unix timestamp
- `filename` (string) - Original filename
- `purpose` (string) - File purpose

### List Files

**Request**

```
GET /v1/files
```

**Parameters**

- `purpose` (string, optional) - Filter by purpose
- `limit` (integer, optional) - Max results (default 10000)
- `order` (string, optional) - `asc` or `desc`
- `after` (string, optional) - Pagination cursor

### Get File

```
GET /v1/files/{file_id}
```

### Download Content

```
GET /v1/files/{file_id}/content
```

### Delete File

```
DELETE /v1/files/{file_id}
```

## Request Examples

### Upload File (cURL)

```bash
curl https://api.openai.com/v1/files \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F purpose="fine-tune" \
  -F file="@training_data.jsonl"
```

### Python Upload

```python
from openai import OpenAI

client = OpenAI()

# Upload for fine-tuning
file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

print(f"File ID: {file.id}")
```

### Python List Files

```python
from openai import OpenAI

client = OpenAI()

# List all files
files = client.files.list()
for f in files.data:
    print(f"{f.id}: {f.filename} ({f.purpose})")

# Filter by purpose
fine_tune_files = client.files.list(purpose="fine-tune")
```

### Python Download Content

```python
from openai import OpenAI

client = OpenAI()

content = client.files.content("file-abc123")

# Save to file
with open("downloaded.jsonl", "wb") as f:
    f.write(content.read())
```

### Python Delete

```python
from openai import OpenAI

client = OpenAI()

deleted = client.files.delete("file-abc123")
print(f"Deleted: {deleted.deleted}")
```

## Response Examples

### Upload Response

```json
{
  "id": "file-abc123",
  "object": "file",
  "bytes": 140,
  "created_at": 1700000000,
  "filename": "training_data.jsonl",
  "purpose": "fine-tune"
}
```

### List Response

```json
{
  "object": "list",
  "data": [
    {
      "id": "file-abc123",
      "object": "file",
      "bytes": 140,
      "created_at": 1700000000,
      "filename": "training_data.jsonl",
      "purpose": "fine-tune"
    }
  ],
  "has_more": false
}
```

## Fine-tuning File Format

JSONL with `messages` array:

```jsonl
{"messages": [{"role": "system", "content": "You are an assistant."}, {"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}
{"messages": [{"role": "user", "content": "What is 2+2?"}, {"role": "assistant", "content": "4"}]}
```

## Batch File Format

JSONL with request objects:

```jsonl
{"custom_id": "req-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}}
{"custom_id": "req-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o", "messages": [{"role": "user", "content": "World"}]}}
```

## Error Codes

- `400 Bad Request` - Invalid file format or purpose
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - File not found
- `413 Payload Too Large` - File exceeds size limit

## Gotchas and Quirks

- Files may take time to process after upload
- Fine-tuning files are validated on job creation, not upload
- Assistants files have different size limits per tool
- Downloaded content may differ from uploaded (processing)

## Related Endpoints

- `_INFO_OAIAPI_UPLOADS.md` - Large file uploads
- `_INFO_OAIAPI_FINE_TUNING.md` - Using files for training
- `_INFO_OAIAPI_BATCH.md` - Using files for batch

## Sources

- OAIAPI-IN01-SC-OAI-FILES - Official files documentation

## Document History

**[2026-01-30 10:05]**
- Initial documentation created
