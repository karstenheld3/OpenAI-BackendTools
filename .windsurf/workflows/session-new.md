---
description: Initialize a new development session
auto_execution_mode: 1
---

## Required Skills

Invoke these skills before proceeding:
- @session-management for session folder structure and tracking files

## Step 1: Check for Existing Session

Check if the user has given you a [SESSION_FOLDER] to work in.
If path already contains NOTES.md, PROGRESS.md, PROBLEMS.md: Execute /session-load instead.

## Step 2: Create Session Folder

If no [SESSION_FOLDER] provided, create one in the default sessions folder with naming scheme:
`_YYYY-MM-DD_[PROBLEM_DESCRIPTION]/`
[PROBLEM_DESCRIPTION] should contain only alphanumerical characters without spaces.

## Step 3: Create Session Documents

In the [SESSION_FOLDER], create tracking files from @session-management templates:

- `NOTES.md` - Include "Current Phase" section for phase tracking. If user provides large prompts (>120 tokens), record them verbatim in "User Prompts" section
- `PROGRESS.md` - Include "Phase Plan" section with 5 phases
- `PROBLEMS.md` - Derive and list all problems from user's initial request. Each problem gets unique ID `[TOPIC]-PR-[NNN]` and goes in "Open" section

## Step 4: Initialize Phase Tracking

Add to NOTES.md:
```markdown
## Current Phase

**Phase**: EXPLORE
**Workflow**: (pending assessment)
**Assessment**: (pending)
```

Add to PROGRESS.md:
```markdown
## Phase Plan

- [ ] **EXPLORE** - in_progress
- [ ] **DESIGN** - pending
```

## Step 5: Document Agent Instructions

**Session documents**: See `devsystem-core.md` sections "Document Types" and "Tracking Documents" for full list and usage.

Read the rules in the windsurf rules folder and write key instructions into NOTES.md under "IMPORTANT: Cascade Agent Instructions".