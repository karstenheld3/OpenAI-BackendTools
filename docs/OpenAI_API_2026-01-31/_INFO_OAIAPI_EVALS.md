# INFO: OpenAI API - Evals

**Doc ID**: OAIAPI-IN38
**Goal**: Document Evals API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

## Summary

The Evals API enables systematic evaluation of model outputs against defined criteria. Evaluations help measure model performance, compare versions, and detect regressions. Evals run against datasets with test cases and produce scored results.

## Key Facts

- **Purpose**: Measure model performance [VERIFIED]
- **Workflow**: Define eval → Run on dataset → Analyze results [VERIFIED]
- **Scoring**: Custom graders and metrics [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/evals` - Create eval
- `GET /v1/evals` - List evals
- `GET /v1/evals/{eval_id}` - Get eval
- `POST /v1/evals/{eval_id}/runs` - Create eval run
- `GET /v1/evals/{eval_id}/runs` - List runs

## Request Examples

### Python

```python
from openai import OpenAI

client = OpenAI()

# Create eval
eval = client.evals.create(
    name="Helpfulness Eval",
    data_source={
        "type": "file",
        "file_id": "file-abc123"
    },
    testing_criteria=[
        {
            "type": "grader",
            "grader_id": "grader-xyz"
        }
    ]
)

# Run eval
run = client.evals.runs.create(
    eval_id=eval.id,
    model="gpt-4o"
)
```

## Sources

- OAIAPI-IN01-SC-OAI-EVALS - Official evals documentation

## Document History

**[2026-01-30 11:00]**
- Initial documentation created
