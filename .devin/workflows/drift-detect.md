---
description: Post-execution drift detection - build DoD, assess output, persist gaps
---

# Drift Detect Workflow

Post-execution drift detection. Runs AFTER a workflow or agent instruction completes. Builds a Definition-of-Done (DoD) from the original instruction, compares against actual output through drift lenses, and persists all gaps to `__DRIFT_[TOPIC].md`.

**Goal**: All instruction-following gaps identified, categorized, and persisted for correction

**Why**: Detection deserves a full context budget. Combining detection and correction in one pass causes shallow analysis (agent rushes detection to save tokens for fixing). Splitting guarantees thorough assessment.

Usage:
- `/drift-detect` - full detection across all drift categories, persist to `__DRIFT_[TOPIC].md`
- `/drift-detect [directive]` - detection with specific focus
- `/drift-detect log` - detect, persist to `__DRIFT_[TOPIC].md`, AND append to DRIFTS.md

**Scope Boundary**: This workflow only DETECTS and RECORDS. It does NOT fix anything. Use `/drift-correct` to close gaps. Use `/verify` for rule/convention compliance. Use `/critique` for logic flaws.

## Required Skills

- @skills:drift-correction for drift lenses, context detection, DoD extraction rules, and templates

## MUST-NOT-FORGET

1. Post-execution only: runs AFTER a workflow or instruction completes. Never before or during.
2. Re-read the original instruction BEFORE auditing - never audit from memory.
3. Two scored lenses (Output Structure, Process Discipline) + one observational lens (Meta-Criteria).
4. MISSED vs FAIL: MISSED = cannot retroactively fix. FAIL = fixable now.
5. DoD is the contract: once persisted, authoritative. Only add items for newly discovered requirements.
6. Detection only: Do NOT fix anything. Do NOT modify output files. Read-only analysis.
7. Spend full budget on thorough detection. No shortcuts - check EVERY source.

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: !NOTES.md or NOTES.md, FAILS.md

## Prerequisites

- A workflow or agent instruction has completed → proceed
- Work is still in progress → do NOT run this workflow
- `__DRIFT_[TOPIC].md` already exists → report "Detection already complete. Run `/drift-correct` to close gaps."

# CONTEXT-SPECIFIC

Context detection and DoD extraction rules are in `@skills:drift-correction` `DRIFT_DETECTION.md`. Read sections "Context Detection", "Default Sources", and the matching context section.

## No Context Match

If no SPEC/IMPL/TASKS and no research output exist: use Generic context. Build DoD entirely from conversation and planning artifacts (default sources).

# EXECUTION

## Steps

```
Step 1: ANALYZE  - Detect context, identify all sources
Step 2: EXTRACT  - Build DoD from sources (exhaustive)
Step 3: COMPARE  - Assess every DoD item against actual output
Step 4: PERSIST  - Write __DRIFT_[TOPIC].md (or DRIFTS.md in log mode)
Step 5: REPORT   - Summary to user
```

### Step 1: ANALYZE - Detect Context

1. Determine `[TOPIC]` from context:
   - User specifies topic explicitly: use that
   - Planning files exist (`__STRUT_[TOPIC].md`, `__TASKS_[TOPIC].md`): extract from filename
   - Fallback: derive from session folder name or conversation subject
2. Read `DRIFT_DETECTION.md` section "Context Detection" to determine context type
3. Identify ALL applicable sources (context-specific + default)

### Step 2: EXTRACT - Build DoD

Read EVERY source identified in Step 1. For each, extract DoD items per `DRIFT_DETECTION.md` extraction rules.

Thoroughness requirement: do not stop at "enough" items. Read every section of every source. Count items extracted per source. If a source has 0 items, explicitly note why.

### Step 3: COMPARE - Assess Output

For each DoD item, assess status per `DRIFT_DETECTION.md` section "Assessment Statuses".

For each item, record:
- Status (PASS / FAIL / MISSED / N/A)
- Evidence (what proves the status)

Note meta-criteria presence/absence (observational).

### Step 4: PERSIST

Working directory = session folder (SESSION-MODE) or project folder (PROJECT-MODE).

**Normal mode** (`/drift-detect` or `/drift-detect [directive]`):

Create `__DRIFT_[TOPIC].md` in working directory using template from `@skills:drift-correction` `DRIFT_TEMPLATE.md`.

**Log mode** (`/drift-detect log`):

After writing `__DRIFT_[TOPIC].md` (same as normal mode), ALSO:

1. Append all FAIL and MISSED items to `DRIFTS.md` in current working directory
2. Use format from `@skills:drift-correction` `DRIFTS_TEMPLATE.md`
3. If DRIFTS.md does not exist, create with header from template

### Step 5: REPORT

```
## Drift Detection Summary

**Topic**: [TOPIC]
**Context**: [Code Implementation | Deep Research | Generic]
**Directive**: [directive or "full audit"]

**Results**:
- Category 1 (Output Structure): [pass]/[total] PASS, [fail] FAIL
- Category 2 (Process Discipline): [pass]/[total] PASS, [fail] FAIL, [missed] MISSED
- Total gaps: [fail_count] FAIL + [missed_count] MISSED

**Meta-Criteria Observations**:
- Present: [list]
- Absent: [list]

**Next**: Run `/drift-correct` to close [fail_count] fixable gaps.
```

# FINALIZATION

## Verification

- [ ] Every source from Step 1 was actually read (not skipped)
- [ ] DoD item count matches expectation (no sources produced 0 items without explanation)
- [ ] `__DRIFT_[TOPIC].md` written (or DRIFTS.md appended in log mode)
- [ ] No modifications made to output files (detection only)

## Output

- `__DRIFT_[TOPIC].md` in working directory (all modes)
- DRIFTS.md entry appended (log mode, additional)
- Detection summary reported to user

## Trigger

- `/drift-detect` - after any `/build`, `/implement`, `/solve` completion
- `/drift-detect` - after `/deep-research` completion
- `/drift-detect [directive]` - when specific aspect needs assessment
- `/drift-detect log` - after any task to accumulate drift data
- As spot-check during long autonomous sessions (`/go`)
