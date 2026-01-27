# TASKS Template

Template for creating task plan documents from partitioned IMPL/TEST plans.

## Header Block

```markdown
# TASKS: [TOPIC] Tasks Plan

**Doc ID (TDID)**: [TOPIC]-TK01
**Feature**: [FEATURE_SLUG]
**Goal**: Partitioned tasks for [TOPIC] implementation
**Source**: `IMPL_[TOPIC].md [TOPIC-IP01]`, `TEST_[TOPIC].md [TOPIC-TP01]`
**Strategy**: PARTITION-[STRATEGY]
```

## Task Overview Section

```markdown
## Task Overview

- Total tasks: N
- Estimated total: X HHW
- Parallelizable: M tasks
```

## Task 0 - Baseline (MANDATORY)

Always include as first task:

```markdown
## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Run existing tests, record pass/fail baseline
- [ ] Note pre-existing failures (not caused by this feature)
```

## Task Item Structure

```markdown
- [ ] **[TOPIC]-TK-001** - Description
  - Files: [files affected]
  - Done when: [specific completion criteria]
  - Verify: [commands to run]
  - Guardrails: [must not change X]
  - Depends: none | TK-NNN
  - Parallel: [P] or blank
  - Model: Sonnet | Opus | Haiku
  - Est: 0.5 HHW
```

**Required fields:**
- Task ID and description
- Files affected
- Done when (completion criteria)
- Est (HHW estimate)

**Optional fields:**
- Verify (commands)
- Guardrails (constraints)
- Depends (dependencies)
- Parallel marker
- Model (for auto model switching)

## Model Hints

Tasks may include model hints for auto model switching.

**Source:** Model definitions and activity mappings are in `!NOTES.md` under `## Cascade Model Switching`.

Model hints are recommendations - agent decides based on actual task.

## Task N - Final Verification (MANDATORY)

Always include as last task:

```markdown
## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] Run /verify workflow
- [ ] Update PROGRESS.md - mark complete
```

## Dependency Graph Section

```markdown
## Dependency Graph

TK-001 ─> TK-003
TK-002 ─> TK-003
TK-003 ─> TK-004
```

## Document History Section

```markdown
## Document History

**[YYYY-MM-DD HH:MM]**
- Initial tasks plan created from IMPL/TEST
```

## Full Example

```markdown
# TASKS: AUTH Tasks Plan

**Doc ID (TDID)**: AUTH-TK01
**Feature**: user-authentication
**Goal**: Partitioned tasks for AUTH implementation
**Source**: `IMPL_AUTH.md [AUTH-IP01]`, `TEST_AUTH.md [AUTH-TP01]`
**Strategy**: PARTITION-DEPENDENCY

## Task Overview

- Total tasks: 5
- Estimated total: 2.5 HHW
- Parallelizable: 2 tasks

## Task 0 - Baseline (MANDATORY)

Run before starting any implementation:
- [ ] Run existing tests, record pass/fail baseline
- [ ] Note pre-existing failures (not caused by this feature)

## Tasks

### Data Layer

- [ ] **AUTH-TK-001** - Create User model
  - Files: src/models/user.py
  - Done when: User model with email, password_hash fields exists
  - Verify: python -m pytest tests/models/
  - Est: 0.5 HHW

### Service Layer

- [ ] **AUTH-TK-002** - Implement password hashing
  - Files: src/services/auth.py
  - Done when: hash_password and verify_password functions work
  - Verify: python -m pytest tests/services/test_auth.py
  - Guardrails: Must use bcrypt, not MD5
  - Depends: TK-001
  - Est: 0.5 HHW

- [ ] **AUTH-TK-003** - Implement JWT tokens
  - Files: src/services/auth.py
  - Done when: create_token and verify_token functions work
  - Verify: python -m pytest tests/services/test_auth.py
  - Parallel: [P]
  - Est: 0.5 HHW

### API Layer

- [ ] **AUTH-TK-004** - Create login endpoint
  - Files: src/api/auth.py
  - Done when: POST /login returns JWT on valid credentials
  - Verify: python -m pytest tests/api/test_auth.py
  - Depends: TK-002, TK-003
  - Est: 0.5 HHW

## Task N - Final Verification (MANDATORY)

Run after all tasks complete:
- [ ] Compare test results to Task 0 baseline
- [ ] New failures = regressions (must fix)
- [ ] Run /verify workflow
- [ ] Update PROGRESS.md - mark complete

## Dependency Graph

TK-001 ─> TK-002 ─> TK-004
          TK-003 ─> TK-004

## Document History

**[2026-01-17 14:35]**
- Initial tasks plan created from IMPL/TEST
```
