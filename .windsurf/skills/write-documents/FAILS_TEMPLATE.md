# Failure Log

**Goal**: Document failures, mistakes, and lessons learned to prevent repetition

## Table of Contents

1. [Active Issues](#active-issues)
2. [Resolved Issues](#resolved-issues)
3. [Document History](#document-history)

## Active Issues

### [DATE] - [Context/Topic]

#### [CRITICAL] `[TOPIC]-FL-001` Issue Title

- **When**: [YYYY-MM-DD HH:MM]
- **Where**: File/function/line or document section
- **What**: Exact problem description
- **Why it went wrong**: Root cause analysis
- **Evidence**: Link, test, or example proving the issue
- **Suggested fix**: Brief recommendation

**Code example** (if applicable):
```
// Before (wrong)
...

// After (correct)
...
```

#### [HIGH] `[TOPIC]-FL-002` Another Issue

- **When**: [YYYY-MM-DD HH:MM]
- **Where**: [Location]
- **What**: [Description]
- **Why it went wrong**: [Root cause]
- **Evidence**: [Proof]
- **Suggested fix**: [Recommendation]

## Resolved Issues

### [DATE] - [Context/Topic]

#### [RESOLVED] `[TOPIC]-FL-001` Issue Title

- **Original severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **Resolved**: [YYYY-MM-DD]
- **Solution**: [What was done to fix it]
- **Link**: [Reference to commit, PR, or document]

## Failure Categories

- `[CRITICAL]` - Flawed assumption causing production failure
- `[HIGH]` - Logic error likely to cause failure under normal conditions
- `[MEDIUM]` - Edge case could cause failure under specific conditions
- `[LOW]` - Minor issue, unlikely to cause failure

## Assumption Labels

- `[UNVERIFIED]` - Assumption made without evidence
- `[CONTRADICTS]` - Logic conflicts with other statement/code
- `[OUTDATED]` - Assumption may no longer be valid
- `[INCOMPLETE]` - Reasoning missing critical considerations

## Location Rules

- **SESSION-BASED**: `[SESSION_FOLDER]/FAILS.md`
- **PROJECT-WIDE + SINGLE-PROJECT**: `[WORKSPACE_FOLDER]/FAILS.md`
- **PROJECT-WIDE + MONOREPO**: `[PROJECT_FOLDER]/FAILS.md`

## Management Rules

- Most recent entries at top
- Never delete entries - mark as `[RESOLVED]` with date and solution
- Link to `_REVIEW` files containing detailed analysis
- Include in `/prime` workflow to load lessons learned

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial failure log created
