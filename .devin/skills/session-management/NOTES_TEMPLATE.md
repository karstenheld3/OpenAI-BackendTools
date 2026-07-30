# Session Notes

Populated by `/session-new` workflow. Captures session context, decisions, and agent instructions for a specific development task.

**Doc ID**: [TOPIC]-NOTES

## Initial Request

**MANDATORY**: Record the user's session-starting prompt verbatim. This preserves intent and prevents drift.

````text
[Paste user's exact prompt here - do not summarize]
````

**Agent rule**: Copy-paste the user's first substantive message that defines the session goal. If prompt is trivial (<20 tokens), write "See Goal above" instead.

## Session Info

- **Started**: 2026-01-15
- **Goal**: Fix authentication token expiration handling in API client
- **Operation Mode**: IMPL-CODEBASE | IMPL-ISOLATED
- **Output Location**: src/features/auth/ | [SESSION_FOLDER]/poc/

## Agent Instructions

- Use exponential backoff for retry logic (1s, 2s, 4s)
- All token operations must be thread-safe

## Key Decisions

- **AUTHSYST-DD-01**: Store refresh token in secure storage instead of localStorage. Rationale: localStorage is vulnerable to XSS attacks.
- **AUTHSYST-DD-02**: Implement token refresh 5 minutes before expiration. Rationale: Prevents race conditions from on-demand refresh.

## Important Findings

- [Finding 1] [LABEL]
- [Finding 2] [LABEL]
- [Finding 3] [LABEL]

## Topic Registry

Maintain list of TOPIC IDs used in this session. Topics MUST be 7-14 uppercase chars. Register globally in ID-REGISTRY.md before use. SUBTOPICs (used in T##/S## nested folders) register HERE only.

**Global topics** (registered in ID-REGISTRY.md):
- `AUTHSYST` - Authentication and authorization system

**Subtopics** (session-local, used in T##/S## folder nested IDs):
- `TKNRFRSH` - Token refresh mechanism (nested as AUTHSYST-TKNRFRSH)
- `APICLTFX` - API client error handling fixes (nested as AUTHSYST-APICLTFX)

## Topic Folders

Independent work streams (see @skills:session-management Topic Folders).

- **T01_TKNRFRSH_TokenRefreshDesign_2026-01-15** - Token refresh mechanism research
- **T02_APICLTFX_APIClientFixes_2026-01-15** - API client error handling

## Step Folders

Sequential pipeline steps (see @skills:session-management Step Folders).

- **S01_SRCPROC_CollectSources_2026-01-15** - Source collection for auth research
- **S02_IMPLMNT_ImplementFixes_2026-01-16** - Implementation phase

## Bug List

Session-local bug tracking. SESSION <-> TOPIC is 1:1, so simple list suffices.
Get next number by counting existing entries. See `/bugfix` workflow.

Format: `[TOPIC]-BG-NNNN` - Description - Status
Example: AUTHSYST-BG-0001 - Token refresh race condition - Resolved

- (none yet)

## Significant Prompts Log

**Agent rule**: Record prompts that change direction, add requirements, or clarify intent. Use 4-backtick fence with `text` language tag.

**Format**: `[YYYY-MM-DD HH:MM]` + one-line context, then fenced prompt.

[2026-01-20 12:24] User clarified retry requirements
````text
Actually, use exponential backoff starting at 500ms, not 1s. And cap at 3 retries.
````

[2026-01-21 09:52] User added thread-safety constraint
````text
I forgot to mention - this runs in a multi-threaded environment. All token ops must be thread-safe.
````