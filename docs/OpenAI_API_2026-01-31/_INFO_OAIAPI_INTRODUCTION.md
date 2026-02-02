# INFO: OpenAI API - Introduction

**Doc ID**: OAIAPI-IN02
**Goal**: Document API overview, base URL, and versioning
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The OpenAI API provides RESTful, streaming, and realtime interfaces for interacting with OpenAI's AI models. The REST API uses standard HTTP methods with JSON request/response bodies, accessible from any environment that supports HTTP. The base URL for all API requests is `https://api.openai.com/v1/`. The current REST API version is `2020-10-01`, returned in the `openai-version` response header. Official SDKs are available for Python, Node.js/TypeScript, and other languages, providing idiomatic access to API functionality. The API supports three interaction patterns: synchronous REST for request-response workflows, Server-Sent Events (SSE) for streaming token-by-token responses, and WebSocket connections for real-time voice and audio interactions.

## Key Facts

- **Base URL**: `https://api.openai.com/v1/` [VERIFIED]
- **API Version**: `2020-10-01` (returned in `openai-version` header) [VERIFIED]
- **Protocol**: REST over HTTPS [VERIFIED]
- **Content-Type**: `application/json` [VERIFIED]
- **SDK Languages**: Python, Node.js/TypeScript, and community SDKs [VERIFIED]

## Use Cases

- **Chat applications**: Build conversational AI using Chat Completions or Responses API
- **Content generation**: Generate text, images, audio, and video
- **Semantic search**: Create embeddings for similarity search and RAG
- **Voice applications**: Real-time voice interactions via Realtime API
- **Batch processing**: Cost-efficient bulk processing via Batch API

## Quick Reference

### Base URL

```
https://api.openai.com/v1/
```

### API Patterns

- **REST**: Standard request-response, JSON payloads
- **Streaming**: Server-Sent Events (SSE) for real-time token delivery
- **Realtime**: WebSocket for voice and live interactions

### Official SDKs

- **Python**: `pip install openai`
- **Node.js**: `npm install openai`
- **Other**: See https://platform.openai.com/docs/libraries

## Request Examples

### cURL

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Python

```python
from openai import OpenAI

client = OpenAI()

models = client.models.list()
print(models)
```

### TypeScript/Node.js

```typescript
import OpenAI from "openai";

const client = new OpenAI();

async function main() {
  const models = await client.models.list();
  console.log(models);
}

main();
```

## Related Endpoints

- `_INFO_OAIAPI_AUTHENTICATION.md` - How to authenticate requests
- `_INFO_OAIAPI_SDKS.md` - Official SDK documentation

## Sources

- OAIAPI-IN01-SC-OAI-INTRO - Official introduction documentation
- OAIAPI-IN01-SC-OAI-LIBS - SDK and libraries documentation

## Document History

**[2026-01-30 09:25]**
- Initial documentation created from API reference
