# INFO: OpenAI API - Assistants Streaming

**Doc ID**: OAIAPI-IN32
**Goal**: Document streaming for Assistants API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ASSISTANTS.md [OAIAPI-IN21]` for context

## Summary

Assistants API supports streaming runs for real-time output delivery. When creating a run with streaming enabled, Server-Sent Events deliver thread, run, message, and step events as they occur. This enables building responsive UIs that show assistant progress in real-time.

## Key Facts

- **Protocol**: Server-Sent Events (SSE) [VERIFIED]
- **Enable**: `stream=True` in run creation [VERIFIED]
- **Events**: Thread, run, message, step events [VERIFIED]

## Event Types

- `thread.created` - Thread created
- `thread.run.created` - Run started
- `thread.run.in_progress` - Run processing
- `thread.run.completed` - Run finished
- `thread.message.created` - Message started
- `thread.message.delta` - Message content chunk
- `thread.message.completed` - Message finished
- `thread.run.step.created` - Step started
- `thread.run.step.delta` - Step progress
- `thread.run.step.completed` - Step finished

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

with client.beta.threads.runs.stream(
    thread_id="thread_abc123",
    assistant_id="asst_xyz789"
) as stream:
    for event in stream:
        if event.event == "thread.message.delta":
            print(event.data.delta.content[0].text.value, end="")
        elif event.event == "thread.run.completed":
            print("\nRun completed!")
```

### With Event Handlers

```python
from openai import OpenAI, AssistantEventHandler

class MyHandler(AssistantEventHandler):
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="")
    
    def on_run_completed(self):
        print("\nDone!")

client = OpenAI()

with client.beta.threads.runs.stream(
    thread_id="thread_abc123",
    assistant_id="asst_xyz789",
    event_handler=MyHandler()
) as stream:
    stream.until_done()
```

## Sources

- OAIAPI-IN01-SC-OAI-ASSTSTR - Official assistants streaming documentation

## Document History

**[2026-01-30 10:45]**
- Initial documentation created
