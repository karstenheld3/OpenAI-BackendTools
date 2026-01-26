---
description: Extract lessons from resolved problems through structured retrospective analysis
auto_execution_mode: 1
---

# Learn Workflow

Run after a problem is marked resolved in PROBLEMS.md to extract transferable lessons.

## Required Skills

- @write-documents for LEARNINGS_TEMPLATE.md structure

## Trigger

- Problem marked as resolved in PROBLEMS.md
- User requests `/learn [TOPIC]-PR-NNN`
- User requests `/learn` (no args) - runs discovery mode

## Step 0: Discovery Mode (if no context provided)

If [ACTOR] did not specify a problem ID or learning objective:

1. Run `/fail` workflow first to detect current issues
2. If `/fail` creates a new entry, use that as the learning target
3. If `/fail` exits without finding issues, report "No failures detected" and exit

## Step 1: Identify Problem

Read the resolved problem entry:
- Problem ID (e.g., `STRUT-PR-003`)
- Original description
- Solution applied
- Any linked FAILS.md entries

## Step 2: Classify Original Problem Type

Determine what was being attempted when the problem occurred:

**If BUILD workflow:**
- COMPLEXITY-LOW (single file, clear scope)
- COMPLEXITY-MEDIUM (multiple files, some dependencies)
- COMPLEXITY-HIGH (breaking changes, new patterns)

**If SOLVE workflow:**
- RESEARCH (explore topic, gather information)
- ANALYSIS (deep dive into data or situation)
- EVALUATION (compare options, make recommendations)
- WRITING (create documents, books, reports)
- DECISION (choose between alternatives)
- HOTFIX (production down)
- BUGFIX (defect investigation)
- CHORE (maintenance analysis)
- MIGRATION (data or system migration)

## Step 3: Reconstruct Context

Answer these questions by reviewing conversation history, commits, and documents:

1. What information was available at decision time?
2. What information was NOT available but should have been?
3. What time/resource constraints existed?

## Step 4: Reconstruct Assumptions

List all assumptions made during planning or design:

- Mark as `[VERIFIED]` if confirmed correct
- Mark as `[UNVERIFIED]` if made without evidence
- Mark as `[CONTRADICTS]` if conflicted with reality

## Step 5: Reconstruct Rationale

Document the reasoning behind decisions:

1. What requirements were specified? (FR, DD, IG references)
2. What design decisions were made and why?
3. What trade-offs were accepted?

## Step 6: Compare to Actual Outcome

Analyze the gap between expectation and reality:

1. What actually happened?
2. At what point did the plan diverge from reality?
3. What signals were missed or ignored?

## Step 7: Collect Evidence

Gather supporting artifacts:

- Conversation excerpts (key decisions, misunderstandings)
- Code diffs and commits (what changed, what broke)
- Error logs and test output
- Document references (SPEC, IMPL, TEST sections)

## Step 8: Build Problem Dependency Tree

Create a tree showing causal relationships:

```
[Root Cause]
├─> [Contributing Factor 1]
│   └─> [Symptom A]
└─> [Contributing Factor 2]
    ├─> [Symptom B]
    └─> [Symptom C]
```

Work backwards from symptoms to identify the root cause.

## Step 9: Identify Root Cause and Prevention

Formulate three statements:

1. **Root cause**: Single sentence identifying the fundamental issue
2. **Counterfactual**: "If we had [X], then [Y]"
3. **Prevention**: "Next time, we should [actionable guidance]"

## Step 10: Create Learning Entry

Add entry to LEARNINGS.md using LEARNINGS_TEMPLATE.md structure:

1. **Determine location (SESSION-FIRST rule)**:
   
   Check current work mode using AGEN states:
   
   **If SESSION-BASED** (working in `[SESSION_FOLDER]`):
   - Write to `[SESSION_FOLDER]/LEARNINGS.md`
   - Create file if it doesn't exist
   - Session entries sync to workspace on `/session-close`
   
   **If PROJECT-WIDE** (no active session):
   - Write to `[WORKSPACE_FOLDER]/LEARNINGS.md`

2. Assign ID: `[TOPIC]-LN-[NNN]`

3. Fill all sections from steps 2-9

4. Place at top of file

## Step 11: Update Linked FAILS Entries

Search FAILS.md for entries linked to this problem:

1. Find entries with matching TOPIC or explicit problem reference
2. Update "Why it went wrong" with root cause insight
3. Update "Suggested fix" with prevention guidance
4. Add code examples if applicable

## Quality Gate

Before completing:
- [ ] Problem type correctly classified
- [ ] All assumptions identified and labeled
- [ ] Root cause is actionable (not just "we made a mistake")
- [ ] Prevention guidance is specific (not just "be more careful")
- [ ] Linked FAILS entries updated
