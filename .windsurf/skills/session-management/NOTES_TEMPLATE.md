# Session Notes

**Doc ID**: YYYY-MM-DD_[SessionTopicCamelCase]-NOTES

## Session Info

- **Started**: 2026-01-15
- **Goal**: Fix authentication token expiration handling in API client
- **Operation Mode**: IMPL-CODEBASE | IMPL-ISOLATED
- **Output Location**: src/features/auth/ | [SESSION_FOLDER]/poc/

## Agent Instructions

- Use exponential backoff for retry logic (1s, 2s, 4s)
- All token operations must be thread-safe

## Key Decisions

- **AUTH-DD-01**: Store refresh token in secure storage instead of localStorage. Rationale: localStorage is vulnerable to XSS attacks.
- **AUTH-DD-02**: Implement token refresh 5 minutes before expiration. Rationale: Prevents race conditions from on-demand refresh.

## Important Findings

- Current implementation has race condition when multiple requests trigger refresh simultaneously [VERIFIED]
- Token expiration check uses client-side time - vulnerable to clock skew [VERIFIED]
- Server returns 401 for both expired and invalid tokens - need to distinguish [ASSUMED]

## Topic Registry

Maintain list of TOPIC IDs used in this session/project:

- `AUTH` - Authentication and authorization system
- `API` - API client and request handling
