# SPEC: [Component Name]

**Doc ID (TDID)**: [TOPIC]-SP[NN]
**Feature**: [FEATURE_SLUG]
**Goal**: [Single sentence describing what to specify]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)
**Target file**: `[path/to/file.py]`

**Depends on:**
- `_SPEC_[X].md [TOPIC-SP01]` for [what it provides]

**Does not depend on:**
- `_SPEC_[Y].md [TOPIC-SP02]` (explicitly exclude if might seem related)

## MUST-NOT-FORGET

- [Critical rule 1]
- [Critical rule 2]

## Table of Contents

1. [Scenario](#1-scenario)
2. [Context](#2-context)
3. [Domain Objects](#3-domain-objects)
4. [Functional Requirements](#4-functional-requirements)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [Design Decisions](#6-design-decisions)
7. [Implementation Guarantees](#7-implementation-guarantees)
8. [Key Mechanisms](#8-key-mechanisms)
9. [Action Flow](#9-action-flow)
10. [Data Structures](#10-data-structures)
11. [User Actions](#11-user-actions) *(UI specs only)*
12. [UX Design](#12-ux-design) *(UI specs only)*
13. [Logging Requirements](#13-logging-requirements)
14. [Implementation Details](#14-implementation-details)
15. [Document History](#15-document-history)

## 1. Scenario

**Problem:** [Real-world problem description]

**Solution:**
- [Approach point 1]
- [Approach point 2]

**What we don't want:**
- [Anti-pattern 1]
- [Anti-pattern 2]

## 2. Context

[Project background, related systems, how this component fits]

## 3. Domain Objects

### [ObjectName]

A **[ObjectName]** represents [description].

**Storage:** `path/to/storage/`
**Definition:** `config.json`

**Key properties:**
- `property_1` - [description]
- `property_2` - [description]

**Schema:**
```json
{
  "field1": "value",
  "field2": 123
}
```

## 4. Functional Requirements

**BAD:**
```
- Toast notifications should support info, success, error types
- Auto-dismiss should be configurable
```

**GOOD:**
```
**UI-FR-01: Toast Notifications**
- Support info, success, error, warning message types
- Auto-dismiss configurable per toast (default 5000ms)
```

**[PREFIX]-FR-01: [Requirement Title]**
- [Requirement detail 1]
- [Requirement detail 2]

**[PREFIX]-FR-02: [Requirement Title]**
- [Requirement detail]

## 5. Non-Functional Requirements

Requirements that constrain how the system operates rather than what it does. Use `[TOPIC]-NFR-[NN]` IDs.

Common categories (include only those applicable):
- **Performance** - response time, throughput, resource usage
- **Reliability** - availability, recovery, fault tolerance
- **Security** - authentication, authorization, data protection
- **Usability** - accessibility, learnability, error handling UX
- **Observability** - monitoring, logging, alerting, diagnostics
- **Scalability** - load limits, growth capacity, degradation behavior
- **Compliance** - regulatory, legal, audit requirements
- **Localization** - language support, timezone handling, character encoding

**[PREFIX]-NFR-01: [Category - Requirement Title]**
- [Measurable constraint with threshold]
- [Verification method]

**[PREFIX]-NFR-02: [Category - Requirement Title]**
- [Measurable constraint]

## 6. Design Decisions

**[PREFIX]-DD-01:** [Decision description]. Rationale: [Why this decision].

**[PREFIX]-DD-02:** [Decision description]. Rationale: [Why this decision].

## 7. Implementation Guarantees

**[PREFIX]-IG-01:** [What the implementation must guarantee]

**[PREFIX]-IG-02:** [What the implementation must guarantee]

## 8. Key Mechanisms

[Technical patterns, algorithms, declarative approaches used]

## 9. Action Flow

Document call chains with box-drawing characters (2-space indentation compatible):

```
User clicks [Button]
├─> functionA(param)
│   ├─> fetch(`/api/endpoint`)
│   │   └─> On success:
│   │       ├─> updateState()
│   │       └─> renderUI()
```

## 10. Data Structures

**Request/Response Example:**
```
<start_json>
{"id": 42, "state": "running"}
</start_json>
<end_json>
{"id": 42, "state": "completed", "result": "ok"}
</end_json>
```

## 11. User Actions

*(For UI specs only)*

- **[Action Name]**: [Description of user interaction and expected result]

## 12. UX Design

*(For UI specs only)*

Use ASCII box diagrams. Show ALL buttons and actions:

```
+-----------------------------------------------------------------------+
|  Component Name                                                       |
|                                                                       |
|  [Button 1]  [Button 2]                                               |
|                                                                       |
|  +-----+----------+---------+--------------------------------------+  |
|  | ID  | Name     | Status  | Actions                              |  |
|  +-----+----------+---------+--------------------------------------+  |
|  | 1   | Item A   | active  | [Edit] [Delete]                      |  |
|  +-----+----------+---------+--------------------------------------+  |
+-----------------------------------------------------------------------+
```

## 13. Logging Requirements

*(If implementation produces no output, state: "N/A: [reason, e.g., pure library with no console output]")*

Use decision tree from SPEC-LG-01 (@skills:write-documents `SPEC_RULES.md`) to identify applicable types. Reference @skills:coding-conventions logging rules.

**Applicable logging types:**
- [ ] User-Facing (UF) - `LOGGING-RULES-USER-FACING.md`
- [ ] App-Level (AP) - `LOGGING-RULES-APP-LEVEL.md`
- [ ] Script-Level (SC) - `LOGGING-RULES-SCRIPT-LEVEL.md`

**[Type] logging:**
- **Audience**: [Who reads this output]
- **Goal**: [What the reader must learn]
- **Key operations**: [Which operations produce logged output]

**Expected output for [key operation]:**
```
[Log output example following Announce > Track > Report pattern]
```

## 14. Implementation Details

[Code organization, function signatures, module structure]

## 15. Document History

**[YYYY-MM-DD HH:MM]**
- Initial specification created
