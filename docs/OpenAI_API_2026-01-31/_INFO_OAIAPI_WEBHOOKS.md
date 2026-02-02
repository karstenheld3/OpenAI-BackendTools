# INFO: OpenAI API - Webhooks

**Doc ID**: OAIAPI-IN27
**Goal**: Document Webhook Events API
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

Webhooks enable receiving notifications when events occur in your OpenAI resources. When configured, OpenAI sends HTTP POST requests to your specified URL when events like batch completions or fine-tuning job status changes occur. Webhooks include signature headers for verification and support retry logic for failed deliveries.

## Key Facts

- **Method**: HTTP POST to your endpoint [VERIFIED]
- **Verification**: Signature in headers [VERIFIED]
- **Retry**: Automatic retry on failure [VERIFIED]

## Use Cases

- **Batch completion**: Get notified when batch jobs finish
- **Fine-tuning**: Track job progress without polling
- **Async workflows**: Event-driven processing

## Event Types

- `batch.completed` - Batch job finished
- `batch.failed` - Batch job failed
- `fine_tuning.job.succeeded` - Fine-tuning complete
- `fine_tuning.job.failed` - Fine-tuning failed

## Webhook Payload

```json
{
  "id": "evt_abc123",
  "object": "event",
  "type": "batch.completed",
  "created_at": 1700000000,
  "data": {
    "id": "batch_xyz789",
    "object": "batch",
    ...
  }
}
```

## Signature Verification

Verify webhook authenticity using the signature header.

```python
import hmac
import hashlib

def verify_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)
```

## Sources

- OAIAPI-IN01-SC-OAI-WEBHK - Official webhooks documentation

## Document History

**[2026-01-30 10:35]**
- Initial documentation created
