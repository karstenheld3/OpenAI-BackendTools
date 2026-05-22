---
description: Autonomous loop until goal reached
---

# Go Workflow

Goal: Execute plan to completion without user interaction.

Fully autonomous execution loop. Agent runs independently until goal is reached or a hard stop is hit.

## Autonomous Mode

**`[ACTOR] = agent`** for the entire duration of `/go` execution.

All verbs targeting `[ACTOR]` are self-resolved:
- `[CONSULT]` → agent decides using available context, logs decision
- `[CONFIRMS]` → agent self-confirms if evidence exists, logs rationale
- `[QUESTION]` → agent researches answer using tools, logs finding
- `[PROPOSE]` → agent evaluates options and picks best, logs choice
- `[RECOMMEND]` → agent accepts if evidence supports it, logs rationale

### Autonomous Decision Protocol

When facing choices, the agent MUST NOT ask the user. Instead:

1. Identify options
2. Evaluate each option against (re-read if needed):
   - `agent-behavior.md` - execution patterns, confirmation rules
   - `core-conventions.md` - formatting, structure rules
   - `/verify` workflow - quality standards for the artifact type
   - Relevant skills and their rules
   - Current SPEC, IMPL, TEST documents (if they exist)
3. Pick the option that best satisfies the rules
4. Log decision with rationale to the tracking document (see Decision Logging)
5. Proceed without waiting

### Decision Logging

Log autonomous decisions to the main progress tracking document:

- If `__TASKS_*.md` exists and tracks progress → log decisions there
- If `PROGRESS.md` is the main tracking document → log decisions there
- If neither exists → create `__TASKS_[TOPIC].md` using @skills:write-documents, log there

Format: `[DECISION] <what was decided> - <rationale> - <rules consulted>`

### Safety Protocol

The agent CAN perform destructive actions (delete, deploy, restructure) if they are **in scope** of the initial instructions, prompts, and workflows invoked before `/go`. To stay recoverable:

- Before deleting substantial data or crucial files: create backup (zip or copy)
- Use `/commit` to proceed in self-contained, reversible, traceable steps
- Commit before AND after risky operations

Backups and zips created during `/go` MUST NOT be deleted by the agent, including during cleanup after goal is reached. Only the user may delete them.

**Hard stop (ONLY case):** Agent proposes a destructive action that is **NOT in scope** when compared with initial instructions, prompts, and workflows invoked before `/go`. Stop and escalate to user.

## Required Reading

- `rules/devsystem-core.md` - Workflow Reference lists all available workflows and skills

## MUST-NOT-FORGET

- `[ACTOR] = agent` - never ask the user, decide and proceed
- Check if goal already reached (Step 1) before any work
- Log blockers to PROBLEMS.md immediately
- Run multi-layer completion check before declaring goal reached
- Never sacrifice requirements - implement 100%
- No shortcuts, no lazy programming

## Step 1: Multi-Layer Completion Check

Check ALL layers, not just STRUT:

1. **TASKS layer**: Read `__TASKS_*.md` - any unchecked `[ ]` items?
2. **IMPL layer**: Read `_IMPL_*.md` - any unchecked IS-XX steps?
3. **TEST layer**: Read `_TEST_*.md` - any unchecked TC-XX?
4. **STRUT layer**: All Deliverables checked? Final Transition = `[END]`?
5. **PROGRESS layer**: Any items in "To Do" or "In Progress"?

ALL layers that exist must show complete. If ANY layer has unchecked items:
- Do NOT declare goal reached
- Log which layer has gaps
- Proceed to Step 2

If all layers complete:
```
Goal already reached. No further work needed.
```
Stop. Do not re-verify on subsequent `/go` calls.

## Step 2: Recap

Run `/recap` to determine:
- Last completed action
- Current state
- Any blockers

## Step 3: Pre-Flight Check

1. Gather more context if unclear
2. Verify stop/acceptance criteria exist
3. Make internal MUST-NOT-FORGET list from conversation and plan documents
4. List all scripts and skills needed for task completion

## Step 4: Execute

Run `/continue` to:
- Execute next task from plan
- Update progress tracking document
- Check for completion

## Step 5: Loop

```
iteration_count = 0
WHILE goal not reached AND iteration_count < 10:
    iteration_count += 1
    /recap
    /continue

    IF iteration_count % 5 == 0:
        Run multi-layer completion check (Step 1)
        Output iteration count and remaining work summary

    IF blocker:
        Classify: TECHNICAL / KNOWLEDGE / SCOPE
        Log to PROBLEMS.md

        IF TECHNICAL:
            Try up to 3 alternative approaches
            If all fail: simplify, implement partial, log remainder

        IF KNOWLEDGE:
            [RESEARCH] using available tools
            Make [UNVERIFIED] assumption, document it, proceed

        IF SCOPE:
            Split: implement what's in scope
            Create new task for out-of-scope part
            Continue with next task

        IF blocker unresolved after alternatives:
            /write-info `.tmp_INFO_[BLOCKER].md` (root cause analysis)
            /critique -> /reconcile
            If still stuck: Hard stop, escalate to user
```

## Stopping Conditions

- All layers complete (multi-layer completion check passes)
- Hard stop triggered (see Safety Protocol above)
- User interruption
- Blocker unresolved after all self-resolution attempts

## Idempotent Behavior

Multiple `/go` commands on completed work:

1. First `/go` after completion: Output "Goal already reached" message
2. Subsequent `/go`: Same message, no re-verification, no action

This prevents:
- Wasted tokens on redundant verification
- Misinterpreting queued `/go` as dissatisfaction
- Overengineering completed deliverables