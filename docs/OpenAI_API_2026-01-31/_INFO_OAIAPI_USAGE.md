# INFO: OpenAI API - Usage

**Doc ID**: OAIAPI-IN35
**Goal**: Document Usage API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_ADMINISTRATION.md [OAIAPI-IN30]` for context

## Summary

The Usage API provides detailed metrics on API consumption across models, projects, and time periods. This enables cost tracking, capacity planning, and usage analysis. Metrics include token counts, request counts, and costs broken down by model and date.

## Key Facts

- **Granularity**: Per model, project, day [VERIFIED]
- **Metrics**: Tokens, requests, costs [VERIFIED]
- **History**: Access historical usage data [VERIFIED]

## Quick Reference

### Endpoints

- `GET /v1/organization/usage/completions` - Completion usage
- `GET /v1/organization/usage/embeddings` - Embedding usage
- `GET /v1/organization/usage/images` - Image usage
- `GET /v1/organization/usage/audio_speeches` - TTS usage
- `GET /v1/organization/usage/audio_transcriptions` - Transcription usage

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()  # Using admin API key

# Get completion usage
usage = client.organization.usage.completions.list(
    start_time="2026-01-01",
    end_time="2026-01-31"
)

for bucket in usage.data:
    print(f"{bucket.start_time}: {bucket.results}")
```

## Response Examples

```json
{
  "object": "page",
  "data": [
    {
      "object": "bucket",
      "start_time": 1704067200,
      "end_time": 1704153600,
      "results": [
        {
          "object": "organization.usage.completions.result",
          "input_tokens": 50000,
          "output_tokens": 25000,
          "num_model_requests": 100,
          "project_id": "proj_abc123"
        }
      ]
    }
  ]
}
```

## Sources

- OAIAPI-IN01-SC-OAI-USAGE - Official usage documentation

## Document History

**[2026-01-30 10:55]**
- Initial documentation created
