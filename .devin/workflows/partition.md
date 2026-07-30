---
description: Partition plans into discrete tasks
auto_execution_mode: 1
---

# Partition Workflow

Split IMPL plans into discrete, testable tasks and output to PROGRESS.md.

## Required Skills

- @write-documents for document structure

## MUST-NOT-FORGET

1. Apply changes immediately without asking for permission
2. Output to PROGRESS.md only - never create separate TASKS document
3. Each task max 0.5 HHW, atomic, testable
4. To create TASKS_[TOPIC].md document, use `/write-tasks-plan` instead

## Workflow

1. **Determine Strategy**
   - If STRATEGY parameter provided, use it
   - Check NOTES.md for partitioning hints
   - BUILD + technical work → PARTITION-DEPENDENCY
   - BUILD + user-facing → PARTITION-SLICE
   - High uncertainty → PARTITION-RISK
   - Default: PARTITION-DEFAULT (0.5 HHW chunks)

2. **Gather Input Documents**
   - SPEC (requirements, FR, DD)
   - IMPL (steps, edge cases)
   - TEST (test cases)

3. **Apply Strategy** (see Strategies section)

4. **Output to PROGRESS.md**

## Strategies

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

## Output Format

Update PROGRESS.md "To Do" section:

```markdown
## To Do

### [Phase] Phase

- [ ] **[TOPIC]-TK-001** - Task description (0.5 HHW)
- [ ] **[TOPIC]-TK-002** - Task description (0.25 HHW)
```

## Task Properties

Each task must be:
- **Atomic** - Implementable in one edit session between commits
- **Testable** - Has defined test cases or verifiable with temp script
- **Scoped** - Does one thing only
- **Estimated** - Max 0.5 HHW
