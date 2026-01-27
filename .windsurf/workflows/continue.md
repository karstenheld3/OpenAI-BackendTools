---
description: Forward-looking assessment, execute next items on plan
auto_execution_mode: 1
---

# Continue Workflow

Forward-looking execution of next steps in a plan.

## Step 1: Build Execution Sequence

Construct an ordered list of next actions by analyzing multiple sources:

**Mandatory re-read before continuing:**

**SESSION-BASED mode** - Re-read session folder documents:
- NOTES.md
- PROBLEMS.md
- PROGRESS.md
- FAILS.md
- LEARNINGS.md (if exists)

**PROJECT-WIDE mode** - Re-read workspace-level documents:
- README.md
- !NOTES.md or NOTES.md
- !PROBLEMS.md or PROBLEMS.md (if exists)
- !PROGRESS.md or PROGRESS.md (if exists)
- FAILS.md
- LEARNINGS.md (if exists)

Then build execution sequence:

**1.1 Analyze conversation context:**
- Scan recent messages for workflow suggestions (e.g., "Run `/session-archive` when ready")
- Check previous workflow outputs for successor workflows
- Note any explicit user instructions about next steps

**1.2 Check session lifecycle state** (SESSION-BASED mode):
- Lifecycle: Init → Work → Save → Resume → Finalize → Archive
- If resuming → check NOTES.md "Workflows to Run on Resume"
- Session lifecycle workflows (`/session-finalize`, `/session-archive`) may appear in sequence from conversation context (Step 1.1), but require `[CONFIRM]` before execution (see Step 2)

**1.3 Check progress and tasks:**
- Read PROGRESS.md for unchecked items in To Do / In Progress
- Read TASKS document (if exists) for next unchecked task
- If no TASKS, check IMPL plan for next step

**1.4 Merge into execution sequence:**
- Combine all sources into ordered list
- Workflow succession comes before task execution
- Format:

```markdown
## Execution Sequence

1. `/session-load` - Session resumed, ready to continue
2. [Next task from PROGRESS.md]
3. ...
```

**1.5 If sequence is empty:** Report "No pending work" and STOP.

## Step 2: Execute First Item

Take the first item from the execution sequence:

**If session lifecycle workflow** (`/session-finalize`, `/session-archive`):
- Output sequence with `[CONFIRM]` - do NOT execute automatically
- Wait for user to confirm with `/continue` or `/go`
- Only then execute the workflow

**If other workflow** (starts with `/`):
- Execute the workflow
- Remove from sequence when complete

**If task**:
- Execute the task
- Update PROGRESS.md / TASKS (mark as Done)

## Step 3: Loop or Stop

After each execution:

- **More items in sequence?** Return to Step 2
- **Phase gate reached?** Run gate check before proceeding
- **Sequence empty?** Report completion
- **Blocker encountered?** Report and wait for user

## Output

**After building sequence (Step 1):**

```markdown
## Execution Sequence

1. `/session-archive` - Session closed, ready to archive
2. Update README.md - From PROGRESS.md To Do
3. Run tests - From TASKS TK-005
```

**After each execution (Step 2-3):**

```markdown
## Continue

**Executed**: [item description]
**Result**: [OK/FAIL]
**Remaining**: [count] items in sequence
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
