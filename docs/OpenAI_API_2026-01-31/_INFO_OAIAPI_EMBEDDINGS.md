# INFO: OpenAI API - Embeddings

**Doc ID**: OAIAPI-IN08
**Goal**: Document Embeddings API endpoint
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Embeddings API generates vector representations of text that capture semantic meaning, enabling similarity search, clustering, and retrieval-augmented generation (RAG) workflows. The endpoint `POST /v1/embeddings` accepts text input and returns a list of floating-point vectors. Models include `text-embedding-3-small` (1536 dimensions by default), `text-embedding-3-large` (3072 dimensions), and the legacy `text-embedding-ada-002`. The newer text-embedding-3 models support custom dimensions via the `dimensions` parameter, allowing trade-offs between performance and storage. Input limits are 8192 tokens per input with a maximum of 300,000 tokens across all inputs in a single request. Output format can be `float` or `base64` encoded.

## Key Facts

- **Endpoint**: `POST https://api.openai.com/v1/embeddings` [VERIFIED]
- **Required parameters**: `input` (string/array), `model` (string) [VERIFIED]
- **Max tokens per input**: 8192 [VERIFIED]
- **Max total tokens per request**: 300,000 [VERIFIED]
- **Max array dimensions**: 2048 [VERIFIED]

## Use Cases

- **Semantic search**: Find similar documents by vector distance
- **RAG**: Retrieve relevant context for LLM prompts
- **Clustering**: Group similar texts together
- **Classification**: Use embeddings as features for ML models
- **Recommendations**: Find similar items based on descriptions

## Quick Reference

### Models

- `text-embedding-3-small` - 1536 dimensions (default), lower cost
- `text-embedding-3-large` - 3072 dimensions, higher quality
- `text-embedding-ada-002` - 1536 dimensions, legacy

### Required Parameters

- `input` (string/array, required) - Text to embed
- `model` (string, required) - Embedding model ID

### Optional Parameters

- `dimensions` (integer) - Output dimensions (text-embedding-3 only)
- `encoding_format` (string) - `float` (default) or `base64`
- `user` (string) - End-user identifier for abuse monitoring

## Endpoints

### Create Embeddings

**Request**

```
POST /v1/embeddings
```

**Headers**

- `Authorization: Bearer $OPENAI_API_KEY` (required)
- `Content-Type: application/json` (required)

**Request Body**

- `input` (string/array, required) - Text or array of texts
- `model` (string, required) - Model ID
- `dimensions` (integer, optional) - Custom dimension count
- `encoding_format` (string, optional) - Output format

**Response**

- `object` (string) - Always `list`
- `data` (array) - Embedding objects
  - `object` (string) - Always `embedding`
  - `embedding` (array) - Vector of floats
  - `index` (integer) - Position in input array
- `model` (string) - Model used
- `usage` (object) - Token counts
  - `prompt_tokens` (integer)
  - `total_tokens` (integer)

## Request Examples

### cURL

```bash
curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "The food was delicious",
    "model": "text-embedding-3-small"
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    input="The food was delicious",
    model="text-embedding-3-small"
)

embedding = response.data[0].embedding
print(f"Dimensions: {len(embedding)}")
```

### With Custom Dimensions

```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    input="The food was delicious",
    model="text-embedding-3-large",
    dimensions=256  # Reduce from 3072 to 256
)
```

### Batch Embedding

```python
from openai import OpenAI

client = OpenAI()

texts = ["First text", "Second text", "Third text"]

response = client.embeddings.create(
    input=texts,
    model="text-embedding-3-small"
)

for item in response.data:
    print(f"Index {item.index}: {len(item.embedding)} dimensions")
```

## Response Examples

### Success Response

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [0.0023064255, -0.009327292, ...],
      "index": 0
    }
  ],
  "model": "text-embedding-3-small",
  "usage": {
    "prompt_tokens": 8,
    "total_tokens": 8
  }
}
```

## Error Codes

- `400 Bad Request` - Empty input, too many tokens, invalid dimensions
- `401 Unauthorized` - Invalid API key
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- `dimensions` only works with text-embedding-3 models
- Empty strings are not allowed as input
- Token counting differs from chat models - use tiktoken for accurate counts
- `base64` encoding returns raw bytes, more compact for transfer

## Related Endpoints

- `_INFO_OAIAPI_VECTOR_STORES.md` - Store embeddings in OpenAI
- `_INFO_OAIAPI_BATCH.md` - Batch embedding for cost savings

## Sources

- OAIAPI-IN01-SC-OAI-EMBED - Official embeddings documentation

## Document History

**[2026-01-30 09:40]**
- Initial documentation created from API reference
