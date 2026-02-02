# OpenAI API Sources

**Doc ID**: OAIAPI-IN01
**Goal**: Master source index for OpenAI API documentation (MCPI)
**Version scope**: API v1, Documentation date 2026-01-30

## Preflight Accuracy

**Pre-research assumptions**: 10 total
**Verified**: 9/10 (90%)
**Status**: CORRECT - proceed without re-run

### Assumption Verification

1. **REST with JSON** - CORRECT [VERIFIED] - API reference confirms REST API with JSON
2. **API key authentication** - CORRECT [VERIFIED] - Bearer token in Authorization header
3. **Main endpoints** - PARTIAL → CORRECT - More endpoints than assumed (Responses API, Realtime, etc.)
4. **Rate limits per org/project** - CORRECT [VERIFIED] - Headers show rate limit info
5. **SSE for streaming** - CORRECT [VERIFIED] - Server-Sent Events confirmed
6. **Models include GPT-4, GPT-3.5, DALL-E, Whisper** - CORRECT [VERIFIED] - Plus newer models (o4, gpt-4o, gpt-5)
7. **Assistants API separate** - CORRECT [VERIFIED] - Distinct section in navigation
8. **Fine-tuning available** - CORRECT [VERIFIED] - Dedicated endpoint
9. **Batch API exists** - CORRECT [VERIFIED] - Listed in Platform APIs
10. **Realtime is WebSocket** - CORRECT [VERIFIED] - WebSocket-based with client/server events

## Official Sources - Core Documentation

### API Reference

- `OAIAPI-IN01-SC-OAI-INTRO` - https://platform.openai.com/docs/api-reference/introduction
- `OAIAPI-IN01-SC-OAI-AUTH` - https://platform.openai.com/docs/api-reference/authentication
- `OAIAPI-IN01-SC-OAI-DEBUG` - https://platform.openai.com/docs/api-reference/debugging-requests
- `OAIAPI-IN01-SC-OAI-COMPAT` - https://platform.openai.com/docs/api-reference/backward-compatibility

### Responses API

- `OAIAPI-IN01-SC-OAI-RESP` - https://platform.openai.com/docs/api-reference/responses
- `OAIAPI-IN01-SC-OAI-CONV` - https://platform.openai.com/docs/api-reference/conversations
- `OAIAPI-IN01-SC-OAI-RESPSTR` - https://platform.openai.com/docs/api-reference/responses-streaming

### Webhooks

- `OAIAPI-IN01-SC-OAI-WEBHK` - https://platform.openai.com/docs/api-reference/webhook-events

### Platform APIs

- `OAIAPI-IN01-SC-OAI-AUDIO` - https://platform.openai.com/docs/api-reference/audio
- `OAIAPI-IN01-SC-OAI-VIDEO` - https://platform.openai.com/docs/api-reference/videos
- `OAIAPI-IN01-SC-OAI-IMAGE` - https://platform.openai.com/docs/api-reference/images
- `OAIAPI-IN01-SC-OAI-IMGSTR` - https://platform.openai.com/docs/api-reference/images-streaming
- `OAIAPI-IN01-SC-OAI-EMBED` - https://platform.openai.com/docs/api-reference/embeddings
- `OAIAPI-IN01-SC-OAI-EVALS` - https://platform.openai.com/docs/api-reference/evals
- `OAIAPI-IN01-SC-OAI-FTUNE` - https://platform.openai.com/docs/api-reference/fine-tuning
- `OAIAPI-IN01-SC-OAI-GRADER` - https://platform.openai.com/docs/api-reference/graders
- `OAIAPI-IN01-SC-OAI-BATCH` - https://platform.openai.com/docs/api-reference/batch
- `OAIAPI-IN01-SC-OAI-FILES` - https://platform.openai.com/docs/api-reference/files
- `OAIAPI-IN01-SC-OAI-UPLOAD` - https://platform.openai.com/docs/api-reference/uploads
- `OAIAPI-IN01-SC-OAI-MODELS` - https://platform.openai.com/docs/api-reference/models
- `OAIAPI-IN01-SC-OAI-MODER` - https://platform.openai.com/docs/api-reference/moderations

### Vector Stores

- `OAIAPI-IN01-SC-OAI-VSTORE` - https://platform.openai.com/docs/api-reference/vector-stores
- `OAIAPI-IN01-SC-OAI-VSFILE` - https://platform.openai.com/docs/api-reference/vector-stores-files
- `OAIAPI-IN01-SC-OAI-VSBATCH` - https://platform.openai.com/docs/api-reference/vector-stores-file-batches

### ChatKit (Beta)

- `OAIAPI-IN01-SC-OAI-CHATKIT` - https://platform.openai.com/docs/api-reference/chatkit

