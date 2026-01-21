---
description: Close a development session, sync findings, and archive
auto_execution_mode: 1
---

# Close Session Workflow

## Required Skills

- @session-management for session lifecycle
- @git-conventions for final commit

Use this workflow when a session is complete. Prepares for archiving but does NOT archive.

## Steps

1. **Sync problems to project !PROBLEMS.md**
   - Read session PROBLEMS.md
   - For each problem:
     - RESOLVED: Mark in `!PROBLEMS.md` as FIXED with date
     - OPEN/DEFERRED: Add to `!PROBLEMS.md`

2. **Sync FAILS to project FAILS.md (MEDIUM and HIGH only)**
   - Read session FAILS.md
   - For each [MEDIUM] or [HIGH] entry:
     - Add to workspace FAILS.md if not already present
     - Skip [LOW] severity entries (session-specific)

3. **Sync LEARNINGS to project (MEDIUM and HIGH only)**
   - Read session LEARNINGS.md
   - For learnings linked to [MEDIUM] or [HIGH] fails:
     - Add prevention rules to `!NOTES.md`
     - Or create workspace-level LEARNINGS.md if patterns are reusable

4. **Update session PROGRESS.md**
   - Keep To Do list intact - do NOT delete
   - Mark completed items as done: `- [x]`
   - Ensure completed tasks in "Done" section

5. **Sync findings to project !NOTES.md**
   - Review session NOTES.md for reusable patterns
   - Add important findings: problem, solution, key facts

6. **Check for deployable artifacts**
   - List session artifacts that may need deployment:
     - `_SPEC_*.md` - Specifications (deploy to workspace root?)
     - `_IMPL_*.md` - Implementation plans
     - `_INFO_*.md` - Research documents
     - Code files created in session folder
     - Skills, workflows, rules created/modified
   - For each artifact found, ask [ACTOR]:
     - "Deploy to workspace/project?" or
     - "Keep in session archive only?"
   - Execute deployment decisions before archiving

7. **Ready for archive**
   - Verify all syncs complete
   - Verify deployment decisions executed
   - Report: "Session ready for archive. Run `/session-archive` when ready."
