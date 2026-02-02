# INFO: OpenAI API - Videos

**Doc ID**: OAIAPI-IN37
**Goal**: Document Videos API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Videos API enables AI-powered video generation from text prompts. Videos are generated asynchronously, requiring polling or webhooks to track completion. The API supports various styles and durations.

## Key Facts

- **Generation**: Async, requires polling [VERIFIED]
- **Models**: Sora-based generation [VERIFIED]
- **Output**: MP4 format [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/videos/generations` - Create video
- `GET /v1/videos/generations/{id}` - Get generation status

## Request Examples

### Python

```python
from openai import OpenAI
import time

client = OpenAI()

# Create video generation
generation = client.videos.generations.create(
    model="sora",
    prompt="A serene beach at sunset with gentle waves"
)

# Poll for completion
while generation.status == "in_progress":
    time.sleep(30)
    generation = client.videos.generations.retrieve(generation.id)

if generation.status == "completed":
    print(f"Video URL: {generation.url}")
```

## Sources

- OAIAPI-IN01-SC-OAI-VIDEO - Official videos documentation

## Document History

**[2026-01-30 11:00]**
- Initial documentation created
