---
description: Execute implementation from context, INFO, SPEC or IMPL documents
auto_execution_mode: 1
---

# Implement Workflow

## Required Skills

- @coding-conventions for coding style
- @write-documents for tracking

## MUST-NOT-FORGET

1. Apply changes immediately without asking for permission - this workflow has authority to implement
2. Phase flow: Prerequisites → GLOBAL-RULES → Impact Assessment → Execution

- Prerequisites ensure required documents (SPEC, IMPL, TEST) exist
- GLOBAL-RULES apply BEFORE any code change
- Impact Assessment is MANDATORY before implementation
- Run `/verify` after implementation complete

Quick reference (prerequisites):
- INFO only → Run `/write-spec`
- SPEC only → Run `/write-impl-plan`
- IMPL only → Run `/write-test-plan`

## GLOBAL-RULES

Apply to ALL implementation contexts. Goal: Understand full impact before making changes.

1. Trace scope - Identify all artifacts affected by the change (direct and indirect)
2. Assess impact - Determine what functionality depends on affected artifacts
3. Define verification - Create checkpoints to catch regressions early

Document rules:
- IMPL exists → Add "Impact Analysis" section to IMPL
- No IMPL + multi-file change → Create IMPL with analysis
- TEST exists → Add new test cases to TEST
- No TEST + multi-file change → Create TEST

# CONTEXT-SPECIFIC

## No Documents

Implement whatever was proposed or specified in conversation.

## Prerequisites Missing

Ensure required documents exist before implementation:

- INFO only → Run `/write-spec` first
- SPEC only → Run `/write-impl-plan` first
- IMPL only → Run `/write-test-plan` first

## Ready to Implement

Entry conditions:
- IMPL plan exists
- TEST exists (no test code) → Implement function skeletons, then failing tests
- TEST + test code exists → Proceed to implementation

### Operation Mode Check

Verify operation mode from NOTES.md before any code changes:
- IMPL-CODEBASE → output to project source folders
- IMPL-ISOLATED → output to `[SESSION_FOLDER]/` only, NEVER workspace root

### Impact Assessment

MANDATORY before implementing. Apply GLOBAL-RULES with code-specific focus:

1. List all code paths that interact with target locations
2. Identify functionality that depends on modified code:
   - Callers and consumers
   - UI components
   - Other endpoints
   - Test files
3. Create test cases for each impacted area BEFORE implementing

### Execution Sequence

1. For each step in IMPL plan:
   - Implement code changes
   - Run tests to verify step works
   - Fix if tests fail (per retry limits)
   - Commit when green
2. Run `/verify` against IMPL plan

### Gate Check: IMPLEMENT→REFINE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

Pass: Run `/refine` | Fail: Continue implementing

## Stuck Detection

If 3 consecutive fix attempts fail:
1. Ask user for guidance
2. Document in PROBLEMS.md
3. Either get guidance or defer and continue

## Attitude

- Senior engineer, anticipating complexity, reducing risks
- Completer / Finisher, never leaves clutter undocumented
- Small cycles: implement → test → fix → green → next

## Rules

- Use small, verifiable steps - never implement large untestable chunks
- Track progress in PROGRESS.md after each commit
- Document problems in PROBLEMS.md immediately when found
- Remove temporary `.tmp_*` files after implementation complete