---
description: Resume a development session
auto_execution_mode: 1
---

## Required Skills

Invoke these skills before proceeding:
- @session-management for session file structure

## Step 1: Identify Session

Check if user provided a session path:
- If path exists with NOTES.md, PROGRESS.md, PROBLEMS.md: Use that session
- If no path provided: Ask user which session to resume

## Step 2: Load Context

Execute the /prime workflow but keep the answer for later.

## Step 3: Read Session Documents

Read all session documents (NOTES.md, PROGRESS.md, PROBLEMS.md, and any INFO/SPEC/IMPL/TASK files).

Restore phase state from NOTES.md "Current Phase" section.

Make sure all state progress is documented in `NOTES.md` and `PROGRESS.md` and `PROBLEMS.md`

## Step 4: Summarize and Propose
Start with single row: "Read [a] .md files ([b] priority), [c] code files ( [d] .py, [e] ...). Mode: [scenario]"

Example: "Read 5 .md files (2 priority), 12 code files (10 .py, 2 .html). Mode: SINGLE-PROJECT + SINGLE-VERSION + SESSION-BASED"

Then:
- Summarize findings and propose next steps.
- Answer with max 20 short lines of text.