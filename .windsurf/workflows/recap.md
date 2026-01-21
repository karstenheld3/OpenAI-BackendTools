---
description: Analyze context, revisit plan, identify current status
auto_execution_mode: 1
---

# Recap Workflow

Backward-looking assessment of current state.

## Step 1: Read All Session Documents

Read in order (improvise if missing):

1. **NOTES.md** - Current phase, constraints, decisions
2. **PROGRESS.md** - Phase plan status (EXPLORE/DESIGN/IMPLEMENT/REFINE/DELIVER)
3. **_SPEC_*.md** - What we're building (requirements, FRs)
4. **_IMPL_*.md** - How we're building (implementation steps)
5. **_TEST_*.md** - How we verify (test cases)
6. **_TASKS_*.md** - Partitioned work items with checkboxes

## Step 2: Determine Exact Position

Verify down to individual item:

1. **Current phase** - Which of the 5 phases?
2. **Current document** - Which plan are we executing?
3. **Current task** - Which item in TASKS (or IMPL step)?
4. **Task status** - Checked or unchecked?

## Step 3: Output Status

```markdown
## Recap

**Phase**: [EXPLORE/DESIGN/IMPLEMENT/REFINE/DELIVER]
**Document**: [TASKS/IMPL filename]
**Current task**: [task ID and description]
**Status**: [done/in_progress/pending]
**Next**: [next unchecked item]
```

## When to Use

- After session resume
- When uncertain about state
- Before [CONTINUE]
- As first part of [GO]
