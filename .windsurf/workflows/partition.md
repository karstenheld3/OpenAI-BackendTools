---
description: Partition plans into discrete tasks
auto_execution_mode: 1
---

# Partition Workflow

Split implementation plans into discrete, testable tasks.

## Required Skills

- @write-documents for document structure

## Rules

- **Output to PROGRESS.md only** - Never create a separate TASKS document
- To create a TASKS_[TOPIC].md document, use /write-tasks-plan instead

## Step 1: Determine Strategy

If STRATEGY parameter provided, use it. Otherwise:
1. Check NOTES.md for partitioning hints
2. If BUILD + technical work → PARTITION-DEPENDENCY
3. If BUILD + user-facing → PARTITION-SLICE
4. If high uncertainty noted → PARTITION-RISK
5. Default: PARTITION-DEFAULT (0.5 HHW chunks)

## Step 2: Gather Input Documents

Read all relevant documents in order:
1. SPEC (requirements, FR, DD)
2. IMPL (steps, edge cases)
3. TEST (test cases)

## Step 3: Apply Strategy

### PARTITION-DEFAULT

- Estimate HHW per item
- Chunk into max 0.5 HHW tasks
- Preserve document order

### PARTITION-DEPENDENCY

- Build component dependency graph
- Topological sort (leaves first)
- Group independent items as parallel

### PARTITION-SLICE

- Map each AC/FR to required components
- Create one task per vertical slice
- Order by value or risk

### PARTITION-RISK

- Rate items by uncertainty
- Order unknowns before knowns
- Front-load integration points

## Step 4: Output to PROGRESS.md

Update PROGRESS.md "To Do" section with partitioned tasks:

```markdown
## To Do

### [Phase] Phase

- [ ] **[TOPIC]-TK-001** - Task description (0.5 HHW)
- [ ] **[TOPIC]-TK-002** - Task description (0.25 HHW)
...
```

## Task Properties

Each task must be:
- **Atomic** - Implementable in one edit session between commits
- **Testable** - Has defined test cases or can be verified with temp script
- **Scoped** - Does one thing only
- **Estimated** - Has HHW estimate (target: max 0.5 HHW)
