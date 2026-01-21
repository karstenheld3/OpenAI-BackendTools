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
5. [Design Decisions](#5-design-decisions)
6. [Implementation Guarantees](#6-implementation-guarantees)
7. [Key Mechanisms](#7-key-mechanisms)
8. [Action Flow](#8-action-flow)
9. [Data Structures](#9-data-structures)
10. [User Actions](#10-user-actions) *(UI specs only)*
11. [UX Design](#11-ux-design) *(UI specs only)*
12. [Implementation Details](#12-implementation-details)
13. [Document History](#13-document-history)

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

## 5. Design Decisions

**[PREFIX]-DD-01:** [Decision description]. Rationale: [Why this decision].

**[PREFIX]-DD-02:** [Decision description]. Rationale: [Why this decision].

## 6. Implementation Guarantees

**[PREFIX]-IG-01:** [What the implementation must guarantee]

**[PREFIX]-IG-02:** [What the implementation must guarantee]

## 7. Key Mechanisms

[Technical patterns, algorithms, declarative approaches used]

## 8. Action Flow

Document call chains with box-drawing characters (2-space indentation compatible):

```
User clicks [Button]
├─> functionA(param)
│   ├─> fetch(`/api/endpoint`)
│   │   └─> On success:
│   │       ├─> updateState()
│   │       └─> renderUI()
```

## 9. Data Structures

**Request/Response Example:**
```
<start_json>
{"id": 42, "state": "running"}
</start_json>
<end_json>
{"id": 42, "state": "completed", "result": "ok"}
</end_json>
```

## 10. User Actions

*(For UI specs only)*

- **[Action Name]**: [Description of user interaction and expected result]

## 11. UX Design

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

## 12. Implementation Details

[Code organization, function signatures, module structure]

## 13. Document History

**[YYYY-MM-DD HH:MM]**
- Initial specification created
