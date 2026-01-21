---
description: Document synchronization
auto_execution_mode: 1
---

# Sync Workflow

## Required Skills

Invoke these skills based on context:
- @write-documents for document formatting rules
- @coding-conventions for code-related sync

## Workflow

1. First find out what the sync context is (Conversation→Docs, Code→Docs, Session→Project, etc.)
2. Read GLOBAL-RULES
3. Read the relevant Context-Specific section
4. Create a sync task list
5. Work through sync task list
6. Run Final Steps

## GLOBAL-RULES

Apply to ALL sync operations:

- Always read source document/code BEFORE updating dependent documents
- Preserve existing IDs (FR-XX, DD-XX, etc.) - never renumber
- Add new items at end of relevant section with next available number
- Mark synced items with timestamp in Document History
- Update verification labels when status changes:
  - Code implemented and tested → `[TESTED]` or `[PROVEN]`
  - Assumption validated → `[VERIFIED]`
- Keep formatting consistent with target document style
- Never delete content without explicit user confirmation

## Sync Direction Reference

```
Code Changes
├─> IMPL (update implementation details)
├─> SPEC (update if behavior changed)
└─> TEST (update expected results)

SPEC Changes
├─> IMPL (add/update implementation steps)
└─> TEST (add/update test cases)

IMPL Changes
├─> SPEC (update if implementation reveals spec gaps)
└─> TEST (update test cases for edge cases)

Session Documents
├─> Project NOTES.md (reusable decisions, patterns)
├─> Project PROBLEMS.md (resolved issues with project impact)
└─> Project PROGRESS.md (completed milestones)

Major Project Changes
├─> README.md (new features, changed structure, updated usage)
├─> NOTES.md (new conventions, topic registry updates)
└─> PROGRESS.md (milestone completions, version changes)
```

## Final Steps

1. Re-read all modified documents
2. [VERIFY] cross-references are valid (IDs exist in source)
3. Update Document History section in each modified file
4. Check for orphaned references (target deleted but reference remains)

# CONTEXT-SPECIFIC

## Code to Documents (Code→Docs)

When implementation differs from plan or spec:

**Detect changes:**
- Compare implemented behavior vs SPEC requirements
- Compare implementation approach vs IMPL plan
- Note any deviations, additions, or simplifications

**Sync to IMPL:**
- Update implementation steps that changed
- Add edge cases discovered during implementation (EC-XX)
- Mark completed steps in verification checklist

**Sync to SPEC:**
- Update FR-XX if requirement interpretation changed
- Add DD-XX for design decisions made during implementation
- Update IG-XX if guarantees changed

**Sync to TEST:**
- Update TC-XX expected results if behavior changed
- Add TC-XX for new edge cases

## Specification Updates (SPEC→Downstream)

When SPEC changes after initial creation:

**Sync to IMPL:**
- Add implementation steps for new FR-XX
- Update steps affected by changed FR-XX
- Add edge case handling for new requirements

**Sync to TEST:**
- Add TC-XX for each new FR-XX
- Update TC-XX for changed requirements
- Remove or mark obsolete TC-XX for removed requirements

## Implementation Plan Updates (IMPL→TEST)

When IMPL plan changes:

**Sync to TEST:**
- Add TC-XX for new EC-XX edge cases
- Update test phases if implementation order changed
- Add setup/teardown for new dependencies

## Session to Project (Session→Project)

When closing a session or syncing findings:

**Sync NOTES.md findings:**
- Key Decisions → Project NOTES.md (if reusable beyond session)
- Agent Instructions → Project rules or NOTES.md
- Important Findings → Relevant SPEC or INFO documents

**Sync PROBLEMS.md:**
- Resolved problems with project impact → Project PROBLEMS.md
- Discovered bugs in unrelated code → Project PROBLEMS.md or GitHub issues
- Deferred items → Project PROBLEMS.md with priority

**Sync PROGRESS.md:**
- Completed milestones → Project PROGRESS.md
- Tried But Not Used → Project NOTES.md (prevent re-exploration)
- Test coverage changes → Relevant TEST documents

## Verification Label Updates

When status changes occur:

**Promote labels:**
- Finding re-read and confirmed → `[ASSUMED]` → `[VERIFIED]`
- POC or test script works → `[VERIFIED]` → `[TESTED]`
- Works in actual implementation → `[TESTED]` → `[PROVEN]`

**Where to update:**
- INFO: Source claims and findings
- SPEC: Design decisions and assumptions
- IMPL: Edge case handling choices
- TEST: Expected behaviors

## Cross-Document Reference Sync

When IDs change or documents restructure:

**Check references:**
- IMPL references to SPEC (FR-XX, DD-XX, IG-XX)
- TEST references to SPEC and IMPL (FR-XX, EC-XX)
- Document "Depends on" headers

**Fix broken references:**
- Update ID if item was renumbered
- Remove reference if item was deleted
- Add note if reference target moved to different document