### Containers

- `OAIAPI-IN01-SC-OAI-CONTAIN` - https://platform.openai.com/docs/api-reference/containers
- `OAIAPI-IN01-SC-OAI-CONTFILE` - https://platform.openai.com/docs/api-reference/container-files

### Realtime API

- `OAIAPI-IN01-SC-OAI-REALTIME` - https://platform.openai.com/docs/api-reference/realtime
- `OAIAPI-IN01-SC-OAI-RTSESS` - https://platform.openai.com/docs/api-reference/realtime-sessions
- `OAIAPI-IN01-SC-OAI-RTCALLS` - https://platform.openai.com/docs/api-reference/realtime-calls
- `OAIAPI-IN01-SC-OAI-RTCLIENT` - https://platform.openai.com/docs/api-reference/realtime-client-events
- `OAIAPI-IN01-SC-OAI-RTSERVER` - https://platform.openai.com/docs/api-reference/realtime-server-events

### Chat Completions

- `OAIAPI-IN01-SC-OAI-CHAT` - https://platform.openai.com/docs/api-reference/chat
- `OAIAPI-IN01-SC-OAI-CHATSTR` - https://platform.openai.com/docs/api-reference/chat-streaming

### Assistants API

- `OAIAPI-IN01-SC-OAI-ASSIST` - https://platform.openai.com/docs/api-reference/assistants
- `OAIAPI-IN01-SC-OAI-THREAD` - https://platform.openai.com/docs/api-reference/threads
- `OAIAPI-IN01-SC-OAI-MSG` - https://platform.openai.com/docs/api-reference/messages
- `OAIAPI-IN01-SC-OAI-RUNS` - https://platform.openai.com/docs/api-reference/runs
- `OAIAPI-IN01-SC-OAI-RUNSTEP` - https://platform.openai.com/docs/api-reference/run-steps
- `OAIAPI-IN01-SC-OAI-ASSTSTR` - https://platform.openai.com/docs/api-reference/assistants-streaming

### Administration

- `OAIAPI-IN01-SC-OAI-ADMIN` - https://platform.openai.com/docs/api-reference/administration
- `OAIAPI-IN01-SC-OAI-ADMKEY` - https://platform.openai.com/docs/api-reference/admin-api-keys
- `OAIAPI-IN01-SC-OAI-INVITE` - https://platform.openai.com/docs/api-reference/invite
- `OAIAPI-IN01-SC-OAI-USERS` - https://platform.openai.com/docs/api-reference/users
- `OAIAPI-IN01-SC-OAI-GROUPS` - https://platform.openai.com/docs/api-reference/groups
- `OAIAPI-IN01-SC-OAI-ROLES` - https://platform.openai.com/docs/api-reference/roles
- `OAIAPI-IN01-SC-OAI-ROLEASSN` - https://platform.openai.com/docs/api-reference/role-assignments
- `OAIAPI-IN01-SC-OAI-PROJ` - https://platform.openai.com/docs/api-reference/projects
- `OAIAPI-IN01-SC-OAI-PROJUSR` - https://platform.openai.com/docs/api-reference/project-users
- `OAIAPI-IN01-SC-OAI-PROJGRP` - https://platform.openai.com/docs/api-reference/project-groups
- `OAIAPI-IN01-SC-OAI-PROJSVC` - https://platform.openai.com/docs/api-reference/project-service-accounts
- `OAIAPI-IN01-SC-OAI-PROJKEY` - https://platform.openai.com/docs/api-reference/project-api-keys
- `OAIAPI-IN01-SC-OAI-PROJLIM` - https://platform.openai.com/docs/api-reference/project-rate-limits
- `OAIAPI-IN01-SC-OAI-AUDIT` - https://platform.openai.com/docs/api-reference/audit-logs
- `OAIAPI-IN01-SC-OAI-USAGE` - https://platform.openai.com/docs/api-reference/usage
- `OAIAPI-IN01-SC-OAI-CERTS` - https://platform.openai.com/docs/api-reference/certificates

### Legacy APIs

- `OAIAPI-IN01-SC-OAI-COMPLET` - https://platform.openai.com/docs/api-reference/completions
- `OAIAPI-IN01-SC-OAI-RTBETA` - https://platform.openai.com/docs/api-reference/realtime_beta
- `OAIAPI-IN01-SC-OAI-RTBSESS` - https://platform.openai.com/docs/api-reference/realtime-beta-sessions
- `OAIAPI-IN01-SC-OAI-RTBCLI` - https://platform.openai.com/docs/api-reference/realtime-beta-client-events
- `OAIAPI-IN01-SC-OAI-RTBSRV` - https://platform.openai.com/docs/api-reference/realtime-beta-server-events

