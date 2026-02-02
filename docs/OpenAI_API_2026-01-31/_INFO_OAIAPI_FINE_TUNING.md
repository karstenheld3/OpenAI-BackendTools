# INFO: OpenAI API - Fine-tuning

**Doc ID**: OAIAPI-IN20
**Goal**: Document Fine-tuning API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Fine-tuning API enables customization of OpenAI models on your specific data. By training on example conversations, you can improve model performance for specific tasks, teach consistent formatting, and reduce prompt length requirements. Fine-tuning is available for select models including gpt-4o-mini and gpt-3.5-turbo. The workflow involves uploading a training file, creating a fine-tuning job, monitoring progress, and using the resulting custom model. Jobs produce checkpoints during training that can be used for evaluation. Fine-tuned models are billed based on training tokens and inference usage.

## Key Facts

- **Supported models**: gpt-4o-mini, gpt-3.5-turbo [VERIFIED]
- **Training format**: JSONL with messages [VERIFIED]
- **Min examples**: 10 (recommended: 50-100) [VERIFIED]
- **Job monitoring**: Via events endpoint [VERIFIED]

## Use Cases

- **Consistent formatting**: Enforce specific output structures
- **Domain expertise**: Train on specialized knowledge
- **Tone/style**: Match specific writing styles
- **Reduce prompting**: Encode instructions in model weights

## Quick Reference

### Endpoints

- `POST /v1/fine_tuning/jobs` - Create job
- `GET /v1/fine_tuning/jobs` - List jobs
- `GET /v1/fine_tuning/jobs/{job_id}` - Get job
- `POST /v1/fine_tuning/jobs/{job_id}/cancel` - Cancel job
- `GET /v1/fine_tuning/jobs/{job_id}/events` - List events
- `GET /v1/fine_tuning/jobs/{job_id}/checkpoints` - List checkpoints

### Job Statuses

- `validating_files` - Checking training data
- `queued` - Waiting to start
- `running` - Training in progress
- `succeeded` - Complete, model ready
- `failed` - Error occurred
- `cancelled` - Job cancelled

## Training Data Format

JSONL with conversation examples:

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi! How can I help?"}]}
{"messages": [{"role": "user", "content": "Summarize this"}, {"role": "assistant", "content": "Here's a summary: ..."}]}
```

### Best Practices

- Include 50-100+ examples for best results
- Cover edge cases and variations
- Use consistent formatting in outputs
- Include system messages if needed at inference
- Validate data before upload

## Endpoints

### Create Fine-tuning Job

**Request**

```
POST /v1/fine_tuning/jobs
```

**Parameters**

- `training_file` (string, required) - File ID of training data
- `model` (string, required) - Base model to fine-tune
- `validation_file` (string, optional) - File ID for validation
- `hyperparameters` (object, optional) - Training parameters
  - `n_epochs` (integer/string) - Number of epochs (default: auto)
  - `batch_size` (integer/string) - Batch size (default: auto)
  - `learning_rate_multiplier` (number/string) - LR multiplier (default: auto)
- `suffix` (string, optional) - Custom model name suffix

### Get Job

```
GET /v1/fine_tuning/jobs/{job_id}
```

### List Events

```
GET /v1/fine_tuning/jobs/{job_id}/events
```

### List Checkpoints

```
GET /v1/fine_tuning/jobs/{job_id}/checkpoints
```

## Request Examples

### Complete Workflow (Python)

```python
from openai import OpenAI

client = OpenAI()

# 1. Upload training file
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# 2. Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4o-mini",
    suffix="my-custom-model"
)

print(f"Job ID: {job.id}")

# 3. Monitor progress
import time
while job.status not in ["succeeded", "failed", "cancelled"]:
    time.sleep(60)
    job = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job.status}")

# 4. Use the model
if job.status == "succeeded":
    response = client.chat.completions.create(
        model=job.fine_tuned_model,
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)
```

### With Hyperparameters

```python
from openai import OpenAI

client = OpenAI()

job = client.fine_tuning.jobs.create(
    training_file="file-abc123",
    model="gpt-4o-mini",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": 4,
        "learning_rate_multiplier": 0.1
    }
)
```

### Monitor Events

```python
from openai import OpenAI

client = OpenAI()

events = client.fine_tuning.jobs.list_events(
    fine_tuning_job_id="ftjob-abc123",
    limit=10
)

for event in events.data:
    print(f"{event.created_at}: {event.message}")
```

### List Checkpoints

```python
from openai import OpenAI

client = OpenAI()

checkpoints = client.fine_tuning.jobs.list_checkpoints(
    fine_tuning_job_id="ftjob-abc123"
)

for cp in checkpoints.data:
    print(f"{cp.id}: step {cp.step_number}, metrics: {cp.metrics}")
```

## Response Examples

### Job Object

```json
{
  "id": "ftjob-abc123",
  "object": "fine_tuning.job",
  "model": "gpt-4o-mini",
  "created_at": 1700000000,
  "finished_at": 1700003600,
  "fine_tuned_model": "ft:gpt-4o-mini:my-org:my-custom-model:abc123",
  "organization_id": "org-123",
  "result_files": ["file-xyz789"],
  "status": "succeeded",
  "validation_file": null,
  "training_file": "file-abc123",
  "hyperparameters": {
    "n_epochs": 3,
    "batch_size": 4,
    "learning_rate_multiplier": 0.1
  },
  "trained_tokens": 50000
}
```

## Error Codes

- `400 Bad Request` - Invalid training file or parameters
- `401 Unauthorized` - Invalid API key
- `404 Not Found` - Job not found
- `429 Too Many Requests` - Rate limit exceeded

## Gotchas and Quirks

- Training time varies (minutes to hours)
- Fine-tuned models incur higher per-token costs
- Checkpoints can be used as standalone models
- Model names follow: `ft:{base}:{org}:{suffix}:{id}`
- Delete fine-tuned models via Models API when done

## Related Endpoints

- `_INFO_OAIAPI_FILES.md` - Upload training data
- `_INFO_OAIAPI_MODELS.md` - List and delete fine-tuned models

## Sources

- OAIAPI-IN01-SC-OAI-FTUNE - Official fine-tuning documentation

## Document History

**[2026-01-30 10:15]**
- Initial documentation created
