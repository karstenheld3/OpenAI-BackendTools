# INFO: OpenAI API - Assistants

**Doc ID**: OAIAPI-IN21
**Goal**: Document Assistants API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Assistants API enables building AI assistants with persistent conversation threads, built-in tools, and file handling. Assistants are configured with instructions, a model, and tools (code interpreter, file search, functions). Conversations happen in threads where messages are added and runs are executed. Runs process messages and may require action (like submitting tool outputs). The API handles conversation state, tool execution, and file management automatically. This is useful for building chatbots, coding assistants, and knowledge-base applications.

## Key Facts

- **Conversation state**: Managed via Threads [VERIFIED]
- **Built-in tools**: code_interpreter, file_search [VERIFIED]
- **Custom tools**: Function calling [VERIFIED]
- **File support**: Upload files per assistant or thread [VERIFIED]

## Use Cases

- **Customer support**: Persistent conversation with knowledge base
- **Coding assistant**: Code interpreter for execution
- **Research assistant**: File search across documents
- **Task automation**: Function calling for actions

## Quick Reference

### Endpoints

- `POST /v1/assistants` - Create assistant
- `GET /v1/assistants` - List assistants
- `GET /v1/assistants/{assistant_id}` - Get assistant
- `POST /v1/assistants/{assistant_id}` - Modify assistant
- `DELETE /v1/assistants/{assistant_id}` - Delete assistant

### Built-in Tools

- `code_interpreter` - Execute Python in sandbox
- `file_search` - Search vector stores

### Workflow

1. Create Assistant (with tools, instructions)
2. Create Thread
3. Add Messages to Thread
4. Run Assistant on Thread
5. Handle required actions (tool calls)
6. Get Messages from Thread

## Endpoints

### Create Assistant

**Request**

```
POST /v1/assistants
```

**Parameters**

- `model` (string, required) - Model ID
- `name` (string, optional) - Assistant name
- `description` (string, optional) - Description
- `instructions` (string, optional) - System instructions
- `tools` (array, optional) - Enabled tools
- `tool_resources` (object, optional) - Tool configuration
  - `code_interpreter` - Files for code interpreter
  - `file_search` - Vector stores for search
- `metadata` (object, optional) - Custom key-value pairs
- `temperature` (number, optional) - Sampling temperature
- `top_p` (number, optional) - Nucleus sampling

### List Assistants

```
GET /v1/assistants
```

### Get Assistant

```
GET /v1/assistants/{assistant_id}
```

### Modify Assistant

```
POST /v1/assistants/{assistant_id}
```

### Delete Assistant

```
DELETE /v1/assistants/{assistant_id}
```

## Request Examples

### Create Assistant (Python)

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    model="gpt-4o",
    tools=[{"type": "code_interpreter"}]
)

print(f"Assistant ID: {assistant.id}")
```

### With File Search

```python
from openai import OpenAI

client = OpenAI()

# Create vector store
vector_store = client.beta.vector_stores.create(name="Knowledge Base")

# Upload files
file = client.files.create(
    file=open("knowledge.pdf", "rb"),
    purpose="assistants"
)

client.beta.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id
)

# Create assistant with file search
assistant = client.beta.assistants.create(
    name="Knowledge Assistant",
    instructions="Answer questions using the provided documents.",
    model="gpt-4o",
    tools=[{"type": "file_search"}],
    tool_resources={
        "file_search": {"vector_store_ids": [vector_store.id]}
    }
)
```

### With Function Calling

```python
from openai import OpenAI

client = OpenAI()

assistant = client.beta.assistants.create(
    name="Weather Assistant",
    instructions="Help users get weather information.",
    model="gpt-4o",
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }]
)
```

### Complete Conversation Flow

```python
from openai import OpenAI
import time

client = OpenAI()

# 1. Create thread
thread = client.beta.threads.create()

# 2. Add message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="What is 25 * 48?"
)

# 3. Run assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id="asst_abc123"
)

# 4. Wait for completion
while run.status in ["queued", "in_progress"]:
    time.sleep(1)
    run = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    )

# 5. Get response
messages = client.beta.threads.messages.list(thread_id=thread.id)
print(messages.data[0].content[0].text.value)
```

## Response Examples

### Assistant Object

```json
{
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1700000000,
  "name": "Math Tutor",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are a personal math tutor.",
  "tools": [{"type": "code_interpreter"}],
  "tool_resources": {},
  "metadata": {}
}
```

## Error Codes

- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Assistant not found
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- Assistants API is in beta (`client.beta.assistants`)
- Threads persist until deleted
- Runs may require action (tool calls)
- File search requires vector stores
- Code interpreter has execution time limits

## Related Endpoints

- `_INFO_OAIAPI_THREADS.md` - Thread management
- `_INFO_OAIAPI_MESSAGES.md` - Message handling
- `_INFO_OAIAPI_RUNS.md` - Run execution
- `_INFO_OAIAPI_VECTOR_STORES.md` - File search setup

## Sources

- OAIAPI-IN01-SC-OAI-ASSIST - Official assistants documentation

## Document History

**[2026-01-30 10:15]**
- Initial documentation created
