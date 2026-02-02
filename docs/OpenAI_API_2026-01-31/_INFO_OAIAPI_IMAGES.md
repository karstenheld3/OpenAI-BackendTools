# INFO: OpenAI API - Images

**Doc ID**: OAIAPI-IN17
**Goal**: Document Images API endpoints (DALL-E)
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Images API enables image generation, editing, and variation creation using DALL-E models. The generation endpoint creates images from text prompts, supporting multiple sizes and quality levels. The edits endpoint modifies existing images based on prompts and masks. The variations endpoint creates alternative versions of an input image. DALL-E 3 supports higher quality and HD options, while DALL-E 2 offers more size flexibility. Images can be returned as URLs (valid for 1 hour) or base64-encoded data.

## Key Facts

- **Models**: `dall-e-3`, `dall-e-2` [VERIFIED]
- **Generation**: `POST /v1/images/generations` [VERIFIED]
- **Edits**: `POST /v1/images/edits` [VERIFIED]
- **Variations**: `POST /v1/images/variations` [VERIFIED]
- **URL validity**: 1 hour [VERIFIED]

## Use Cases

- **Content creation**: Generate images for articles, social media
- **Design**: Create concept art, mockups
- **Editing**: Modify existing images with prompts
- **Variations**: Explore alternative versions of images

## Quick Reference

### Endpoints

- `POST /v1/images/generations` - Generate images from text
- `POST /v1/images/edits` - Edit images with mask
- `POST /v1/images/variations` - Create variations

### DALL-E 3 Sizes

- `1024x1024` (square)
- `1792x1024` (landscape)
- `1024x1792` (portrait)

### DALL-E 2 Sizes

- `256x256`
- `512x512`
- `1024x1024`

### Quality Options (DALL-E 3)

- `standard` - Default, faster
- `hd` - Higher detail, slower

### Style Options (DALL-E 3)

- `vivid` - Hyper-real, dramatic
- `natural` - More natural, less dramatic

## Endpoints

### Generate Images

**Request**

```
POST /v1/images/generations
```

**Parameters**

- `prompt` (string, required) - Text description (max 4000 chars for DALL-E 3)
- `model` (string, optional) - `dall-e-3` or `dall-e-2`
- `n` (integer, optional) - Number of images (1 for DALL-E 3, 1-10 for DALL-E 2)
- `size` (string, optional) - Image dimensions
- `quality` (string, optional) - `standard` or `hd` (DALL-E 3)
- `style` (string, optional) - `vivid` or `natural` (DALL-E 3)
- `response_format` (string, optional) - `url` or `b64_json`
- `user` (string, optional) - End-user identifier

### Edit Images

**Request**

```
POST /v1/images/edits
Content-Type: multipart/form-data
```

**Parameters**

- `image` (file, required) - Original image (PNG, <4MB, square)
- `prompt` (string, required) - Edit description
- `mask` (file, optional) - Mask image (transparent areas to edit)
- `model` (string, optional) - Only `dall-e-2`
- `n` (integer, optional) - 1-10
- `size` (string, optional) - DALL-E 2 sizes
- `response_format` (string, optional) - `url` or `b64_json`

### Create Variations

**Request**

```
POST /v1/images/variations
Content-Type: multipart/form-data
```

**Parameters**

- `image` (file, required) - Source image (PNG, <4MB, square)
- `model` (string, optional) - Only `dall-e-2`
- `n` (integer, optional) - 1-10
- `size` (string, optional) - DALL-E 2 sizes
- `response_format` (string, optional) - `url` or `b64_json`

## Request Examples

### Generate Image (cURL)

```bash
curl https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A serene mountain landscape at sunset",
    "size": "1024x1024",
    "quality": "hd"
  }'
```

### Python Generation

```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A serene mountain landscape at sunset",
    size="1024x1024",
    quality="hd",
    n=1
)

image_url = response.data[0].url
print(image_url)
```

### Python with Base64

```python
from openai import OpenAI
import base64

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A cute robot",
    response_format="b64_json"
)

image_data = base64.b64decode(response.data[0].b64_json)
with open("robot.png", "wb") as f:
    f.write(image_data)
```

### Python Edit

```python
from openai import OpenAI

client = OpenAI()

response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),
    prompt="A sunlit indoor lounge area with a pool",
    n=1,
    size="1024x1024"
)

print(response.data[0].url)
```

### Python Variations

```python
from openai import OpenAI

client = OpenAI()

response = client.images.create_variation(
    model="dall-e-2",
    image=open("original.png", "rb"),
    n=3,
    size="1024x1024"
)

for i, image in enumerate(response.data):
    print(f"Variation {i}: {image.url}")
```

## Response Examples

### Generation Response

```json
{
  "created": 1700000000,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/...",
      "revised_prompt": "A serene mountain landscape at sunset, with..."
    }
  ]
}
```

## Error Codes

- `400 Bad Request` - Invalid prompt, size, or image format
- `401 Unauthorized` - Invalid API key
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- DALL-E 3 only generates 1 image per request (`n=1`)
- DALL-E 3 may revise prompts - check `revised_prompt` in response
- Edits and variations only work with DALL-E 2
- URLs expire after 1 hour - download immediately or use b64_json
- Images must be PNG for edits/variations
- Mask transparency indicates areas to edit

## Related Endpoints

- `_INFO_OAIAPI_IMAGES_STREAMING.md` - Streaming generation

## Sources

- OAIAPI-IN01-SC-OAI-IMAGE - Official images documentation

## Document History

**[2026-01-30 10:05]**
- Initial documentation created
