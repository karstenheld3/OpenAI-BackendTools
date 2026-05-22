---
description: Resume a development session
auto_execution_mode: 1
---

# Load Session Workflow

## Required Skills

- @skills:session-management for session file structure

## MUST-NOT-FORGET

- Run `/prime` workflow BEFORE reading session documents
- `/prime` loads FAILS.md, ID-REGISTRY.md, !NOTES.md - critical workspace context

## Step 1: Identify Session

Check if user provided a session path:
- If path provided with NOTES.md, PROGRESS.md, PROBLEMS.md: Use that session
- If no path provided: Find most recently modified session folder:

```powershell
Get-ChildItem -Path "[DEFAULT_SESSIONS_FOLDER]" -Directory -Filter "_*" | Where-Object { Test-Path "$($_.FullName)\NOTES.md" } | Sort-Object { (Get-ChildItem $_.FullName -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1).LastWriteTime } -Descending | Select-Object -First 1 -ExpandProperty FullName
```

**Topic Folder Detection:** Run @skills:session-management **Topic Folder Detection** procedure. If target matches `T##_*`, load parent session context before proceeding.

## Step 2: Load Context

Run `/prime` workflow now.

## Step 3: Read Session Documents

Read all session documents (NOTES.md, PROGRESS.md, PROBLEMS.md, and any INFO/SPEC/IMPL/TASK files).

Restore phase state from NOTES.md "Current Phase" section.

Make sure all state progress is documented in `NOTES.md` and `PROGRESS.md` and `PROBLEMS.md`

## Step 4: Summarize and Propose
Start with single row: "Read [a] .md files ([b] priority), [c] code files ( [d] .py, [e] ...). Mode: [scenario]"

Example: "Read 5 .md files (2 priority), 12 code files (10 .py, 2 .html). Mode: SINGLE-PROJECT + SINGLE-VERSION + SESSION-MODE"

Then:
- Summarize findings and propose next steps.
- Answer with max 20 short lines of text.

## Step 5: Verify MUST-NOT-FORGET

Review each MNF item above and confirm compliance.