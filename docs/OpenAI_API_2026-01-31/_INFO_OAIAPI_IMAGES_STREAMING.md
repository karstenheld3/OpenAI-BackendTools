# INFO: OpenAI API - Image Streaming

**Doc ID**: OAIAPI-IN49
**Goal**: Document Image Streaming API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_IMAGES.md [OAIAPI-IN17]` for context

## Summary

Image Streaming enables progressive image generation delivery. Instead of waiting for the full image, partial results are streamed as the generation progresses. This improves perceived latency for interactive applications.

## Key Facts

- **Protocol**: Server-Sent Events [VERIFIED]
- **Enable**: `stream: true` in request [VERIFIED]

## Quick Reference

### Enable Streaming

```json
{
  "model": "dall-e-3",
  "prompt": "A mountain landscape",
  "stream": true
}
```

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

stream = client.images.generate(
    model="dall-e-3",
    prompt="A serene mountain landscape",
    stream=True
)

for event in stream:
    if event.type == "image.partial":
        # Display partial image
        display_partial(event.data)
    elif event.type == "image.complete":
        print(f"Final: {event.data.url}")
```

## Sources

- OAIAPI-IN01-SC-OAI-IMGSTR - Official image streaming documentation

## Document History

**[2026-01-30 11:25]**
- Initial documentation created