## Official Sources - Guides

- `OAIAPI-IN01-SC-OAI-RATELIM` - https://platform.openai.com/docs/guides/rate-limits
- `OAIAPI-IN01-SC-OAI-PRODBP` - https://platform.openai.com/docs/guides/production-best-practices
- `OAIAPI-IN01-SC-OAI-SAFETY` - https://platform.openai.com/docs/guides/safety-best-practices
- `OAIAPI-IN01-SC-OAI-ERRCODES` - https://platform.openai.com/docs/guides/error-codes
- `OAIAPI-IN01-SC-OAI-LIBS` - https://platform.openai.com/docs/libraries
- `OAIAPI-IN01-SC-OAI-MODELSOV` - https://platform.openai.com/docs/models
- `OAIAPI-IN01-SC-OAI-CHANGELOG` - https://platform.openai.com/docs/changelog

## Official Sources - Cookbook

- `OAIAPI-IN01-SC-COOK-HOME` - https://cookbook.openai.com/
- `OAIAPI-IN01-SC-COOK-ABOUT` - https://cookbook.openai.com/about
- `OAIAPI-IN01-SC-COOK-GPT5` - https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide
- `OAIAPI-IN01-SC-COOK-DEEP` - https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api
- `OAIAPI-IN01-SC-COOK-DEEPAG` - https://cookbook.openai.com/examples/deep_research_api/introduction_to_deep_research_api_agents

## Community Sources

### Stack Overflow

- `OAIAPI-IN01-SC-SO-AUTH` - https://stackoverflow.com/questions/76580372/problems-with-openai-authentification
  - Topic: Authentication issues
- `OAIAPI-IN01-SC-SO-429` - https://stackoverflow.com/questions/75041580/openai-api-giving-error-429-too-many-requests
  - Topic: Rate limit errors (429), credit balance issues
- `OAIAPI-IN01-SC-SO-400` - https://stackoverflow.com/questions/78285635/openai-api-error-how-do-i-fix-error-400-when-using-the-chat-completions-api
  - Topic: Bad request errors (400)
- `OAIAPI-IN01-SC-SO-ERRHNDL` - https://stackoverflow.com/questions/76363168/openai-api-how-do-i-handle-errors-in-python
  - Topic: Error handling patterns in Python
- `OAIAPI-IN01-SC-SO-STREAM` - https://stackoverflow.com/questions/78660088/how-does-streaming-work-in-openais-apis
  - Topic: Streaming implementation details

### GitHub Issues

- `OAIAPI-IN01-SC-GH-RATELIM` - https://github.com/openai/openai-cookbook/blob/main/examples/How_to_handle_rate_limits.ipynb
  - Topic: Official rate limit handling guide
- `OAIAPI-IN01-SC-GH-TPM937` - https://github.com/openai/openai-python/issues/937
  - Topic: TPM limit errors for Azure
- `OAIAPI-IN01-SC-GH-IMG2755` - https://github.com/openai/openai-python/issues/2755
  - Topic: Dynamic rate limit update loss for GPT-Image
- `OAIAPI-IN01-SC-GH-IMGFAIL` - https://github.com/openai/openai-python/issues/2269
  - Topic: Image generation rate limit handling on failures

### Community Forums

- `OAIAPI-IN01-SC-FORUM-SSE` - https://community.openai.com/t/sse-client-in-golang-issues-with-fine-tune-event-streaming/270133
  - Topic: SSE implementation issues in Go
- `OAIAPI-IN01-SC-FORUM-STRGUIDE` - https://community.openai.com/t/responses-api-streaming-the-simple-guide-to-events/1363122
  - Topic: Responses API streaming events guide

## Related APIs/Technologies

- **Azure OpenAI Service** - Microsoft's hosted version with enterprise features
  - URL: https://learn.microsoft.com/en-us/azure/ai-services/openai/
  - Difference: Different authentication (Azure AD), regional endpoints, enterprise compliance
- **Anthropic Claude API** - Competing LLM API
  - URL: https://docs.anthropic.com/
  - Difference: Different message format, different models, different pricing
- **Google Gemini API** - Competing LLM API
  - URL: https://ai.google.dev/docs
  - Difference: Different authentication (Google Cloud), different models

## Source Statistics

- **Official API Reference pages**: 56
- **Official Guide pages**: 7
- **Cookbook examples**: 5
- **Community sources**: 11
- **Total sources**: 79

## Document History

**[2026-01-30 09:20]**
- Initial sources document created
- All 56 API reference endpoints enumerated from navigation
- 11 community sources collected
- Assumptions verified (90% accuracy)
