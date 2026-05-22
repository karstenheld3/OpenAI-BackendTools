# IMPL: [Feature Name]

**Doc ID (TDID)**: [TOPIC]-IP[NN]
**Feature**: [FEATURE_SLUG]
**Goal**: [Single sentence describing what to implement]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)

**Target files**:
- `[path/to/file1.py]` (NEW)
- `[path/to/file2.py]` (EXTEND +50 lines)
- `[path/to/file3.py]` (MODIFY)

**Depends on:**
- `_SPEC_[X].md` [[DOC_ID]] for [what it provides]

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## Table of Contents

1. [File Structure](#1-file-structure)
2. [Edge Cases](#2-edge-cases)
3. [Implementation Steps](#3-implementation-steps)
4. [Logging Preview](#4-logging-preview)
5. [Test Cases](#5-test-cases)
6. [Verification Checklist](#6-verification-checklist)
7. [Document History](#7-document-history)

## 1. File Structure

```
[folder]/
├── [file1.py]    # [Description] (~N lines) [NEW]
├── [file2.py]    # [Description] [EXTEND +50 lines]
└── [subfolder]/
    └── [file3.py]  # [Description] [MODIFY]
```

## 2. Edge Cases

Derive from domain objects and actions:

- **[PREFIX]-IP01-EC-01**: Empty input list -> Return empty result, log warning
- **[PREFIX]-IP01-EC-02**: Network timeout -> Retry 3 times, then fail with error
- **[PREFIX]-IP01-EC-03**: Duplicate ID -> Skip and log, continue processing

**Categories to consider:**
- Input boundaries (empty, null, max length, invalid format)
- State transitions (invalid state, concurrent modifications)
- External failures (network, file locked, permission denied)
- Data anomalies (missing references, corrupt data)

## 3. Implementation Steps

### [PREFIX]-IP01-IS-01: [Action Description]

**Location**: `filename.py` > `function_name()` or after `existing_function()`

**Action**: [Add | Modify | Remove] [description]

**Code**:
```python
def new_function(...):
  ...
```

**Note**: [Any gotchas or important details]

### [PREFIX]-IP01-IS-02: [Action Description]

**Location**: `filename.py` > `class_name`

**Action**: [Add | Modify | Remove] [description]

**Code**:
```python
# Outline only - avoid implementation detail
def another_function(...): ...
```

**BAD** (too much detail):
```python
def renderJobRow(job):
  const actions = renderJobActions(job);
  const formatTimestamp = (ts) => {
    if (!ts) return '';
    return ts.substring(0, 19).replace('T', ' ');
  };
  # ... 20 more lines
```

**GOOD** (outline only):
```python
# Generate <tr> HTML for single job
def renderJobRow(job): ...
```

## 4. Logging Preview

*(If implementation produces no logged output, state: "N/A: [reason, e.g., pure data transform with no console output]")*

Show the exact log output the implementation will produce for key operations. This is the contract between SPEC logging requirements and implementation. Follow @skills:coding-conventions logging rules.

**[Operation name]:**
```
[Exact log output following Announce > Track > Report pattern]
[Include success path, error path, and skip path]
```

**Error case - [error scenario]:**
```
[Exact log output showing error handling]
```

## 5. Test Cases

### Category 1: [Name] (N tests)

- **[PREFIX]-IP01-TC-01**: [Description] -> ok=true, [expected result]
- **[PREFIX]-IP01-TC-02**: [Error case] -> ok=false, [error message]

### Category 2: [Name] (N tests)

- **[PREFIX]-IP01-TC-03**: [Description] -> ok=true, [expected result]

## 6. Verification Checklist

### Prerequisites
- [ ] **[PREFIX]-IP01-VC-01**: Related specs read and understood
- [ ] **[PREFIX]-IP01-VC-02**: Backward compatibility test created (if applicable)

### Implementation
- [ ] **[PREFIX]-IP01-VC-03**: IS-01 completed
- [ ] **[PREFIX]-IP01-VC-04**: IS-02 completed

### Validation
- [ ] **[PREFIX]-IP01-VC-10**: All test cases pass
- [ ] **[PREFIX]-IP01-VC-11**: Manual verification in UI

## 7. Document History

**[YYYY-MM-DD HH:MM]**
- Initial implementation plan created
