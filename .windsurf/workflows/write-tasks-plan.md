---
description: Create tasks plan document from IMPL/TEST
auto_execution_mode: 1
---

# Write Tasks Plan Workflow

Create partitioned task documents from IMPL plans. Combines `/partition` workflow with document creation.

## Required Skills

- @write-documents for TASKS template and document structure

## Prerequisites

- IMPL plan exists (`_IMPL_[TOPIC].md`)
- Optionally: TEST plan exists (`_TEST_[TOPIC].md`)

## Steps

1. **Run `/partition`**
   - Apply `/partition` workflow with STRATEGY if specified
   - Collect partitioned tasks

2. **Create Tasks Plan File**
   - Create `TASKS_[TOPIC].md` in session folder
   - Header block with Doc ID, Goal, Source documents

3. **Write Task Sections**
   - Group tasks by phase or component
   - Include dependencies between tasks
   - Mark parallel vs sequential tasks

4. **Add Verification Criteria**
   - Each task references test cases from TEST plan
   - Or defines temporary verification method

5. **Update PROGRESS.md**
   - Copy task list to "To Do" section
   - Link to TASKS document for details

## Document Structure

```markdown
# TASKS: [TOPIC] Tasks Plan

**Doc ID (TDID)**: [TOPIC]-TK01
**Feature**: [FEATURE_SLUG]
**Goal**: Partitioned tasks for [TOPIC] implementation
**Source**: `IMPL_[TOPIC].md [TOPIC-IP01]`, `TEST_[TOPIC].md [TOPIC-TP01]`
**Strategy**: PARTITION-[STRATEGY]

## Task Overview

- Total tasks: N
- Estimated total: X HHW
- Parallelizable: M tasks

## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Run existing tests, record pass/fail baseline
- [ ] Note pre-existing failures (not caused by this feature)

## Tasks

### Phase/Component Name

- [ ] **[TOPIC]-TK-001** - Description
  - Files: [files affected]
  - Done when: [specific completion criteria]
  - Verify: [commands to run]
  - Guardrails: [must not change X]
  - Depends: none
  - Parallel: [P] or blank
  - Est: 0.5 HHW

- [ ] **[TOPIC]-TK-002** - Description
  - Files: [files affected]
  - Done when: [specific completion criteria]
  - Verify: [commands to run]
  - Depends: TK-001
  - Est: 0.25 HHW

## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] Run /verify workflow
- [ ] Update PROGRESS.md - mark complete

## Dependency Graph

TK-001 ─> TK-003
TK-002 ─> TK-003
TK-003 ─> TK-004

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial tasks plan created from IMPL/TEST
```
