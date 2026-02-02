# INFO: OpenAI API - Graders

**Doc ID**: OAIAPI-IN39
**Goal**: Document Graders API endpoints
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `_INFO_OAIAPI_EVALS.md [OAIAPI-IN38]` for context

## Summary

Graders define scoring criteria for evaluations. They specify how model outputs should be assessed, using rubrics, model-based grading, or custom logic. Graders are reusable across multiple evals.

## Key Facts

- **Types**: Model-based, rule-based [VERIFIED]
- **Reusable**: Across multiple evals [VERIFIED]

## Quick Reference

### Endpoints

- `POST /v1/graders` - Create grader
- `GET /v1/graders` - List graders
- `GET /v1/graders/{grader_id}` - Get grader

## Sources

- OAIAPI-IN01-SC-OAI-GRADER - Official graders documentation

## Document History

**[2026-01-30 11:05]**
- Initial documentation created
