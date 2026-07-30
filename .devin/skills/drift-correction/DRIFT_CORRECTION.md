# Drift Correction Knowledge

Knowledge source for the `/drift-correct` workflow. Contains gap closure strategies, verification patterns, and correction boundaries.

## Correction Principles

1. **Trust the detection file** - `__DRIFT_[TOPIC].md` is the contract. Do not re-assess items. If it says FAIL, fix it.
2. **Minimum viable fix** - close the gap with the smallest change that makes the item PASS. Do not over-engineer.
3. **Verify after each fix** - confirm the item now passes before moving on. No batch-fixing without verification.
4. **Preserve existing work** - corrections must not break things that already PASS. If a fix risks regression, note it.
5. **MISSED items are informational** - they cannot be retroactively fixed. Do not attempt. Record for future prevention.

## Gap Closure Strategies

### Category 1 (Output Structure) - Common Fixes

- **Missing file/folder** → create it with expected content
- **Wrong file name** → rename (check for references)
- **Missing section/header** → add to document
- **Placeholder content** → replace with actual content
- **Missing cross-references/IDs** → add references
- **Truncated content** → complete it

### Category 2 (Process Discipline) - Common Fixes

- **Tracking files not updated** → update NOTES.md, PROGRESS.md, PROBLEMS.md now
- **`/verify` not run** → run `/verify` now
- **Commit not created** → create commit for completed work
- **Gate condition not checked** → check it now, document result
- **Test not executed** → run the test now

### Category 2 - NOT Fixable (mark BLOCKED)

- **Step sequence violated** → cannot undo (mark MISSED if not already)
- **Processing depth was shallow** → might require full redo (mark BLOCKED with reason)
- **Backup not created before modify** → cannot retroactively create (MISSED)

## Verification After Fix

For each corrected item, verify by:

1. **Output Structure items** - check file/folder exists, content matches expectation
2. **Process Discipline items** - check artifact exists (commit, tracking file update, test result)
3. **Cross-check** - does the fix maintain consistency with other PASS items?

## When to Mark BLOCKED

An item is BLOCKED (not fixable in current context) when:

- Requires user decision (architectural choice, priority call)
- Depends on external resource (API access, credentials, third-party service)
- Would require full re-execution (shallow processing cannot be deepened without redo)
- Conflicts with another PASS item (fixing one would break another)

Always provide a specific reason. "Cannot fix" is not acceptable.

## Correction Boundaries

- Do NOT modify the DoD criteria themselves (only status changes)
- Do NOT add new criteria (detection is complete)
- Do NOT change Priority or Category assignments
- Do NOT touch MISSED items (informational only)
- Do NOT modify FAILS.md or LEARNINGS.md (user-triggered only)
- DO update tracking files (PROGRESS.md, NOTES.md) after significant corrections
- DO create commits for completed corrections if git workflow is active
