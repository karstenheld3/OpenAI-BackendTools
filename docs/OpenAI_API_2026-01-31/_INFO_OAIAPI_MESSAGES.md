# INFO: OpenAI API - Messages

**Doc ID**: OAIAPI-IN24
**Goal**: Document Messages API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_THREADS.md [OAIAPI-IN23]` for context

## Summary

Messages are the content units within Assistants API threads. Users add messages to threads, and assistants generate response messages during runs. Messages support multiple content types including text, images, and file attachments. Text messages may contain annotations (file citations, file paths) that reference tool outputs. Messages are paginated and can be listed, retrieved, and modified.

## Key Facts

- **Roles**: user, assistant [VERIFIED]
- **Content types**: text, images, files [VERIFIED]
- **Annotations**: File citations, file paths [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/threads/{thread_id}/messages` - Create message
- `GET /v1/threads/{thread_id}/messages` - List messages
- `GET /v1/threads/{thread_id}/messages/{message_id}` - Get message
- `POST /v1/threads/{thread_id}/messages/{message_id}` - Modify message
- `DELETE /v1/threads/{thread_id}/messages/{message_id}` - Delete message

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

# Add user message
message = client.beta.threads.messages.create(
    thread_id="thread_abc123",
    role="user",
    content="What is the capital of France?"
)

# With file attachment
message = client.beta.threads.messages.create(
    thread_id="thread_abc123",
    role="user",
    content="Analyze this document",
    attachments=[
        {"file_id": "file-xyz", "tools": [{"type": "file_search"}]}
    ]
)

# List messages
messages = client.beta.threads.messages.list(thread_id="thread_abc123")
for msg in messages.data:
    print(f"{msg.role}: {msg.content[0].text.value}")
```

## Response Examples

```json
{
  "id": "msg_abc123",
  "object": "thread.message",
  "created_at": 1700000000,
  "thread_id": "thread_xyz",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": {
        "value": "The capital of France is Paris.",
        "annotations": []
      }
    }
  ]
}
```

## Related Endpoints

- `_INFO_OAIAPI_THREADS.md` - Thread management
- `_INFO_OAIAPI_RUNS.md` - Execute to generate responses

## Sources

- OAIAPI-IN01-SC-OAI-MSG - Official messages documentation

## Document History

**[2026-01-30 10:25]**
- Initial documentation created
