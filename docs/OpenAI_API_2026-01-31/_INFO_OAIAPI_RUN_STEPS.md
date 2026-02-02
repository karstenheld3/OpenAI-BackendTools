# INFO: OpenAI API - Run Steps

**Doc ID**: OAIAPI-IN31
**Goal**: Document Run Steps API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_RUNS.md [OAIAPI-IN25]` for context

## Summary

Run Steps provide granular visibility into the execution of an assistant run. Each step represents a discrete action like message creation or tool invocation. Steps are useful for debugging, understanding model behavior, and building detailed UIs that show the assistant's reasoning process.

## Key Facts

- **Step types**: message_creation, tool_calls [VERIFIED]
- **Read-only**: Cannot create or modify steps [VERIFIED]
- **Pagination**: Support cursor-based pagination [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/threads/{thread_id}/runs/{run_id}/steps` - List steps
- `GET /v1/threads/{thread_id}/runs/{run_id}/steps/{step_id}` - Get step

### Step Types

- `message_creation` - Assistant created a message
- `tool_calls` - Assistant called tool(s)

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

steps = client.beta.threads.runs.steps.list(
    thread_id="thread_abc123",
    run_id="run_xyz789"
)

for step in steps.data:
    print(f"{step.type}: {step.status}")
    if step.type == "tool_calls":
        for call in step.step_details.tool_calls:
            print(f"  - {call.type}: {call.function.name}")
```

## Response Examples

```json
{
  "id": "step_abc123",
  "object": "thread.run.step",
  "type": "tool_calls",
  "status": "completed",
  "step_details": {
    "type": "tool_calls",
    "tool_calls": [
      {
        "id": "call_xyz",
        "type": "function",
        "function": {
          "name": "get_weather",
          "arguments": "{\"location\":\"Paris\"}"
        }
      }
    ]
  }
}
```

## Sources

- OAIAPI-IN01-SC-OAI-RUNSTEP - Official run steps documentation

## Document History

**[2026-01-30 10:45]**
- Initial documentation created
