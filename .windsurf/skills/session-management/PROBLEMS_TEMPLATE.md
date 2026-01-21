# Session Problems

**Doc ID**: YYYY-MM-DD_[SessionTopicCamelCase]-PROBLEMS

Track problems discovered during this session using ID format: `[TOPIC]-PR-[NNN]`

## Open

**AUTH-PR-001: Race condition on simultaneous token refresh**
- **History**: Added 2026-01-15 14:20
- **Description**: Multiple API requests trigger token refresh at the same time, causing duplicate refresh calls
- **Impact**: Server rate-limits refresh endpoint, causing 429 errors and failed requests
- **Next Steps**: Implement mutex/lock pattern to ensure only one refresh happens at a time

**API-PR-002: Clock skew causes premature token expiration**
- **History**: Added 2026-01-15 14:20
- **Description**: Client-side expiration check uses local time, which may be out of sync with server
- **Impact**: Valid tokens rejected as expired, or expired tokens used causing 401 errors
- **Next Steps**: Use server time from response headers or implement server-side expiration check

## Resolved

**AUTH-PR-003: Refresh token stored in localStorage**
- **History**: Added 2026-01-15 14:20 | Resolved 2026-01-15 16:45
- **Solution**: Migrated to secure httpOnly cookie storage with SameSite=Strict
- **Verification**: Tested XSS attack vectors, confirmed token not accessible from JavaScript

## Deferred

**API-PR-004: No retry logic for network failures**
- **History**: Added 2026-01-15 16:45 | Deferred 2026-01-15 16:45
- **Reason**: Requires broader error handling refactor, not critical for current session goal
- **Next**: Implement exponential backoff retry in separate session after auth fixes are stable

## Problems Changes

**[2026-01-15 16:45]**
- Resolved: AUTH-PR-003 (migrated to httpOnly cookies)
- Added: API-PR-004 to Deferred (retry logic postponed)

**[2026-01-15 14:20]**
- Added: AUTH-PR-001 (race condition on token refresh)
- Added: API-PR-002 (clock skew issue)
- Added: AUTH-PR-003 to Open (localStorage security issue)
