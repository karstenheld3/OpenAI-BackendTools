---
description: Fix bugs - record, investigate, create [BUG_FOLDER], test, commit, update docs (renamed from fix.md)
---

# Bugfix Workflow

Complete bug-fixing workflow from problem discovery to verified fix and documentation.

## Required Skills

- @write-documents for INFO, STRUT, and FIXES templates
- @coding-conventions for code changes
- @skills:session-management for session setup (PROJECT-MODE only)

## MUST-NOT-FORGET

- Determine context FIRST: SESSION-MODE or PROJECT-MODE
- Always create `[BUG_FOLDER]` (both contexts)
- Impact assessment BEFORE implementing fix
- Test impacted functionality BEFORE committing
- Run `/learn` after fix is verified (optional but recommended)

## Trigger

- `/bugfix [problem-description]` - Start with known problem
- `/bugfix` - Discovery mode (analyze context for issues)

## Quick Reference

SESSION-MODE (bug found during active session):
- Folder: `[SESSION_FOLDER]/`
- Bug ID: `[TOPIC]-BG-NNNN` (4-digit)
- Bug Folder: `[SESSION_FOLDER]/[TOPIC]-BG-NNNN_IssueDescription/`
- Docs: SPEC, IMPL, TEST
- Commit: `fix([TOPIC]-BG-NNNN): description`

PROJECT-MODE (bug found after session closed):
- Folder: `[BUGFIXES_FOLDER]/` = `[DEFAULT_SESSIONS_FOLDER]/_BugFixes/`
- Bug ID: `GLOB-BG-NNNN` (4-digit, uses GLOB prefix)
- Bug Folder: `[BUGFIXES_FOLDER]/GLOB-BG-NNNN_IssueDescription/`
- Docs: SPEC, IMPL, TEST + `*_FIXES.md`
- Commit: `fix(GLOB-BG-NNNN): description`

## Step 1: Determine Context

CRITICAL: The entire workflow depends on this determination.

### SESSION-MODE

Condition: Currently working in an active session (`[SESSION_FOLDER]` exists)

Characteristics:
- Bug found WHILE WORKING on a task
- Problem may or may not be confirmed as bug yet
- Fix happens in current session folder
- Uses BG (Bug) tracking ID (`[TOPIC]-BG-NNNN`)

Folder structure:
```
[SESSION_FOLDER]/
├── NOTES.md, PROBLEMS.md, PROGRESS.md
└── [TOPIC]-BG-NNNN_IssueDescription/    <- [BUG_FOLDER]
    ├── PROBLEMS.md                      <- Full detail
    ├── _INFO_*.md, __STRUT_*.md
    ├── backup/, poc/, test/
```

Documentation on completion:
- Update SPEC, IMPL, TEST docs only
- NO `*_FIXES.md` file created

### PROJECT-MODE

Condition: No active session OR bug found after session closed/archived

Characteristics:
- Bug found AFTER implementation is done
- Confirmed defect in existing code
- Fix happens in persistent `_BugFixes` session
- Uses BG (Bug) tracking ID (`GLOB-BG-NNNN`, cross-cutting)

Folder structure:
```
[BUGFIXES_FOLDER]/              <- Permanent session (never archived)
├── NOTES.md, PROBLEMS.md, PROGRESS.md
└── GLOB-BG-NNNN_IssueDescription/      <- [BUG_FOLDER] (uses GLOB prefix)
    ├── PROBLEMS.md                      <- Full detail
    ├── _INFO_*.md, __STRUT_*.md
    ├── backup/, poc/, test/
```

Documentation on completion:
- Update SPEC, IMPL, TEST docs
- ALSO create/update `*_FIXES.md` next to component's IMPL or SPEC doc

## Step 2: Ensure _BugFixes Session Exists (PROJECT-MODE only)

If PROJECT-MODE:

1. Read `!NOTES.md` to get `[BUGFIXES_FOLDER]` path
2. Check if `[BUGFIXES_FOLDER]` exists
3. If NOT exists, create `[BUGFIXES_FOLDER]` with:
   - `NOTES.md` (minimal session notes)
   - `PROBLEMS.md` (empty with header)
   - `PROGRESS.md` (empty with header)
   - `FAILS.md` (empty with header)
4. This session is PERMANENT - never archived

If SESSION-MODE: Skip this step, use current `[SESSION_FOLDER]`

## Step 3: Record Problem

If no description provided (discovery mode):
- Analyze recent conversation for error messages
- Check test output for failures
- Look for "doesn't work", "fails", "broken" phrases
- If nothing found, exit with "No issues detected"

Record in PROBLEMS.md (no subfolder for problems):

- SESSION-MODE: `[SESSION_FOLDER]/PROBLEMS.md`, ID format `[SESSION_TOPIC]-PR-NNNN`
- PROJECT-MODE: `[BUGFIXES_FOLDER]/PROBLEMS.md`, ID format `GLOB-PR-NNNN`

Entry format:
```markdown
### [ID] ShortDescription

**Status**: Open
**Reported**: [timestamp]

**Verbatim prompt**:
````
[exact user message or error]
````

**Initial assessment**: [brief description]
```

## Step 4: Analyze and Create [BUG_FOLDER]

