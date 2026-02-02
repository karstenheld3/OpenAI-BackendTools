# INFO: OpenAI API - Chat Completions Streaming

**Doc ID**: OAIAPI-IN07
**Goal**: Document streaming for Chat Completions API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_CHAT.md [OAIAPI-IN06]` for base endpoint

## Summary

Chat Completions streaming enables real-time delivery of model responses using Server-Sent Events (SSE). When `stream: true` is set in the request, the API returns chunks of the completion as they are generated, each containing a delta of the content. This allows applications to display responses progressively rather than waiting for the full completion. Each chunk is a `chat.completion.chunk` object sharing the same ID and timestamp as other chunks in the stream. The final chunk contains an empty delta and a `finish_reason`. Usage statistics can be included in the final chunk by setting `stream_options: {"include_usage": true}`.

## Key Facts

- **Protocol**: Server-Sent Events (SSE) [VERIFIED]
- **Object type**: `chat.completion.chunk` [VERIFIED]
- **Enable streaming**: `stream: true` in request [VERIFIED]
- **Usage in stream**: Set `stream_options: {"include_usage": true}` [VERIFIED]
- **Chunk ID**: Same across all chunks in a completion [VERIFIED]

## Use Cases

- **Chat interfaces**: Display responses as they're generated
- **Long responses**: Show progress for lengthy completions
- **Low latency perception**: Improve user experience with immediate feedback

## Quick Reference

### Enable Streaming

```json
{
  "model": "gpt-4o",
  "messages": [...],
  "stream": true,
  "stream_options": {"include_usage": true}
}
```

### Chunk Object Properties

- `id` (string) - Unique completion ID (same for all chunks)
- `object` (string) - Always `chat.completion.chunk`
- `created` (integer) - Unix timestamp (same for all chunks)
- `model` (string) - Model used
- `choices` (array) - Delta content
  - `index` (integer) - Choice index
  - `delta` (object) - Incremental content
    - `role` (string) - Only in first chunk
    - `content` (string) - Text delta
    - `tool_calls` (array) - Tool call deltas
  - `finish_reason` (string/null) - null until final chunk
- `usage` (object/null) - Only with `include_usage: true` on final chunk

### Finish Reasons

- `stop` - Natural completion
- `length` - Max tokens reached
- `tool_calls` - Tool call requested
- `content_filter` - Content filtered

## Request Examples

### cURL

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": true
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI()

stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### TypeScript/Node.js

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function main() {
  const stream = await client.chat.completions.create({
    model: "gpt-4o",
    messages: [{ role: "user", content: "Hello" }],
    stream: true,
  });

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content || "";
    process.stdout.write(content);
  }
}

main();
```

## Response Examples

### Stream Chunks

```
data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{"role":"assistant","content":""},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}

data: {"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}

data: [DONE]
```

## Gotchas and Quirks

- First chunk contains `role` in delta, subsequent chunks contain only `content`
- Final chunk has empty delta `{}` with `finish_reason` set
- `choices` array may be empty in final chunk when `include_usage` is true
- SSE format: each chunk prefixed with `data: `, stream ends with `data: [DONE]`
- `system_fingerprint` is deprecated but still returned

## Limitations and Known Issues

- **[COMMUNITY: OAIAPI-IN01-SC-SO-STREAM]** - Streaming appears to buffer entire response in some inspection scenarios; this is expected SSE behavior
- **[COMMUNITY: OAIAPI-IN01-SC-FORUM-STRGUIDE]** - Tool call streaming requires assembling partial function arguments across chunks

## Related Endpoints

- `_INFO_OAIAPI_CHAT.md` - Non-streaming Chat Completions
- `_INFO_OAIAPI_RESPONSES_STREAMING.md` - Responses API streaming

## Sources

- OAIAPI-IN01-SC-OAI-CHATSTR - Official streaming documentation
- OAIAPI-IN01-SC-SO-STREAM - Streaming implementation questions
- OAIAPI-IN01-SC-FORUM-STRGUIDE - Community streaming guide

## Document History

**[2026-01-30 09:35]**
- Initial documentation created from API reference
