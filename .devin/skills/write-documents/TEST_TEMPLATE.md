# TEST: [Component Name]

**Doc ID (TDID)**: [TOPIC]-TP[NN]
**Feature**: [FEATURE_SLUG]
**Goal**: [Single sentence describing test purpose]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)
**Target file**: `[path/to/test_file.py]`

**Depends on:**
- `_SPEC_[X].md` [[DOC_ID]] for requirements
- `_IMPL_[X].md` [[DOC_ID]] for implementation details

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## Table of Contents

1. [Overview](#1-overview)
2. [Scenario](#2-scenario)
3. [Test Strategy](#3-test-strategy)
4. [Test Priority Matrix](#4-test-priority-matrix)
5. [Test Data](#5-test-data)
6. [Test Cases](#6-test-cases)
7. [Test Phases](#7-test-phases)
8. [Helper Functions](#8-helper-functions)
9. [Cleanup](#9-cleanup)
10. [Verification Checklist](#10-verification-checklist)
11. [Document History](#11-document-history)

## 1. Overview

[Brief description of what this test covers]

## 2. Scenario

**Problem:** [What issue or behavior we're testing]

**Solution:** [How the tests verify correct behavior]

**What we don't want:**
- [Test anti-pattern 1]
- [Test anti-pattern 2]

## 3. Test Strategy

**Approach**: [unit | integration | snapshot-based]

**Snapshot-Based Verification** (if applicable):
1. Restore state from snapshot (or clean for first test)
2. Run operation with specific parameters
3. Compare actual state vs expected snapshot
4. Report pass/fail

## 4. Test Priority Matrix

### MUST TEST (Critical Business Logic)

- **`function_name()`** - module_name
  - Testability: **EASY**, Effort: Low
  - [Description of what to test]

### SHOULD TEST (Important Workflows)

- **`function_name()`** - module_name
  - Testability: Medium, Effort: Medium
  - [Description]

### DROP (Not Worth Testing)

- **`function_name()`** - Reason: [External dependency / UI-only / trivial]

## 5. Test Data

**Required Fixtures:**
- [Fixture 1]: [Description]
- [Fixture 2]: [Description]

**Setup:**
```python
# Setup code or description
```

**Teardown:**
```python
# Cleanup code or description
```

## 6. Test Cases

### Category 1: [Name] (N tests)

- **[PREFIX]-TC-01**: [Description] -> ok=true, [expected result]
- **[PREFIX]-TC-02**: [Error case] -> ok=false, [error message]

### Category 2: [Name] (N tests)

- **[PREFIX]-TC-03**: [Description] -> ok=true, [expected result]

## 7. Test Phases

Ordered execution sequence:

1. **Phase 1: Setup** - [Description]
2. **Phase 2: Core Tests** - [Description]
3. **Phase 3: Edge Cases** - [Description]
4. **Phase 4: Cleanup** - [Description]

## 8. Helper Functions

```python
# Reusable test utilities
def assert_state_matches(actual, expected): ...
def create_test_fixture(): ...
```

## 9. Cleanup

- [Artifact 1 to remove]
- [Artifact 2 to remove]

## 10. Verification Checklist

- [ ] All MUST TEST functions covered
- [ ] All test cases pass
- [ ] Coverage meets requirements
- [ ] Edge cases covered
- [ ] Cleanup executed

## 11. Document History

**[YYYY-MM-DD HH:MM]**
- Initial test plan created
