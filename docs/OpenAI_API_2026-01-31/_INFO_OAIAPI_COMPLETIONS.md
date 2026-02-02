# INFO: OpenAI API - Completions (Legacy)

**Doc ID**: OAIAPI-IN62
**Goal**: Document legacy Completions API endpoint
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Completions API is the legacy text generation endpoint, superseded by Chat Completions. It generates text continuations from prompts without conversation structure. While still functional, new applications should use Chat Completions or Responses API instead.

## Key Facts

- **Status**: Legacy (deprecated for new development) [VERIFIED]
- **Endpoint**: `POST /v1/completions` [VERIFIED]
- **Replacement**: Chat Completions API [VERIFIED]

## Quick Reference

### Endpoint

```
POST /v1/completions
```

### Parameters

- `model` (string, required) - Model ID
- `prompt` (string/array, required) - Text prompt
- `max_tokens` (integer) - Max tokens to generate
- `temperature` (number) - Sampling temperature
- `top_p` (number) - Nucleus sampling
- `n` (integer) - Number of completions
- `stop` (string/array) - Stop sequences
- `suffix` (string) - Text to append after completion

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Once upon a time",
    max_tokens=100
)

print(response.choices[0].text)
```

## Response Examples

```json
{
  "id": "cmpl-abc123",
  "object": "text_completion",
  "created": 1700000000,
  "model": "gpt-3.5-turbo-instruct",
  "choices": [
    {
      "text": " there was a brave knight...",
      "index": 0,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 50,
    "total_tokens": 55
  }
}
```

## Migration to Chat Completions

Replace prompt-based completions with message-based:

```python
# Legacy
response = client.completions.create(
    model="gpt-3.5-turbo-instruct",
    prompt="Write a poem about the ocean"
)

# Modern
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a poem about the ocean"}]
)
```

## Sources

- OAIAPI-IN01-SC-OAI-COMPL - Official completions documentation

## Document History

**[2026-01-30 11:45]**
- Initial documentation created
