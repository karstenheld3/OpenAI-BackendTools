# INFO: OpenAI API - Threads

**Doc ID**: OAIAPI-IN23
**Goal**: Document Threads API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ASSISTANTS.md [OAIAPI-IN21]` for context

## Summary

Threads represent conversations in the Assistants API. Each thread maintains a persistent message history that can be continued across multiple runs. Threads are created independently and then associated with assistants during run creation. They can include tool resources like vector stores for file search within the conversation context. Threads persist until explicitly deleted and can contain unlimited messages.

## Key Facts

- **Persistence**: Until explicitly deleted [VERIFIED]
- **Messages**: Unlimited per thread [VERIFIED]
- **Tool resources**: Vector stores for file search [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/threads` - Create thread
- `GET /v1/threads/{thread_id}` - Get thread
- `POST /v1/threads/{thread_id}` - Modify thread
- `DELETE /v1/threads/{thread_id}` - Delete thread
- `POST /v1/threads/runs` - Create thread and run

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

# Create empty thread
thread = client.beta.threads.create()

# Create with messages
thread = client.beta.threads.create(
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

# With tool resources
thread = client.beta.threads.create(
    tool_resources={
        "file_search": {"vector_store_ids": ["vs_abc123"]}
    }
)

# Delete thread
client.beta.threads.delete(thread.id)
```

## Response Examples

```json
{
  "id": "thread_abc123",
  "object": "thread",
  "created_at": 1700000000,
  "metadata": {},
  "tool_resources": {}
}
```

## Related Endpoints

- `_INFO_OAIAPI_MESSAGES.md` - Add messages to threads
- `_INFO_OAIAPI_RUNS.md` - Execute assistant on thread

## Sources

- OAIAPI-IN01-SC-OAI-THREAD - Official threads documentation

## Document History

**[2026-01-30 10:25]**
- Initial documentation created
