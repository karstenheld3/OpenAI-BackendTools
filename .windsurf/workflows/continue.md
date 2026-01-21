---
description: Forward-looking assessment, execute next items on plan
auto_execution_mode: 1
---

# Continue Workflow

Forward-looking execution of next steps in a plan.

## Step 1: Identify Next Action

1. Read PROGRESS.md for current phase and status
2. Read TASKS document (if exists) for next unchecked task
3. If no TASKS, use IMPL plan steps

## Step 2: Execute Next Item

1. Execute the next task
2. Update PROGRESS.md / TASKS (mark as Done)
3. Proceed to next item

## Step 3: Loop or Stop

- **More tasks?** Continue to next item
- **Phase complete?** Check gate, transition if passes
- **All done?** Report completion

## Output

After each task:

```markdown
## Continue

**Executed**: [task description]
**Result**: [OK/FAIL]
**Next**: [next task or gate check]
```

## When to Use

- After `/recap` confirms state
- To execute plan items sequentially
- As second part of `/go`

## Stopping Conditions

- All tasks complete
- Blocker requires user input
- Gate check needed
- User interruption
