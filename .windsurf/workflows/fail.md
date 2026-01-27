---
description: Record a failure in FAILS.md, either from user input or by analyzing context
auto_execution_mode: 1
---

# Fail Workflow

Record failures to prevent repetition. Can be triggered explicitly or run analysis to detect issues.

## Required Skills

- @write-documents for FAILS_TEMPLATE.md structure

## Trigger

- [ACTOR] reports a failure: `/fail [description]`
- Agent suspects something is wrong: `/fail` (no args)

## Step 1: Check for Explicit Input

If [ACTOR] provided a description:
- Use that as the failure description
- Skip to Step 3 (Classify Severity)

If no description provided:
- Proceed to Step 2 (Analyze Context)

## Step 2: Analyze Context (Discovery Mode)

Search for evidence of failures in order:

### 2.1 Recent Conversation
- Look for error messages shared by [ACTOR]
- Look for phrases like "doesn't work", "fails", "broken", "wrong"
- Look for corrections or rollbacks

### 2.2 Test Status
- Run test suite if available
- Check for failing tests
- Note which tests are red

### 2.3 Code State
- Check git status for uncommitted changes
- Look for TODO/FIXME comments added recently
- Check for syntax errors or lint issues

### 2.4 Logs
- Check application logs for errors
- Check build logs for failures
- Check console output from recent commands

### 2.5 Documents
- Check PROBLEMS.md for unresolved issues
- Check session NOTES.md for blocked items
- Check PROGRESS.md for stuck tasks

### 2.6 Exit Condition

If no significant issues found:
- Report: "No failures detected in current context"
- Exit workflow without creating entry

## Step 3: Classify Severity

Determine severity based on impact:

- **[CRITICAL]** - Will definitely cause production failure
- **[HIGH]** - Likely to cause failure under normal conditions
- **[MEDIUM]** - Could cause failure under specific conditions
- **[LOW]** - Minor issue, unlikely to cause failure

## Step 4: Collect Evidence

Gather supporting artifacts:

- **When**: Current timestamp
- **Where**: File/function/line or document section
- **What**: Exact problem description
- **Evidence**: Link, test output, or example proving the issue

## Step 5: Analyze Root Cause (Brief)

Quick assessment of why it went wrong:
- What assumption was incorrect?
- What was missed?
- Keep brief - detailed analysis is for `/learn` workflow

## Step 6: Suggest Fix

Brief recommendation for resolution:
- Immediate action to take
- Keep actionable and specific

## Step 7: Create FAILS Entry

Add entry to FAILS.md:

1. **Determine location (SESSION-FIRST rule)**:
   
   Check current work mode using AGEN states:
   
   **If SESSION-BASED** (working in `[SESSION_FOLDER]`):
   - Write to `[SESSION_FOLDER]/FAILS.md`
   - Create file if it doesn't exist
   - Session entries sync to workspace on `/session-finalize`
   
   **If PROJECT-WIDE** (no active session):
   - Write to `[WORKSPACE_FOLDER]/FAILS.md` or `[PROJECT_FOLDER]/FAILS.md`
   - For workspace-wide issues (DevSystem, tooling, MCP servers)
   - For issues affecting multiple projects

2. Generate ID: `[TOPIC]-FL-[NNN]`

3. Add entry at top of file using FAILS_TEMPLATE.md structure

4. Include code example if applicable (before/after)

## Step 8: Report

Confirm to [ACTOR]:
- Created `[TOPIC]-FL-NNN` in FAILS.md
- Brief summary of what was recorded
- Suggest `/learn` after problem is resolved for deeper analysis

## Quality Gate

Before completing:
- [ ] Severity correctly classified
- [ ] Evidence is concrete (not vague)
- [ ] Location is specific (file:line when applicable)
- [ ] Suggested fix is actionable
