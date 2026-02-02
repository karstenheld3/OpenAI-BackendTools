# OpenAI API Documentation - Table of Contents

**Doc ID**: OAIAPI-TOC01
**Goal**: Master index for all OpenAI API documentation files
**Version scope**: API v1, Documentation date 2026-01-30

**Depends on:**
- `__OAIAPI_SOURCES.md [OAIAPI-IN01]` for source references

**Research stats**: 35m net | ~35 credits | 62 docs | 79 sources | Opus 4.5 Thinking

## Summary

The OpenAI API is a RESTful API (v1) that provides programmatic access to OpenAI's AI models including GPT-4o, GPT-5, o4-mini, DALL-E, Whisper, and specialized models for embeddings, moderation, and fine-tuning. Authentication uses Bearer tokens via API keys, with optional organization and project headers for multi-tenant scenarios. The API supports three interaction patterns: synchronous REST requests, Server-Sent Events (SSE) streaming for real-time token delivery, and WebSocket-based Realtime API for voice and live interactions. Key endpoint families include: Responses API (new unified interface), Chat Completions (legacy but widely used), Assistants API (stateful conversations with tools), and Platform APIs for media processing (audio, video, images). Vector stores enable RAG workflows with built-in file chunking and retrieval. Administrative endpoints allow organization management, user roles, project configuration, rate limit customization, and audit logging. Rate limits are enforced per-model at organization and project levels, with headers providing real-time quota information. The Batch API enables cost-efficient async processing for bulk workloads. Fine-tuning is available for select models with job management and checkpoint APIs. Enterprise features include mTLS certificates and Admin API keys for programmatic org management.

## Topic Files

**Total topics: 62**

