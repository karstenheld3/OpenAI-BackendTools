# Workflow Template

Template for writing Windsurf workflows (or Claude Code commands).

## Workflow Structure

```markdown
---
description: [Brief description of what the verb does]
auto_execution_mode: 1
---

# [Verb Name] Workflow

[Brief description in plain English - no AGEN verb references]

## Required Skills
- @skill-name for [what it provides]

## Rules
- [Constraints that always apply]

## Step 1: Context Discovery
[Analyze what documents exist, determine strategy]

## Step 2: Gather Input
[Read relevant documents]

## Step 3: Execute
[Perform the verb action]

## Step 4: Output
[Where and how to write results]
```

## General vs Specific Parts

Workflows have two distinct parts:

**General Part** (verb knowledge):
- What the verb does
- Required skills
- Rules and constraints
- Output format

**Specific Part** (context branching):
- What documents exist?
- What strategy applies?
- What scope is relevant?

## Context Discovery Pattern

Workflows must analyze context before acting:

```markdown
## Context Branching

Check what documents exist and proceed accordingly:

### IMPL exists
[Steps when IMPL document is found]

### TEST exists (no IMPL)
[Steps when only TEST document is found]

### SPEC exists (no IMPL, no TEST)
[Steps when only SPEC document is found]
```

## Strategy Pattern

For verbs that support multiple strategies:

```markdown
## Step 1: Determine Strategy

If STRATEGY parameter provided, use it. Otherwise:
1. Check NOTES.md for hints
2. If [condition A] → STRATEGY-X
3. If [condition B] → STRATEGY-Y
4. Default: STRATEGY-DEFAULT
```

## Output Rules

- Verb workflows update tracking files (PROGRESS.md, PROBLEMS.md)
- Document creation requires explicit `[WRITE-*]` verb or dedicated workflow
- Example: `/partition` updates PROGRESS.md, `/write-tasks-plan` creates TASKS document

## Examples

- `/partition` - Context discovery + strategy selection, outputs to PROGRESS.md
- `/test` - Context branching by SCOPE-*, executes appropriate test type
- `/implement` - Context branching by document existence, calls other workflows
