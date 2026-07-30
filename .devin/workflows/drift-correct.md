---
description: Close drift gaps identified by /drift-detect based on __DRIFT_ file
---

# Drift Correct Workflow

Closes instruction-following gaps identified by `/drift-detect`. Reads the persisted `__DRIFT_[TOPIC].md` file and systematically fixes all FAIL items.

**Goal**: All fixable gaps closed, unfixable gaps marked BLOCKED

**Key term**: Definition-of-Done (DoD) = the checklist in `__DRIFT_[TOPIC].md`

**Why**: Correction deserves a full context budget. The `__DRIFT_[TOPIC].md` file provides perfect context (complete gap list with priorities and sources) without needing to re-derive anything.

Usage:
- `/drift-correct` - close all gaps in `__DRIFT_[TOPIC].md`
- `/drift-correct [TOPIC]` - specify which drift file to process

**Scope Boundary**: This workflow only FIXES gaps from an existing `__DRIFT_[TOPIC].md`. It does NOT re-detect. Use `/drift-detect` first.

## Required Skills

- @skills:drift-correction `DRIFT_CORRECTION.md` for gap closure strategies and correction boundaries

## MUST-NOT-FORGET

1. `__DRIFT_[TOPIC].md` must exist. If not found: report "No detection file. Run `/drift-detect` first."
2. Never re-derive the DoD. The file IS the contract. Trust it.
3. Atomic gap closure: one gap at a time. Fix, verify, update file.
4. Priority order: HIGH first, then MEDIUM, then LOW.
5. MISSED items cannot be fixed. Skip them. Only process FAIL items.
6. Spend full budget on thorough correction. Each fix must be verified before moving on.
7. Update tracking files (PROGRESS.md, NOTES.md) after significant corrections.

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: !NOTES.md or NOTES.md, FAILS.md

## Prerequisites

- `__DRIFT_[TOPIC].md` exists with Status: IN_PROGRESS or BLOCKED → proceed (resume correction)
- `__DRIFT_[TOPIC].md` not found → report error, suggest `/drift-detect`
- `__DRIFT_[TOPIC].md` Status: COMPLETE → report "Already complete. No gaps to close."

# EXECUTION

## Steps

```
Step 1: LOAD     - Read __DRIFT_[TOPIC].md, identify FAIL items
Step 2: FILL     - Close gaps in priority order
Step 3: FINALIZE - Update status, report
```

### Step 1: LOAD - Read Detection File

1. Locate `__DRIFT_[TOPIC].md`:
   - User specifies TOPIC → use that
   - Search working directory for `__DRIFT_*.md` files
   - If multiple found → list them, use most recent
2. Read file, extract all FAIL items as TODO list
3. Verify file integrity: Status should be IN_PROGRESS or BLOCKED

### Step 2: FILL - Close Gaps

Process FAIL items: HIGH first, then MEDIUM, then LOW.

For each FAIL item:

1. Read the criterion and its source document
2. Understand what "PASS" means for this item
3. Execute minimum change to close gap
4. Verify: does the item now PASS? (check actual output)
5. Update `__DRIFT_[TOPIC].md`: FAIL → PASS, check off TODO
6. Next item

If a gap cannot be closed:
- Mark BLOCKED with specific reason
- Move to next item

Session boundary: if context exhausted, update `__DRIFT_[TOPIC].md` with current state. File persists for resume.

### Step 3: FINALIZE

When all FAIL items are PASS or BLOCKED:

1. Update Status: all PASS/MISSED/N/A → `COMPLETE`, any BLOCKED → `BLOCKED`
2. Report summary:

```
## Drift Correction Summary

**Topic**: [TOPIC]
**Status**: [COMPLETE | BLOCKED]

**Corrections Made**: [count] gaps closed
**Blocked**: [count] (with reasons)
**Remaining MISSED**: [count] (unfixable, recorded only)

**Files Modified**: [list of files changed during correction]
```

## Stuck Detection

If 3 consecutive FAIL items cannot be closed:
1. Document in PROBLEMS.md
2. Mark remaining items BLOCKED with reason "stuck - 3 consecutive failures"
3. Proceed to FINALIZE

# FINALIZATION

## Verification

- [ ] All FAIL items resolved (PASS) or BLOCKED with reason
- [ ] `__DRIFT_[TOPIC].md` updated with final status
- [ ] No items left in FAIL status
- [ ] Each fix was verified after applying

## Output

- Updated `__DRIFT_[TOPIC].md` with final status
- Modified output files (gap closures applied)
- Correction summary reported to user

## Trigger

- `/drift-correct` - after `/drift-detect` completes
- `/drift-correct` - when resuming from a previous session (file persists)
- `/drift-correct [TOPIC]` - when multiple `__DRIFT_` files exist
