# INFO: OpenAI API - Chat Completions

**Doc ID**: OAIAPI-IN06
**Goal**: Document Chat Completions API endpoint and usage
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references
- `_INFO_OAIAPI_AUTHENTICATION.md` for auth requirements

## Summary

The Chat Completions API generates model responses from a list of messages comprising a conversation. It is the primary interface for text generation with GPT models, supporting text, image, and audio inputs depending on the model. The endpoint `POST /v1/chat/completions` accepts messages with roles (system, user, assistant, tool) and returns generated completions. Key features include function calling for tool use, structured outputs via JSON schema, streaming for real-time token delivery, and logprobs for token probability analysis. While widely used, OpenAI now recommends the newer Responses API for new projects. The API supports CRUD operations: create, get, list, update, and delete completions. Models like gpt-4o, gpt-4o-mini, o3, and o4-mini are supported, with parameter availability varying by model (especially for reasoning models).

## Key Facts

- **Endpoint**: `POST https://api.openai.com/v1/chat/completions` [VERIFIED]
- **Required parameters**: `messages` (array), `model` (string) [VERIFIED]
- **Message roles**: system, user, assistant, tool [VERIFIED]
- **Supported models**: gpt-4o, gpt-4o-mini, o3, o4-mini, and more [VERIFIED]
- **Recommendation**: Use Responses API for new projects [VERIFIED]

## Use Cases

- **Chatbots**: Build conversational AI with multi-turn context
- **Content generation**: Generate articles, summaries, creative writing
- **Code assistance**: Generate, explain, or debug code
- **Function calling**: Integrate with external tools and APIs
- **Structured data extraction**: Extract JSON from unstructured text

## Quick Reference

### Endpoints

- `POST /v1/chat/completions` - Create chat completion
- `GET /v1/chat/completions/{id}` - Get chat completion
- `GET /v1/chat/completions/{id}/messages` - Get chat messages
- `GET /v1/chat/completions` - List chat completions
- `POST /v1/chat/completions/{id}` - Update chat completion
- `DELETE /v1/chat/completions/{id}` - Delete chat completion

### Required Parameters

- `messages` (array, required) - List of messages in the conversation
- `model` (string, required) - Model ID (e.g., `gpt-4o`, `o3`)

### Key Optional Parameters

- `temperature` (number, 0-2) - Sampling temperature. Default: 1
- `max_tokens` (integer) - Maximum tokens to generate
- `top_p` (number) - Nucleus sampling parameter
- `n` (integer) - Number of completions to generate. Default: 1
- `stream` (boolean) - Enable streaming. Default: false
- `stop` (string/array) - Stop sequences
- `presence_penalty` (number, -2 to 2) - Penalty for new topics
- `frequency_penalty` (number, -2 to 2) - Penalty for repetition
- `tools` (array) - List of tools (functions) available
- `tool_choice` (string/object) - Control tool use
- `response_format` (object) - Force JSON output or schema
- `logprobs` (boolean) - Return log probabilities
- `seed` (integer) - For reproducible outputs

## Message Roles

- **system** - Sets behavior and context for the assistant
- **user** - Messages from the human user
- **assistant** - Previous responses from the model
- **tool** - Results from tool/function calls

## Endpoints

### Create Chat Completion

**Request**

```
POST /v1/chat/completions
```

**Headers**

- `Authorization: Bearer $OPENAI_API_KEY` (required)
- `Content-Type: application/json` (required)

**Request Body**

- `messages` (array, required) - Conversation messages
  - `role` (string) - One of: system, user, assistant, tool
  - `content` (string/array) - Message content (text or multimodal)
  - `name` (string, optional) - Participant name
  - `tool_calls` (array, optional) - Tool calls made by assistant
  - `tool_call_id` (string, optional) - ID for tool response
- `model` (string, required) - Model ID
- `temperature` (number, optional) - Sampling temperature (0-2)
- `max_tokens` (integer, optional) - Max tokens to generate
- `tools` (array, optional) - Available tools/functions
- `response_format` (object, optional) - Output format control

**Response**

- `id` (string) - Unique completion ID (e.g., `chatcmpl-...`)
- `object` (string) - Always `chat.completion`
- `created` (integer) - Unix timestamp
- `model` (string) - Model used
- `choices` (array) - Generated completions
  - `index` (integer) - Choice index
  - `message` (object) - Generated message
  - `finish_reason` (string) - stop, length, tool_calls, content_filter
  - `logprobs` (object, optional) - Log probabilities
- `usage` (object) - Token usage
  - `prompt_tokens` (integer)
  - `completion_tokens` (integer)
  - `total_tokens` (integer)

## Request Examples

### Basic Chat (cURL)

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### TypeScript/Node.js

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function main() {
  const response = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "Hello!" },
    ],
  });

  console.log(response.choices[0].message.content);
}

main();
```

### With Function Calling

```python
from openai import OpenAI

client = OpenAI()

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "City name"},
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)
```

### With Structured Output (JSON Schema)

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Extract: John is 30 years old"}],
    response_format={
        "type": "json_schema",
        "json_schema": {
            "name": "person",
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "age": {"type": "integer"}
                },
                "required": ["name", "age"]
            }
        }
    }
)
```

## Response Examples

### Success Response

```json
{
  "id": "chatcmpl-AyPNinnUqUDYo9SAdA52NobMflmj2",
  "object": "chat.completion",
  "created": 1738960610,
  "model": "gpt-4o-2024-08-06",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I help you today?"
      },
      "finish_reason": "stop",
      "logprobs": null
    }
  ],
  "usage": {
    "prompt_tokens": 13,
    "completion_tokens": 18,
    "total_tokens": 31
  },
  "system_fingerprint": "fp_50cad350e4"
}
```

### Finish Reasons

- `stop` - Natural completion or stop sequence
- `length` - Max tokens reached
- `tool_calls` - Model wants to call a tool
- `content_filter` - Content was filtered

## Error Codes

- `400 Bad Request` - Invalid parameters or message format
- `401 Unauthorized` - Invalid API key
- `403 Forbidden` - Model access not allowed
- `404 Not Found` - Completion ID not found
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - OpenAI server error

## Limitations and Known Issues

- **[COMMUNITY: OAIAPI-IN01-SC-SO-429]** - Rate limit errors (429) often indicate billing/credit issues, not just request volume
- **[COMMUNITY: OAIAPI-IN01-SC-SO-400]** - 400 errors can occur from malformed message arrays or unsupported parameters for specific models
- Reasoning models (o3, o4) have different parameter support - check reasoning guide

## Gotchas and Quirks

- `max_tokens` must be set explicitly for long outputs; defaults vary by model
- `temperature` and `top_p` should not both be modified together
- Function/tool names must match regex: `^[a-zA-Z0-9_-]+$`
- `seed` provides deterministic outputs but isn't guaranteed identical across API versions

## Related Endpoints

- `_INFO_OAIAPI_CHAT_STREAMING.md` - Streaming responses
- `_INFO_OAIAPI_RESPONSES.md` - Recommended for new projects
- `_INFO_OAIAPI_COMPLETIONS.md` - Legacy completions (deprecated)

## Sources

- OAIAPI-IN01-SC-OAI-CHAT - Official Chat Completions documentation
- OAIAPI-IN01-SC-SO-429 - Rate limit error handling
- OAIAPI-IN01-SC-SO-400 - Bad request troubleshooting

## Document History

**[2026-01-30 09:30]**
- Initial documentation created from API reference
