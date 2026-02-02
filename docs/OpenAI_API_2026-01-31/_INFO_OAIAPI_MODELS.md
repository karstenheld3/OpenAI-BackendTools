# INFO: OpenAI API - Models

**Doc ID**: OAIAPI-IN09
**Goal**: Document Models API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Models API provides endpoints to list, retrieve, and delete models available in the OpenAI API. The list endpoint returns all models accessible to the user, including base models and fine-tuned models. Each model object includes its ID, owner, and creation timestamp. Fine-tuned models can be deleted by their owner, but base OpenAI models cannot be deleted. Model IDs are used in other API calls (chat completions, embeddings, etc.) to specify which model to use for generation.

## Key Facts

- **Base URL**: `https://api.openai.com/v1/models` [VERIFIED]
- **List models**: `GET /v1/models` [VERIFIED]
- **Get model**: `GET /v1/models/{model}` [VERIFIED]
- **Delete model**: `DELETE /v1/models/{model}` (fine-tuned only) [VERIFIED]

## Use Cases

- **Model discovery**: List available models for selection
- **Validation**: Check if a model exists before use
- **Cleanup**: Delete unused fine-tuned models
- **Inventory**: Track fine-tuned model creation

## Quick Reference

### Endpoints

- `GET /v1/models` - List all models
- `GET /v1/models/{model}` - Get model details
- `DELETE /v1/models/{model}` - Delete fine-tuned model

### Model Object Properties

- `id` (string) - Model identifier (e.g., `gpt-4o`)
- `object` (string) - Always `model`
- `created` (integer) - Unix timestamp
- `owned_by` (string) - Owner (e.g., `openai`, `organization-xxx`)

## Endpoints

### List Models

**Request**

```
GET /v1/models
```

**Response**

- `object` (string) - Always `list`
- `data` (array) - Model objects

### Get Model

**Request**

```
GET /v1/models/{model}
```

**Response**

Returns model object with `id`, `object`, `created`, `owned_by`.

### Delete Model

**Request**

```
DELETE /v1/models/{model}
```

**Response**

- `id` (string) - Deleted model ID
- `object` (string) - Always `model`
- `deleted` (boolean) - Always `true`

## Request Examples

### List Models (cURL)

```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Python

```python
from openai import OpenAI

client = OpenAI()

# List all models
models = client.models.list()
for model in models.data:
    print(model.id)

# Get specific model
model = client.models.retrieve("gpt-4o")
print(f"Created: {model.created}")

# Delete fine-tuned model
deleted = client.models.delete("ft:gpt-4o-mini:my-org:custom:id")
print(f"Deleted: {deleted.deleted}")
```

## Response Examples

### List Response

```json
{
  "object": "list",
  "data": [
    {
      "id": "gpt-4o",
      "object": "model",
      "created": 1686935002,
      "owned_by": "openai"
    },
    {
      "id": "ft:gpt-4o-mini:my-org::abc123",
      "object": "model",
      "created": 1699000000,
      "owned_by": "organization-abc"
    }
  ]
}
```

## Error Codes

- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Model does not exist
- `403 Forbidden` - Cannot delete (not owner or base model)

## Gotchas and Quirks

- Only fine-tuned models can be deleted
- Model list includes deprecated models
- Fine-tuned model IDs follow format: `ft:{base}:{org}:{suffix}:{id}`

## Related Endpoints

- `_INFO_OAIAPI_FINE_TUNING.md` - Create fine-tuned models
- `_INFO_OAIAPI_CHAT.md` - Use models for completions

## Sources

- OAIAPI-IN01-SC-OAI-MODELS - Official models documentation

## Document History

**[2026-01-30 09:40]**
- Initial documentation created
