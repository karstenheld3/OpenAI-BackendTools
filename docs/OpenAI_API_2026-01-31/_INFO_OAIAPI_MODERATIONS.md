# INFO: OpenAI API - Moderations

**Doc ID**: OAIAPI-IN10
**Goal**: Document Moderations API endpoint
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Moderations API classifies text for potentially harmful content across multiple categories including hate, harassment, violence, sexual content, and self-harm. The endpoint `POST /v1/moderations` accepts text input and returns category flags and confidence scores. This is useful for content filtering before displaying user-generated content or feeding it to other models. The API is free to use for monitoring inputs and outputs of OpenAI APIs. Multiple models are available with varying capabilities, including `omni-moderation-latest` for text and images.

## Key Facts

- **Endpoint**: `POST https://api.openai.com/v1/moderations` [VERIFIED]
- **Required parameter**: `input` (string/array) [VERIFIED]
- **Default model**: `omni-moderation-latest` [VERIFIED]
- **Cost**: Free for OpenAI API content monitoring [VERIFIED]

## Use Cases

- **Content filtering**: Block harmful user-generated content
- **Pre-screening**: Check prompts before sending to LLMs
- **Post-processing**: Filter model outputs before display
- **Compliance**: Meet content moderation requirements

## Quick Reference

### Categories

- `hate` - Hate speech targeting protected groups
- `hate/threatening` - Hateful content with violence
- `harassment` - Harassing content
- `harassment/threatening` - Harassment with violence
- `self-harm` - Self-harm promotion
- `self-harm/intent` - Intent to self-harm
- `self-harm/instructions` - Self-harm instructions
- `sexual` - Sexual content
- `sexual/minors` - Sexual content involving minors
- `violence` - Violent content
- `violence/graphic` - Graphic violence

### Models

- `omni-moderation-latest` - Latest, supports text and images
- `omni-moderation-2024-09-26` - Pinned version
- `text-moderation-latest` - Text only
- `text-moderation-stable` - Stable text version

## Endpoints

### Create Moderation

**Request**

```
POST /v1/moderations
```

**Request Body**

- `input` (string/array, required) - Text to classify
- `model` (string, optional) - Model ID

**Response**

- `id` (string) - Moderation ID
- `model` (string) - Model used
- `results` (array) - Classification results
  - `flagged` (boolean) - True if any category triggered
  - `categories` (object) - Boolean per category
  - `category_scores` (object) - Score (0-1) per category

## Request Examples

### cURL

```bash
curl https://api.openai.com/v1/moderations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "input": "I want to hurt someone"
  }'
```

### Python

```python
from openai import OpenAI

client = OpenAI()

response = client.moderations.create(
    input="I want to hurt someone"
)

result = response.results[0]
print(f"Flagged: {result.flagged}")

if result.flagged:
    for category, flagged in result.categories:
        if flagged:
            score = result.category_scores[category]
            print(f"  {category}: {score:.2%}")
```

### Batch Moderation

```python
from openai import OpenAI

client = OpenAI()

texts = ["Text 1", "Text 2", "Text 3"]

response = client.moderations.create(input=texts)

for i, result in enumerate(response.results):
    print(f"Text {i}: {'FLAGGED' if result.flagged else 'OK'}")
```

## Response Examples

### Success Response

```json
{
  "id": "modr-abc123",
  "model": "omni-moderation-latest",
  "results": [
    {
      "flagged": true,
      "categories": {
        "hate": false,
        "harassment": false,
        "violence": true,
        "sexual": false,
        "self-harm": false
      },
      "category_scores": {
        "hate": 0.0001,
        "harassment": 0.0003,
        "violence": 0.9234,
        "sexual": 0.0002,
        "self-harm": 0.0001
      }
    }
  ]
}
```

## Error Codes

- `400 Bad Request` - Invalid input format
- `401 Unauthorized` - Invalid API key

## Gotchas and Quirks

- Scores are not calibrated probabilities, higher = more confident
- Thresholds for `flagged` are set by OpenAI, not configurable
- Empty strings may return low scores but not flag

## Related Endpoints

- `_INFO_OAIAPI_CHAT.md` - Content to moderate

## Sources

- OAIAPI-IN01-SC-OAI-MODER - Official moderations documentation

## Document History

**[2026-01-30 09:40]**
- Initial documentation created
