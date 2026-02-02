# INFO: OpenAI API - Runs

**Doc ID**: OAIAPI-IN25
**Goal**: Document Runs API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ASSISTANTS.md [OAIAPI-IN21]` for context

## Summary

Runs execute an assistant on a thread, processing messages and generating responses. A run progresses through statuses from queued to completed (or failed). Runs may require action when the assistant invokes function tools, requiring the client to submit tool outputs. Runs can be cancelled and support streaming for real-time output. Each run tracks token usage and can override assistant settings like model and instructions.

## Key Facts

- **Statuses**: queued, in_progress, requires_action, completed, failed, cancelled, expired [VERIFIED]
- **Expiration**: 10 minutes if not completed [VERIFIED]
- **Tool outputs**: Required for function calls [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/threads/{thread_id}/runs` - Create run
- `GET /v1/threads/{thread_id}/runs` - List runs
- `GET /v1/threads/{thread_id}/runs/{run_id}` - Get run
- `POST /v1/threads/{thread_id}/runs/{run_id}` - Modify run
- `POST /v1/threads/{thread_id}/runs/{run_id}/cancel` - Cancel run
- `POST /v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs` - Submit tool outputs

### Run Statuses

- `queued` - Waiting to start
- `in_progress` - Processing
- `requires_action` - Waiting for tool outputs
- `completed` - Finished successfully
- `failed` - Error occurred
- `cancelling` - Cancel in progress
- `cancelled` - Cancelled
- `expired` - Timed out

## Request Examples

### Python

```python
from openai import OpenAI
import time

client = OpenAI()

# Create and poll run
run = client.beta.threads.runs.create(
    thread_id="thread_abc123",
    assistant_id="asst_xyz789"
)

while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id="thread_abc123",
        run_id=run.id
    )

# Handle required action (function calls)
if run.status == "requires_action":
    tool_outputs = []
    for call in run.required_action.submit_tool_outputs.tool_calls:
        # Process function call
        result = process_function(call.function.name, call.function.arguments)
        tool_outputs.append({
            "tool_call_id": call.id,
            "output": result
        })
    
    run = client.beta.threads.runs.submit_tool_outputs(
        thread_id="thread_abc123",
        run_id=run.id,
        tool_outputs=tool_outputs
    )
```

## Response Examples

```json
{
  "id": "run_abc123",
  "object": "thread.run",
  "created_at": 1700000000,
  "thread_id": "thread_xyz",
  "assistant_id": "asst_123",
  "status": "completed",
  "required_action": null,
  "model": "gpt-4o",
  "instructions": "You are helpful.",
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50,
    "total_tokens": 150
  }
}
```

## Related Endpoints

- `_INFO_OAIAPI_RUN_STEPS.md` - Detailed run steps
- `_INFO_OAIAPI_ASSISTANTS_STREAMING.md` - Streaming runs

## Sources

- OAIAPI-IN01-SC-OAI-RUNS - Official runs documentation

## Document History

**[2026-01-30 10:25]**
- Initial documentation created