1. Make several assumptions about possible causes
2. Search in code, verify each assumption
3. Disambiguate and narrow down the problem

A problem is confirmed as a **bug** when it's a deviation from desired behavior that prevents the goal from being reached. Can be:
- A flaw in the code
- A flawed design decision in the IMPL
- An incorrect assessment of actual behavior of libraries, frameworks, or backends
- A flawed assumption or design decision in the SPEC (rare)

Create [BUG_FOLDER] (only when problem confirmed as bug):

- SESSION-MODE: `[SESSION_FOLDER]/[TOPIC]-BG-NNNN_IssueDescription/`
  - Get next BG number from `[SESSION_FOLDER]/NOTES.md` "Bug List" section (count existing entries + 1)
- PROJECT-MODE: `[BUGFIXES_FOLDER]/GLOB-BG-NNNN_IssueDescription/`
  - Get next BG number from `[BUGFIXES_FOLDER]/NOTES.md` (single source of truth)

Inside [BUG_FOLDER], create:
- `PROBLEMS.md` - Full detail problem tracking

Update parent PROBLEMS.md PR entry with note: "→ Now tracked as [TOPIC]-BG-NNNN" (or "→ Now tracked as GLOB-BG-NNNN" for PROJECT-MODE).

## Step 5: Reproduce Bug

- Use `.tmp` scripts or Playwright MCP
- Leave artifacts ONLY in `[BUG_FOLDER]`
- Verify bug exists on current code before any changes
- If cannot reproduce after 3 attempts → [CONSULT] with user

## Step 6: Deep Analysis

Run `/write-info` to create `_INFO_*.md` in `[BUG_FOLDER]`:
- Document all evidence and observations
- Record what was tried and what failed
- Identify root cause hypothesis

## Step 7: Develop Plan

Run `/write-strut` to create fix plan:
- Step-by-step plan with verifiable phases
- Testing actions for each testable change
- Backup affected files to `[BUG_FOLDER]/backup/`
- Define commit strategy (NEVER commit untested code)

Planning principles:
- Verify assumptions before acting
- Medium complexity ideas: test in POCs first
- Ask: "How easy is it to test this?" Choose easiest first.
- Avoid blaming hardware/infrastructure without evidence
- Add detailed logging BEFORE jumping to conclusions

## Step 8: Impact Assessment

MANDATORY before implementing:

1. List all code paths that interact with the fix location
2. Identify functionality that depends on fixed code:
   - Callers and consumers
   - UI components
   - Other endpoints
   - Test files
3. Document impacted areas in `[BUG_FOLDER]/PROBLEMS.md`
4. Create test cases for each impacted area BEFORE implementing fix

## Step 9: Execute Plan

Run `/implement` principles:
- Execute step by step autonomously
- Small cycles: implement → test → fix → green → next
- For complex plans: use `/write-tasks-plan` and `/write-test-plan`
- Update STRUT and tracking documents frequently
- Track artifacts created during testing (must delete after fix)

## Step 10: Final Verification and Documentation

### 10.1 Verify Fix

- Do BEFORE/AFTER comparison using `[BUG_FOLDER]/backup/`
- Run all tests for impacted functionality
- Only proceed if ALL tests pass

### 10.2 Update Documentation

ALWAYS (both contexts):
- Update SPEC docs to cover the newly discovered scenario
- Update IMPL docs with implementation changes
- Update TEST docs with new test cases

PROJECT-MODE only:
- Create/update `*_FIXES.md` next to component docs:
  1. Search for `*_IMPL_*.md` for the component → add/update `*_IMPL_*_FIXES.md`
  2. If no IMPL doc → search for `*_SPEC_*.md` → add/update `*_SPEC_*_FIXES.md`

### 10.3 Commit

Run `/commit` with format: `fix(GLOB-BG-NNNN): description` (PROJECT-MODE) or `fix([TOPIC]-BG-NNNN): description` (SESSION-MODE)

### 10.4 Mark Resolved

Update PROBLEMS.md entry:
```markdown
**Status**: Resolved
**Resolved**: [timestamp]
**Solution**: [brief description]
```

## Step 11: Completion Checklist

- [ ] Context determined (SESSION-MODE or PROJECT-MODE)
- [ ] `[BUG_FOLDER]` created with all artifacts
- [ ] Impact assessment documented
- [ ] All impacted functionality tested and passing
- [ ] SPEC/IMPL/TEST docs updated with new scenario
- [ ] `*_FIXES.md` created/updated (PROJECT-MODE only)
- [ ] PROBLEMS.md entry marked Resolved
- [ ] Clean commit with proper message format

## Post-Fix

Run `/learn` to reflect on mistakes and extract lessons from this fix.

## _FIXES.md Format

Created for PROJECT-MODE only. One file per component.

```markdown
### GLOB-BG-NNNN IssueDescription

**Problem**: Single sentence describing the bug
**Solution**: Single sentence describing the fix

**Changed or added files**:
- `path/to/file.py`      - What was changed
- `path/to/poc_file.py`  - POC file that was used to prove solution
- `path/to/test_file.py` - Test file that was used to test bugfix
- `path/to/spec.md`      - Added scenario for edge case X
- `path/to/impl.md`      - Updated step Y to handle Z
```