### Core Documentation
- [_INFO_OAIAPI_INTRODUCTION.md](#topic-introduction) - API overview, base URL, versioning
- [_INFO_OAIAPI_AUTHENTICATION.md](#topic-authentication) - API keys, headers, organizations, projects
- [_INFO_OAIAPI_DEBUGGING.md](#topic-debugging) - Request IDs, headers, troubleshooting
- [_INFO_OAIAPI_COMPATIBILITY.md](#topic-compatibility) - Backward compatibility, breaking changes

### Responses API
- [_INFO_OAIAPI_RESPONSES.md](#topic-responses) - Create response, input types, tools
- [_INFO_OAIAPI_CONVERSATIONS.md](#topic-conversations) - Multi-turn conversations, context
- [_INFO_OAIAPI_RESPONSES_STREAMING.md](#topic-responses-streaming) - SSE events, deltas

### Webhooks
- [_INFO_OAIAPI_WEBHOOKS.md](#topic-webhooks) - Webhook events, delivery, signatures

### Chat Completions
- [_INFO_OAIAPI_CHAT.md](#topic-chat-completions) - Create completion, messages, functions
- [_INFO_OAIAPI_CHAT_STREAMING.md](#topic-chat-streaming) - Stream chunks, finish reasons

### Assistants API
- [_INFO_OAIAPI_ASSISTANTS.md](#topic-assistants) - Create/manage assistants, tools
- [_INFO_OAIAPI_THREADS.md](#topic-threads) - Thread lifecycle, metadata
- [_INFO_OAIAPI_MESSAGES.md](#topic-messages) - Add/list messages, annotations
- [_INFO_OAIAPI_RUNS.md](#topic-runs) - Execute runs, status, required actions
- [_INFO_OAIAPI_RUN_STEPS.md](#topic-run-steps) - Step details, tool calls
- [_INFO_OAIAPI_ASSISTANTS_STREAMING.md](#topic-assistants-streaming) - Run streaming events

### Platform APIs - Media
- [_INFO_OAIAPI_AUDIO.md](#topic-audio) - Transcription (Whisper), TTS, translation
- [_INFO_OAIAPI_VIDEOS.md](#topic-videos) - Video generation, status
- [_INFO_OAIAPI_IMAGES.md](#topic-images) - Generation (DALL-E), edits, variations
- [_INFO_OAIAPI_IMAGES_STREAMING.md](#topic-images-streaming) - Streaming image generation

### Platform APIs - AI Core
- [_INFO_OAIAPI_EMBEDDINGS.md](#topic-embeddings) - Text embeddings, dimensions
- [_INFO_OAIAPI_MODERATIONS.md](#topic-moderations) - Content moderation, categories
- [_INFO_OAIAPI_MODELS.md](#topic-models) - List models, model info, delete fine-tuned

### Platform APIs - Evaluation & Training
- [_INFO_OAIAPI_EVALS.md](#topic-evals) - Evaluation jobs, metrics
- [_INFO_OAIAPI_FINE_TUNING.md](#topic-fine-tuning) - Jobs, events, checkpoints
- [_INFO_OAIAPI_GRADERS.md](#topic-graders) - Grading models, rubrics

### Platform APIs - Processing
- [_INFO_OAIAPI_BATCH.md](#topic-batch) - Batch jobs, async processing
- [_INFO_OAIAPI_FILES.md](#topic-files) - Upload, list, retrieve, delete
- [_INFO_OAIAPI_UPLOADS.md](#topic-uploads) - Multipart uploads, parts

### Vector Stores
- [_INFO_OAIAPI_VECTOR_STORES.md](#topic-vector-stores) - Create/manage stores
- [_INFO_OAIAPI_VECTOR_STORE_FILES.md](#topic-vector-store-files) - Add files, chunking
- [_INFO_OAIAPI_VECTOR_STORE_FILE_BATCHES.md](#topic-vector-store-file-batches) - Bulk file operations

### Realtime API
- [_INFO_OAIAPI_REALTIME.md](#topic-realtime) - WebSocket overview, sessions
- [_INFO_OAIAPI_REALTIME_SESSIONS.md](#topic-realtime-sessions) - Client secrets, session config
- [_INFO_OAIAPI_REALTIME_CALLS.md](#topic-realtime-calls) - Voice calls, telephony
- [_INFO_OAIAPI_REALTIME_CLIENT_EVENTS.md](#topic-realtime-client-events) - Client-to-server events
- [_INFO_OAIAPI_REALTIME_SERVER_EVENTS.md](#topic-realtime-server-events) - Server-to-client events

### Containers
- [_INFO_OAIAPI_CONTAINERS.md](#topic-containers) - Container management
- [_INFO_OAIAPI_CONTAINER_FILES.md](#topic-container-files) - Container file operations

### ChatKit (Beta)
- [_INFO_OAIAPI_CHATKIT.md](#topic-chatkit) - ChatKit components, UI integration

### Administration
- [_INFO_OAIAPI_ADMINISTRATION.md](#topic-administration) - Admin overview, API keys
- [_INFO_OAIAPI_ADMIN_API_KEYS.md](#topic-admin-api-keys) - Admin key management
- [_INFO_OAIAPI_INVITES.md](#topic-invites) - User invitations
- [_INFO_OAIAPI_USERS.md](#topic-users) - User management
- [_INFO_OAIAPI_GROUPS.md](#topic-groups) - Group management
- [_INFO_OAIAPI_ROLES.md](#topic-roles) - Role definitions
- [_INFO_OAIAPI_ROLE_ASSIGNMENTS.md](#topic-role-assignments) - Assign roles
- [_INFO_OAIAPI_PROJECTS.md](#topic-projects) - Project management
- [_INFO_OAIAPI_PROJECT_USERS.md](#topic-project-users) - Project membership
- [_INFO_OAIAPI_PROJECT_GROUPS.md](#topic-project-groups) - Project group access
- [_INFO_OAIAPI_PROJECT_SERVICE_ACCOUNTS.md](#topic-project-service-accounts) - Service accounts
- [_INFO_OAIAPI_PROJECT_API_KEYS.md](#topic-project-api-keys) - Project-scoped keys
- [_INFO_OAIAPI_PROJECT_RATE_LIMITS.md](#topic-project-rate-limits) - Per-project limits
- [_INFO_OAIAPI_AUDIT_LOGS.md](#topic-audit-logs) - Audit trail
- [_INFO_OAIAPI_USAGE.md](#topic-usage) - Usage metrics, costs
- [_INFO_OAIAPI_CERTIFICATES.md](#topic-certificates) - mTLS certificates

### Legacy APIs
- [_INFO_OAIAPI_COMPLETIONS.md](#topic-completions) - Legacy completions endpoint
- [_INFO_OAIAPI_REALTIME_BETA.md](#topic-realtime-beta) - Legacy realtime API

### Guides (Cross-Cutting)
- [_INFO_OAIAPI_RATE_LIMITS.md](#topic-rate-limits) - Rate limiting, tiers, quotas
- [_INFO_OAIAPI_ERROR_HANDLING.md](#topic-error-handling) - Error codes, retry strategies
- [_INFO_OAIAPI_PRODUCTION.md](#topic-production) - Production best practices
- [_INFO_OAIAPI_SDKS.md](#topic-sdks) - Official SDKs, libraries

## Topic Details

### Topic: Introduction
**Scope**: API overview, base URL structure, REST conventions, versioning strategy
**Contents**:
- Base URL: `https://api.openai.com/v1/`
- REST API version (currently `2020-10-01`)
- SDK availability and links
- Request/response format (JSON)
**Sources**: OAIAPI-IN01-SC-OAI-INTRO

### Topic: Authentication
**Scope**: API key management, authentication headers, multi-org support
**Contents**:
- Bearer token authentication
- `Authorization: Bearer $OPENAI_API_KEY`
- `OpenAI-Organization` header for org selection
- `OpenAI-Project` header for project selection
- Key security best practices
**Sources**: OAIAPI-IN01-SC-OAI-AUTH

### Topic: Debugging
**Scope**: Request tracing, response headers, troubleshooting
**Contents**:
- `x-request-id` header for support
- `X-Client-Request-Id` for custom tracing
- `openai-processing-ms` timing header
- Rate limit headers (x-ratelimit-*)
**Sources**: OAIAPI-IN01-SC-OAI-DEBUG

### Topic: Compatibility
**Scope**: Versioning policy, backward compatibility guarantees
**Contents**:
- REST API v1 stability
- SDK semantic versioning
- Model family stability
- Backward-compatible changes (additive)
- Changelog location
**Sources**: OAIAPI-IN01-SC-OAI-COMPAT

### Topic: Responses
**Scope**: New unified Responses API for model interactions
**Contents**:
- POST /v1/responses - Create response
- Input types (text, image, file)
- Tools (code_interpreter, file_search, function)
- Reasoning configuration
- Output formats
**Sources**: OAIAPI-IN01-SC-OAI-RESP

### Topic: Conversations
**Scope**: Multi-turn conversation management
**Contents**:
- Conversation context
- Previous response linking
- Memory management
**Sources**: OAIAPI-IN01-SC-OAI-CONV

### Topic: Responses Streaming
**Scope**: Server-Sent Events for Responses API
**Contents**:
- Event types (response.created, response.delta, etc.)
- Delta handling
- Partial content assembly
**Sources**: OAIAPI-IN01-SC-OAI-RESPSTR

### Topic: Webhooks
**Scope**: Webhook event delivery system
**Contents**:
- Event types
- Delivery guarantees
- Signature verification
- Retry behavior
**Sources**: OAIAPI-IN01-SC-OAI-WEBHK

### Topic: Chat Completions
**Scope**: Chat-based model interactions (legacy, widely used)
**Contents**:
- POST /v1/chat/completions
- Message roles (system, user, assistant, tool)
- Function calling
- Response format (json_object, json_schema)
- Logprobs
**Sources**: OAIAPI-IN01-SC-OAI-CHAT

### Topic: Chat Streaming
**Scope**: SSE streaming for Chat Completions
**Contents**:
- Stream parameter
- Chunk format
- Delta content
- Finish reasons
**Sources**: OAIAPI-IN01-SC-OAI-CHATSTR

### Topic: Assistants
**Scope**: Stateful AI assistants with tools
**Contents**:
- CRUD operations for assistants
- Tool configuration
- Model selection
- Instructions and metadata
**Sources**: OAIAPI-IN01-SC-OAI-ASSIST

### Topic: Threads
**Scope**: Conversation threads for Assistants
**Contents**:
- Create, retrieve, modify, delete threads
- Thread metadata
- Tool resources attachment
**Sources**: OAIAPI-IN01-SC-OAI-THREAD

### Topic: Messages
**Scope**: Messages within threads
**Contents**:
- Add messages to threads
- Message content types
- Annotations (file citations, file paths)
- Pagination
**Sources**: OAIAPI-IN01-SC-OAI-MSG

### Topic: Runs
**Scope**: Execute assistant on thread
**Contents**:
- Create and manage runs
- Run status lifecycle
- Required actions (tool calls)
- Submit tool outputs
- Cancel runs
**Sources**: OAIAPI-IN01-SC-OAI-RUNS

### Topic: Run Steps
**Scope**: Granular run execution details
**Contents**:
- Step types (message_creation, tool_calls)
- Step status
- Tool call details
**Sources**: OAIAPI-IN01-SC-OAI-RUNSTEP

### Topic: Assistants Streaming
**Scope**: SSE streaming for assistant runs
**Contents**:
- Thread events
- Run events
- Message delta events
- Run step events
**Sources**: OAIAPI-IN01-SC-OAI-ASSTSTR

### Topic: Audio
**Scope**: Audio processing (Whisper, TTS)
**Contents**:
- POST /v1/audio/transcriptions - Speech to text
- POST /v1/audio/translations - Translate to English
- POST /v1/audio/speech - Text to speech
- Supported formats, languages
**Sources**: OAIAPI-IN01-SC-OAI-AUDIO

### Topic: Videos
**Scope**: Video generation
**Contents**:
- Video generation endpoints
- Status tracking
- Output formats
**Sources**: OAIAPI-IN01-SC-OAI-VIDEO

### Topic: Images
**Scope**: Image generation and editing (DALL-E)
**Contents**:
- POST /v1/images/generations
- POST /v1/images/edits
- POST /v1/images/variations
- Size, quality, style options
**Sources**: OAIAPI-IN01-SC-OAI-IMAGE

### Topic: Images Streaming
**Scope**: Streaming image generation
**Contents**:
- Partial image events
- Progressive rendering
**Sources**: OAIAPI-IN01-SC-OAI-IMGSTR

### Topic: Embeddings
**Scope**: Text embeddings for semantic search
**Contents**:
- POST /v1/embeddings
- Models (text-embedding-3-small, text-embedding-3-large)
- Dimensions parameter
- Input types
**Sources**: OAIAPI-IN01-SC-OAI-EMBED

### Topic: Moderations
**Scope**: Content moderation
**Contents**:
- POST /v1/moderations
- Categories (hate, violence, sexual, etc.)
- Category scores
- Flagged determination
**Sources**: OAIAPI-IN01-SC-OAI-MODER

### Topic: Models
**Scope**: Model listing and management
**Contents**:
- GET /v1/models - List models
- GET /v1/models/{model} - Model details
- DELETE /v1/models/{model} - Delete fine-tuned
**Sources**: OAIAPI-IN01-SC-OAI-MODELS

### Topic: Evals
**Scope**: Model evaluation system
**Contents**:
- Evaluation job management
- Metrics and scoring
- Dataset configuration
**Sources**: OAIAPI-IN01-SC-OAI-EVALS

### Topic: Fine-tuning
**Scope**: Custom model training
**Contents**:
- POST /v1/fine_tuning/jobs - Create job
- Job lifecycle and events
- Hyperparameters
- Checkpoints
- Integration with Files API
**Sources**: OAIAPI-IN01-SC-OAI-FTUNE

### Topic: Graders
**Scope**: Grading and evaluation models
**Contents**:
- Grader configuration
- Rubric definition
- Scoring endpoints
**Sources**: OAIAPI-IN01-SC-OAI-GRADER

### Topic: Batch
**Scope**: Async batch processing
**Contents**:
- POST /v1/batches - Create batch
- Batch status tracking
- Input/output file format (JSONL)
- Cost savings (50% discount)
- 24-hour completion window
**Sources**: OAIAPI-IN01-SC-OAI-BATCH

### Topic: Files
**Scope**: File management
**Contents**:
- POST /v1/files - Upload file
- GET /v1/files - List files
- GET /v1/files/{file_id} - Retrieve metadata
- GET /v1/files/{file_id}/content - Download
- DELETE /v1/files/{file_id}
- Purpose types (fine-tune, assistants, batch, etc.)
**Sources**: OAIAPI-IN01-SC-OAI-FILES

### Topic: Uploads
**Scope**: Large file uploads
**Contents**:
- Multipart upload initiation
- Part upload
- Upload completion
- Abort upload
**Sources**: OAIAPI-IN01-SC-OAI-UPLOAD

### Topic: Vector Stores
**Scope**: Vector database for RAG
**Contents**:
- CRUD operations
- Expiration policies
- File counts
- Usage bytes
**Sources**: OAIAPI-IN01-SC-OAI-VSTORE

### Topic: Vector Store Files
**Scope**: Files in vector stores
**Contents**:
- Add files to store
- Chunking strategy
- File status
- Remove files
**Sources**: OAIAPI-IN01-SC-OAI-VSFILE

### Topic: Vector Store File Batches
**Scope**: Bulk file operations
**Contents**:
- Create file batch
- Batch status
- List batch files
- Cancel batch
**Sources**: OAIAPI-IN01-SC-OAI-VSBATCH

### Topic: Realtime
**Scope**: WebSocket-based real-time API
**Contents**:
- WebSocket connection
- Session management
- Audio streaming
- Turn detection
**Sources**: OAIAPI-IN01-SC-OAI-REALTIME

### Topic: Realtime Sessions
**Scope**: Client secrets for realtime
**Contents**:
- POST /v1/realtime/sessions - Create session
- Client secret generation
- Session configuration
**Sources**: OAIAPI-IN01-SC-OAI-RTSESS

### Topic: Realtime Calls
**Scope**: Voice/telephony integration
**Contents**:
- Call management
- Telephony integration
**Sources**: OAIAPI-IN01-SC-OAI-RTCALLS

### Topic: Realtime Client Events
**Scope**: Events sent by client
**Contents**:
- session.update
- input_audio_buffer.append
- input_audio_buffer.commit
- conversation.item.create
- response.create
**Sources**: OAIAPI-IN01-SC-OAI-RTCLIENT

### Topic: Realtime Server Events
**Scope**: Events sent by server
**Contents**:
- session.created
- session.updated
- conversation.item.created
- response.audio.delta
- response.done
- error
**Sources**: OAIAPI-IN01-SC-OAI-RTSERVER

### Topic: Containers
**Scope**: Container management
**Contents**:
- Container CRUD
- Execution environment
**Sources**: OAIAPI-IN01-SC-OAI-CONTAIN

### Topic: Container Files
**Scope**: Files within containers
**Contents**:
- File operations in containers
**Sources**: OAIAPI-IN01-SC-OAI-CONTFILE

### Topic: ChatKit
**Scope**: UI components (Beta)
**Contents**:
- ChatKit overview
- Component integration
**Sources**: OAIAPI-IN01-SC-OAI-CHATKIT

### Topic: Administration
**Scope**: Organization management overview
**Contents**:
- Admin API overview
- Admin API key requirements
- Permission model
**Sources**: OAIAPI-IN01-SC-OAI-ADMIN

### Topic: Admin API Keys
**Scope**: Admin key management
**Contents**:
- Create, list, delete admin keys
- Key permissions
**Sources**: OAIAPI-IN01-SC-OAI-ADMKEY

### Topic: Invites
**Scope**: User invitation management
**Contents**:
- Send invites
- List pending invites
- Revoke invites
**Sources**: OAIAPI-IN01-SC-OAI-INVITE

### Topic: Users
**Scope**: Organization user management
**Contents**:
- List users
- Retrieve user
- Modify user role
- Delete user
**Sources**: OAIAPI-IN01-SC-OAI-USERS

### Topic: Groups
**Scope**: User group management
**Contents**:
- Create, list, modify, delete groups
- Group membership
**Sources**: OAIAPI-IN01-SC-OAI-GROUPS

### Topic: Roles
**Scope**: Role definitions
**Contents**:
- List available roles
- Role permissions
**Sources**: OAIAPI-IN01-SC-OAI-ROLES

### Topic: Role Assignments
**Scope**: Assign roles to users/groups
**Contents**:
- Create assignments
- List assignments
- Delete assignments
**Sources**: OAIAPI-IN01-SC-OAI-ROLEASSN

### Topic: Projects
**Scope**: Project management
**Contents**:
- Create, list, retrieve, modify projects
- Archive projects
**Sources**: OAIAPI-IN01-SC-OAI-PROJ

### Topic: Project Users
**Scope**: Project membership
**Contents**:
- Add users to project
- List project users
- Modify user role in project
- Remove from project
**Sources**: OAIAPI-IN01-SC-OAI-PROJUSR

### Topic: Project Groups
**Scope**: Group access to projects
**Contents**:
- Add groups to project
- List project groups
- Remove groups
**Sources**: OAIAPI-IN01-SC-OAI-PROJGRP

### Topic: Project Service Accounts
**Scope**: Service account management
**Contents**:
- Create service accounts
- List service accounts
- Delete service accounts
**Sources**: OAIAPI-IN01-SC-OAI-PROJSVC

### Topic: Project API Keys
**Scope**: Project-scoped API keys
**Contents**:
- List project keys
- Retrieve key
- Delete key
**Sources**: OAIAPI-IN01-SC-OAI-PROJKEY

### Topic: Project Rate Limits
**Scope**: Per-project rate limit configuration
**Contents**:
- List rate limits by model
- Modify rate limits
**Sources**: OAIAPI-IN01-SC-OAI-PROJLIM

### Topic: Audit Logs
**Scope**: Organization audit trail
**Contents**:
- List audit log events
- Event types
- Actor information
- Filtering options
**Sources**: OAIAPI-IN01-SC-OAI-AUDIT

### Topic: Usage
**Scope**: Usage metrics and billing
**Contents**:
- Usage by model
- Usage by project
- Cost tracking
- Time-based queries
**Sources**: OAIAPI-IN01-SC-OAI-USAGE

### Topic: Certificates
**Scope**: mTLS certificate management
**Contents**:
- Upload certificates
- List certificates
- Delete certificates
- mTLS configuration
**Sources**: OAIAPI-IN01-SC-OAI-CERTS

### Topic: Completions
**Scope**: Legacy text completion API
**Contents**:
- POST /v1/completions (deprecated)
- Prompt-based completion
- Migration to Chat Completions
**Sources**: OAIAPI-IN01-SC-OAI-COMPLET

### Topic: Realtime Beta
**Scope**: Legacy realtime API
**Contents**:
- Previous realtime implementation
- Migration notes
**Sources**: OAIAPI-IN01-SC-OAI-RTBETA

### Topic: Rate Limits
**Scope**: Rate limiting system (cross-cutting)
**Contents**:
- Rate limit types (RPM, TPM, RPD)
- Usage tiers
- Rate limit headers
- Handling 429 errors
- Retry strategies
**Sources**: OAIAPI-IN01-SC-OAI-RATELIM, OAIAPI-IN01-SC-SO-429, OAIAPI-IN01-SC-GH-RATELIM

### Topic: Error Handling
**Scope**: Error responses and handling (cross-cutting)
**Contents**:
- HTTP status codes
- Error object structure
- Common errors (400, 401, 429, 500)
- Python exception types
- Retry strategies
**Sources**: OAIAPI-IN01-SC-OAI-ERRCODES, OAIAPI-IN01-SC-SO-ERRHNDL, OAIAPI-IN01-SC-SO-400

### Topic: Production
**Scope**: Production deployment guidance
**Contents**:
- Security best practices
- API key management
- Organization setup
- Monitoring and logging
- Scaling considerations
**Sources**: OAIAPI-IN01-SC-OAI-PRODBP, OAIAPI-IN01-SC-OAI-SAFETY

### Topic: SDKs
**Scope**: Official client libraries
**Contents**:
- Python SDK (openai-python)
- Node.js SDK
- Other languages
- SDK versioning
**Sources**: OAIAPI-IN01-SC-OAI-LIBS

## Related APIs/Technologies

- **Azure OpenAI Service**
  - URL: https://learn.microsoft.com/en-us/azure/ai-services/openai/
  - Relation: Microsoft-hosted version with enterprise features, different authentication
- **Anthropic Claude API**
  - URL: https://docs.anthropic.com/
  - Relation: Competing LLM API with different message format
- **Google Gemini API**
  - URL: https://ai.google.dev/docs
  - Relation: Competing LLM API from Google

## Document History

**[2026-01-30 10:15]**
- Replaced verbose Research Metadata with one-liner in header block per MCPI spec

**[2026-01-30 10:07]**
- Removed Progress Tracking section (belongs in TASKS/STRUT)
- Added "Total topics: 62" at start of Topic Files section

**[2026-01-30 09:25]**
- Initial TOC created with 62 topics
- All API sections enumerated from navigation
- Cross-cutting guides added
- Related technologies documented
