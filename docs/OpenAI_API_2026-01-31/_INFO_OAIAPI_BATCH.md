# INFO: OpenAI API - Batch

**Doc ID**: OAIAPI-IN19
**Goal**: Document Batch API for async processing
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Batch API enables asynchronous processing of large numbers of API requests at 50% reduced cost. Batches are submitted as JSONL files containing individual requests, processed within a 24-hour window, and results returned as a downloadable file. This is ideal for non-time-sensitive workloads like bulk content generation, embeddings, or evaluations. Batches can be monitored for status, cancelled if needed, and support all major endpoints including chat completions and embeddings.

## Key Facts

- **Cost savings**: 50% discount vs real-time [VERIFIED]
- **Completion window**: 24 hours [VERIFIED]
- **Input format**: JSONL file [VERIFIED]
- **Max requests**: 50,000 per batch [VERIFIED]
- **Supported endpoints**: Chat, Embeddings, Completions [VERIFIED]

## Use Cases

- **Bulk generation**: Generate thousands of responses overnight
- **Embeddings**: Create embeddings for large document sets
- **Evaluations**: Run evaluations across many test cases
- **Data processing**: Classify or extract from large datasets

## Quick Reference

### Endpoints

- `POST /v1/batches` - Create batch
- `GET /v1/batches/{batch_id}` - Get batch status
- `GET /v1/batches` - List batches
- `POST /v1/batches/{batch_id}/cancel` - Cancel batch

### Batch Statuses

- `validating` - Input file being validated
- `in_progress` - Requests being processed
- `finalizing` - Results being compiled
- `completed` - Done, output available
- `failed` - Batch failed
- `expired` - Exceeded 24-hour window
- `cancelling` - Cancel in progress
- `cancelled` - Cancelled

## Input File Format

JSONL with one request per line:

```jsonl
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o", "messages": [{"role": "user", "content": "Hello"}]}}
{"custom_id": "request-2", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o", "messages": [{"role": "user", "content": "World"}]}}
```

### Request Fields

- `custom_id` (string, required) - Your unique identifier
- `method` (string, required) - Always `POST`
- `url` (string, required) - API endpoint path
- `body` (object, required) - Request body

## Output File Format

JSONL with responses:

```jsonl
{"id": "batch_req_123", "custom_id": "request-1", "response": {"status_code": 200, "body": {...}}, "error": null}
{"id": "batch_req_456", "custom_id": "request-2", "response": {"status_code": 200, "body": {...}}, "error": null}
```

## Endpoints

### Create Batch

**Request**

```
POST /v1/batches
```

**Parameters**

- `input_file_id` (string, required) - ID of uploaded JSONL file
- `endpoint` (string, required) - Target endpoint
- `completion_window` (string, required) - `24h`
- `metadata` (object, optional) - Custom key-value pairs

### Get Batch

```
GET /v1/batches/{batch_id}
```

### List Batches

```
GET /v1/batches
```

### Cancel Batch

```
POST /v1/batches/{batch_id}/cancel
```

## Request Examples

### Complete Workflow (Python)

```python
from openai import OpenAI
import json
import time

client = OpenAI()

# 1. Create input file
requests = [
    {"custom_id": f"req-{i}", "method": "POST", "url": "/v1/chat/completions", 
     "body": {"model": "gpt-4o-mini", "messages": [{"role": "user", "content": f"Count to {i}"}]}}
    for i in range(1, 101)
]

with open("batch_input.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")

# 2. Upload file
batch_file = client.files.create(
    file=open("batch_input.jsonl", "rb"),
    purpose="batch"
)

# 3. Create batch
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "Counting batch"}
)

print(f"Batch ID: {batch.id}")

# 4. Poll for completion
while batch.status in ["validating", "in_progress", "finalizing"]:
    time.sleep(60)
    batch = client.batches.retrieve(batch.id)
    print(f"Status: {batch.status}")

# 5. Download results
if batch.status == "completed":
    output = client.files.content(batch.output_file_id)
    with open("batch_output.jsonl", "wb") as f:
        f.write(output.read())
    print("Results saved!")
else:
    print(f"Batch failed: {batch.errors}")
```

### Check Batch Status

```python
from openai import OpenAI

client = OpenAI()

batch = client.batches.retrieve("batch_abc123")

print(f"Status: {batch.status}")
print(f"Total: {batch.request_counts.total}")
print(f"Completed: {batch.request_counts.completed}")
print(f"Failed: {batch.request_counts.failed}")
```

### List Recent Batches

```python
from openai import OpenAI

client = OpenAI()

batches = client.batches.list(limit=10)
for b in batches.data:
    print(f"{b.id}: {b.status} ({b.request_counts.completed}/{b.request_counts.total})")
```

## Response Examples

### Batch Object

```json
{
  "id": "batch_abc123",
  "object": "batch",
  "endpoint": "/v1/chat/completions",
  "errors": null,
  "input_file_id": "file-input123",
  "completion_window": "24h",
  "status": "completed",
  "output_file_id": "file-output456",
  "error_file_id": null,
  "created_at": 1700000000,
  "in_progress_at": 1700000060,
  "expires_at": 1700086400,
  "finalizing_at": 1700003600,
  "completed_at": 1700003660,
  "failed_at": null,
  "expired_at": null,
  "request_counts": {
    "total": 100,
    "completed": 100,
    "failed": 0
  },
  "metadata": {}
}
```

## Error Codes

- `400 Bad Request` - Invalid input file format
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Batch not found
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- Maximum 50,000 requests per batch
- Each request in batch has independent retry logic
- Failed requests appear in error file, not output file
- Batch processing order is not guaranteed
- Streaming not supported in batch requests

## Related Endpoints

- `_INFO_OAIAPI_FILES.md` - File upload for batch input
- `_INFO_OAIAPI_CHAT.md` - Chat completions in batch

## Sources

- OAIAPI-IN01-SC-OAI-BATCH - Official batch documentation

## Document History

**[2026-01-30 10:10]**
- Initial documentation created
