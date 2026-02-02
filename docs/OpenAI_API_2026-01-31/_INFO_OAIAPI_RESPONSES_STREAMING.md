# INFO: OpenAI API - Responses Streaming

**Doc ID**: OAIAPI-IN29
**Goal**: Document streaming events for Responses API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_RESPONSES.md [OAIAPI-IN11]` for context

## Summary

The Responses API supports streaming via Server-Sent Events (SSE) when `stream: true` is set. Events are emitted as the response is generated, including response lifecycle events, content deltas, and tool use events. This enables real-time display of responses as they're generated.

## Key Facts

- **Protocol**: Server-Sent Events (SSE) [VERIFIED]
- **Enable**: `stream: true` in request [VERIFIED]
- **Event types**: response.*, content.*, tool.* [VERIFIED]

## Event Types

### Response Events

- `response.created` - Response started
- `response.in_progress` - Processing
- `response.completed` - Finished
- `response.failed` - Error occurred

### Content Events

- `response.output_item.added` - Output item started
- `response.content_part.added` - Content part started
- `response.output_text.delta` - Text chunk
- `response.output_text.done` - Text complete

### Tool Events

- `response.function_call_arguments.delta` - Function args chunk
- `response.function_call_arguments.done` - Function call complete

## Request Examples

### Python Streaming

```python
from openai import OpenAI

client = OpenAI()

stream = client.responses.create(
    model="gpt-4o",
    input="Tell me a story",
    stream=True
)

for event in stream:
    if event.type == "response.output_text.delta":
        print(event.delta, end="")
    elif event.type == "response.completed":
        print("\nDone!")
```

## Sources

- OAIAPI-IN01-SC-OAI-RESPSTR - Official streaming documentation

## Document History

**[2026-01-30 10:35]**
- Initial documentation created
