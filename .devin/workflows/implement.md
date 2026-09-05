---
description: Implement approved changes - code from plans or corrections from reviews
auto_execution_mode: 3
---

# Implement Workflow

Implement what was decided and approved. Works in two modes: building code from plans, or applying review-approved corrections to documents.

**Goal**: Changed artifacts (code or documents) matching approved decisions

**Why**: Separates judgment (critique, fact-check, verify) from execution (implement). One workflow applies all approved changes regardless of source.

**Scope boundary**: This workflow EXECUTES approved changes. It does NOT judge quality (`/verify`, `/critique`), check facts (`/fact-check`), or triage findings (`/reconcile`).

## Required Skills

- @skills:coding-conventions for coding style
- @skills:write-documents for tracking and document edits

## MUST-NOT-FORGET

1. NEVER ask questions - derive goal from conversation context. Act on best inference.
2. Apply changes immediately without asking for permission - this workflow has authority to implement
3. **Detect context first**: Review Pipeline or Build. Wrong mode = wrong output.
4. Review Pipeline: input is `*_REVIEW.md` + reconcile output → apply corrections to source documents
5. Build: input is SPEC/IMPL → produce code
6. Run `/verify` after implementation complete

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: README.md, !NOTES.md or NOTES.md, FAILS.md

## Workflow

1. Detect context: Review Pipeline or Build (see detection rules below)
2. Read GLOBAL-RULES
3. Read relevant CONTEXT-SPECIFIC section
4. Execute
5. Run `/verify`

## Context Detection

**Review Pipeline** - ANY of these signals:
- `*_REVIEW.md` file referenced or in scope (from `/critique` or `/fact-check`)
- Reconcile output in preceding conversation (recommended actions, improvement options)
- User invokes after `/reconcile` without specifying a SPEC/IMPL
- User mentions "apply findings", "implement corrections", "fix the review items"

**Build** - ALL of these:
- SPEC, IMPL, or TEST documents in scope
- No `*_REVIEW.md` in scope
- No reconcile output in preceding conversation

**Ambiguous** - Both signals present:
- If user references a `*_REVIEW.md` AND a SPEC/IMPL → Review Pipeline (review takes priority)
- If unclear → state interpretation, proceed with best inference

## GLOBAL-RULES

Apply to ALL implementation contexts.

1. Trace scope - identify all artifacts affected by the change
2. Assess impact - determine what depends on affected artifacts
3. Define verification - create checkpoints to catch regressions
4. Track progress in PROGRESS.md
5. Document problems in PROBLEMS.md immediately when found

# CONTEXT-SPECIFIC

## Review Pipeline (from `/critique` or `/fact-check` via `/reconcile`)

Apply reconcile-approved corrections to source documents. This is document editing, not code building.

### Input

1. Read `*_REVIEW.md` files in scope
2. Read reconcile output from conversation (Verified Findings, Recommendations)
3. Identify which findings are CONFIRMED with approved fix options

### Execution

For each confirmed finding with an approved fix:

1. Open the source document referenced by the finding
2. Locate the specific section/claim cited
3. Apply the approved correction (Option A, B, or as recommended)
4. If finding is from fact-check: verify replacement claim is factually correct before inserting
5. If finding affects downstream documents (SPEC claim used in IMPL), trace and fix dependents

### Post-Corrections

1. Update `FAILS.md`: mark addressed entries as `[RESOLVED]` with fix reference
2. Rename implemented `*_REVIEW.md` files: replace `_REVIEW.md` with `_REVIEW-implemented.md` (e.g., `_INFO_FOO_REVIEW.md` becomes `_INFO_FOO_REVIEW-implemented.md`)
3. Run `/verify` on modified documents

### Gate Check: REVIEW-PIPELINE→COMPLETE

- [ ] All confirmed findings applied
- [ ] Replacement claims verified (not swapping one error for another)
- [ ] Downstream dependents checked
- [ ] FAILS.md updated
- [ ] `*_REVIEW.md` files renamed to `*_REVIEW-implemented.md`

Pass: Complete | Fail: Continue applying

## Build: No Documents

Implement whatever was proposed or specified in conversation.

## Build: Prerequisites Missing

Ensure required documents exist before implementation:

- INFO only → Run `/write-spec` first
- SPEC only → Run `/write-impl-plan` first
- IMPL only → Run `/write-test-plan` first

## Build: Ready to Implement

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

Document rules:
- IMPL exists → Add "Impact Analysis" section to IMPL
- No IMPL + multi-file change → Create IMPL with analysis
- TEST exists → Add new test cases to TEST
- No TEST + multi-file change → Create TEST

### Execution Sequence

1. For each step in IMPL plan:
   - Implement code changes
   - Run tests to verify step works
   - Fix if tests fail (per retry limits)
   - Commit when green
2. Run `/verify` against IMPL plan

### Gate Check: BUILD→COMPLETE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed
- [ ] Progress committed

Pass: Run `/verify` | Fail: Continue implementing

## No Context Match

1. Re-read conversation for implicit context
2. If still ambiguous, state interpretation and proceed
3. Default to Build mode if no review signals found

## Stuck Detection

If 3 consecutive fix attempts fail:
1. Document in PROBLEMS.md
2. Ask user for guidance
3. Either get guidance or defer and continue

# FINALIZATION

## Quality Gate

- [ ] Context correctly detected (Review Pipeline or Build)
- [ ] All approved changes applied
- [ ] No original intent lost (review: corrections match findings; build: code matches IMPL)
- [ ] PROGRESS.md updated
- [ ] Temporary `.tmp_*` files removed

## Verification

Run `/verify` on all modified artifacts.

## Output

- **Review Pipeline**: Modified source documents + updated FAILS.md + `*_REVIEW.md` renamed to `*_REVIEW-implemented.md`
- **Build**: Implemented code + tests + updated PROGRESS.md