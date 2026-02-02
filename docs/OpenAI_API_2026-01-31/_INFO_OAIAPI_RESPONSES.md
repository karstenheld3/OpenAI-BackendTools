# INFO: OpenAI API - Responses

**Doc ID**: OAIAPI-IN11
**Goal**: Document Responses API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Responses API is OpenAI's recommended interface for new projects, providing a unified way to create model responses with support for text, images, audio, and tool use. Unlike Chat Completions, it offers built-in conversation state management via `previous_response_id`, background processing mode, and response compaction for long conversations. The endpoint `POST /v1/responses` accepts flexible input types and returns structured output items. Key features include native tool support (web_search, code_interpreter, file_search, computer_use, mcp), reasoning configuration for o-series models, and streaming via Server-Sent Events. Responses can be retrieved, cancelled, deleted, and compacted. The API supports both synchronous and background processing modes.

## Key Facts

- **Endpoint**: `POST https://api.openai.com/v1/responses` [VERIFIED]
- **Required parameters**: `model` (string), `input` (string/array) [VERIFIED]
- **Recommended for**: New projects (over Chat Completions) [VERIFIED]
- **Conversation state**: Via `previous_response_id` [VERIFIED]
- **Background mode**: Set `background: true` for async processing [VERIFIED]

## Use Cases

- **Conversational AI**: Multi-turn conversations with automatic state
- **Tool-augmented generation**: Web search, code execution, file retrieval
- **Reasoning tasks**: Extended thinking with o-series models
- **Long conversations**: Compact responses to manage context
- **Background processing**: Async generation with webhooks

## Quick Reference

### Endpoints

- `POST /v1/responses` - Create a model response
- `GET /v1/responses/{response_id}` - Get a response
- `DELETE /v1/responses/{response_id}` - Delete a response
- `POST /v1/responses/{response_id}/cancel` - Cancel a response
- `POST /v1/responses/{response_id}/compact` - Compact a response
- `GET /v1/responses/{response_id}/input_items` - List input items
- `GET /v1/responses/{response_id}/input_tokens` - Get token counts

### Required Parameters

- `model` (string, required) - Model ID (e.g., `gpt-4o`, `o3`)
- `input` (string/array, required) - Text or structured input items

### Key Optional Parameters

- `instructions` (string) - System instructions
- `previous_response_id` (string) - Link to previous response for conversation
- `tools` (array) - Available tools
- `stream` (boolean) - Enable streaming. Default: false
- `background` (boolean) - Background processing mode
- `reasoning` (object) - Reasoning configuration for o-series
- `max_output_tokens` (integer) - Maximum tokens to generate
- `temperature` (number) - Sampling temperature
- `metadata` (object) - Custom key-value pairs

### Built-in Tools

- `web_search` - Search the web
- `code_interpreter` - Execute code in sandbox
- `file_search` - Search vector stores
- `computer_use` - Computer control (preview)
- `mcp` - Model Context Protocol servers

## Input Types

- **Text string**: Simple text input
- **Message objects**: Structured messages with role and content
- **Content arrays**: Multi-modal (text, images, audio, files)

### Input Content Types

- `input_text` - Text content
- `input_image` - Image (URL or base64)
- `input_audio` - Audio content
- `input_file` - File reference

## Endpoints

### Create Response

**Request**

```
POST /v1/responses
```

**Request Body**

- `model` (string, required) - Model ID
- `input` (string/array, required) - Input content
- `instructions` (string, optional) - System instructions
- `tools` (array, optional) - Available tools
- `previous_response_id` (string, optional) - Conversation continuation
- `stream` (boolean, optional) - Enable streaming
- `background` (boolean, optional) - Background mode
- `reasoning` (object, optional) - Reasoning config for o-series
- `max_output_tokens` (integer, optional) - Max tokens
- `temperature` (number, optional) - Sampling temperature

**Response**

- `id` (string) - Response ID (e.g., `resp_...`)
- `object` (string) - Always `response`
- `status` (string) - `completed`, `in_progress`, `failed`, `cancelled`
- `output` (array) - Output items
- `usage` (object) - Token usage
- `created_at` (integer) - Unix timestamp

### Get Response

```
GET /v1/responses/{response_id}
```

### Delete Response

```
DELETE /v1/responses/{response_id}
```

### Cancel Response

```
POST /v1/responses/{response_id}/cancel
```

### Compact Response

```
POST /v1/responses/{response_id}/compact
```

Compacts long conversations by summarizing earlier context.

## Request Examples

### Basic Request (cURL)

```bash
curl https://api.openai.com/v1/responses \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "input": "Tell me a three sentence bedtime story about a unicorn."
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="Tell me a bedtime story about a unicorn."
)

print(response.output[0].content[0].text)
```

### With Instructions

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    instructions="You are a helpful assistant that speaks like a pirate.",
    input="How do I make pasta?"
)
```

### Multi-turn Conversation

```python
from openai import OpenAI

client = OpenAI()

# First message
response1 = client.responses.create(
    model="gpt-4o",
    input="My name is Alice."
)

# Continue conversation
response2 = client.responses.create(
    model="gpt-4o",
    input="What is my name?",
    previous_response_id=response1.id
)
```

### With Tools

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    input="What's the weather in Paris?",
    tools=[{"type": "web_search"}]
)
```

### Background Mode

```python
from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="o3",
    input="Solve this complex problem...",
    background=True,
    reasoning={"effort": "high"}
)

# Poll for completion
while response.status == "in_progress":
    response = client.responses.retrieve(response.id)
```

## Response Examples

### Success Response

```json
{
  "id": "resp_67890",
  "object": "response",
  "created_at": 1741476542,
  "status": "completed",
  "model": "gpt-4o-2024-08-06",
  "output": [
    {
      "type": "message",
      "id": "msg_123",
      "role": "assistant",
      "content": [
        {
          "type": "output_text",
          "text": "Once upon a time, a unicorn..."
        }
      ]
    }
  ],
  "usage": {
    "input_tokens": 328,
    "output_tokens": 52,
    "total_tokens": 380
  }
}
```

## Error Codes

- `400 Bad Request` - Invalid parameters
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Response not found
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- `previous_response_id` only works with responses from the same model family
- Background mode requires polling or webhooks for completion
- Compaction is useful for conversations exceeding context limits
- Output structure differs from Chat Completions (uses `output` array)

## Related Endpoints

- `_INFO_OAIAPI_CONVERSATIONS.md` - Conversation management
- `_INFO_OAIAPI_RESPONSES_STREAMING.md` - Streaming events
- `_INFO_OAIAPI_CHAT.md` - Legacy Chat Completions

## Sources

- OAIAPI-IN01-SC-OAI-RESP - Official Responses documentation

## Document History

**[2026-01-30 09:45]**
- Initial documentation created from API reference
