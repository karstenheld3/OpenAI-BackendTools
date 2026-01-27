---
description: Autonomous loop until goal reached
auto_execution_mode: 1
---

# Go Workflow

Autonomous execution loop using `/recap` and `/continue`.

## Step 0: Completion Check

Before any work, check if goal is already reached:

1. Read STRUT plan (PROGRESS.md or session document)
2. Run `/verify` (STRUT Transition Phase) to check:
   - All Deliverables in final phase checked?
   - All Objectives verified via linked Deliverables?
   - Final Transition points to `[END]`?

**If already complete:**
```
Goal already reached. No further work needed.
Last completed: [final deliverable]
```
→ Stop. Do not execute. Do not re-verify on subsequent `/go` calls.

**If not complete:** Proceed to Pre-Flight Check.

## Step 1: Pre-Flight Check

1. Do we have enough context? If unclear, ask user.
2. Do we have stop or acceptance criteria?
3. Re-read conversation, make internal MUST-NOT-FORGET list.

## Step 2: Execution Loop

```
WHILE goal not reached:
    /recap   # Assess current state
    /continue # Execute next item
    
    IF blocker:
        Ask user for guidance
        WAIT for response
```

## Step 3: Recap

Run `/recap` to determine:
- Last completed action
- Current state
- Any blockers

## Step 4: Continue

Run `/continue` to:
- Execute next task from plan
- Update progress
- Check for completion

## Step 5: Loop or Stop

- **Goal reached?** Stop, output summary
- **Blocker?** Log to PROBLEMS.md, ask user
- **More work?** Return to Step 3

## Stopping Conditions

- All tasks complete (final Transition = `[END]` checked)
- Blocker requires user input
- User interruption
- Retry limit exceeded (5 attempts for MEDIUM/HIGH complexity)

## Idempotent Behavior

Multiple `/go` commands on completed work:

1. First `/go` after completion: Output "Goal already reached" message
2. Subsequent `/go`: Same message, no re-verification, no action

This prevents:
- Wasted tokens on redundant verification
- Misinterpreting queued `/go` as dissatisfaction
- Overengineering completed deliverables