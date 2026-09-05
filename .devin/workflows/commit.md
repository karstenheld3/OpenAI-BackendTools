---
description: Create conventional commits
auto_execution_mode: 3
---

# Commit Workflow

Create conventional commits for staged changes.

## Required Skills

- @skills:git-conventions for commit message format

## MUST-NOT-FORGET

- **Suppress git noise**: Use `2>$null` on `git add` (CRLF warnings go to stderr) and `-q` on `git commit` (suppresses rename/summary output). Without this, large repos produce hundreds of lines that cause Cascade blocking commands to hang or time out.
- **Use non-blocking execution** (`Blocking: false`, `WaitMsBeforeAsync: 5000`) for `git add -A` when many files are affected (e.g., version bumps, bulk renames). Check completion with `command_status`.

## Steps

1. Analyze what was done since last commit
2. If multiple activities with different files, plan multiple commits
3. Identify chronological order by file modification times
4. Separate into commits by type:
   - Research, specifications, plans (docs)
   - Implementation (feat/fix)
   - Tests (test)
   - Documentation (docs)
5. Follow @skills:git-conventions for message format
6. Execute commits until all changes committed

## Execution Rules

**Stage files**:
```powershell
git add -A 2>$null
# Or for specific files:
git add <files> 2>$null
```

**Commit**:
```powershell
git commit -q -m "<type>(<scope>): <description>"
```

**For bulk operations** (version bumps, large renames with 50+ files):
- Run `git add -A 2>$null` as non-blocking with `WaitMsBeforeAsync: 5000`
- Poll with `command_status` if not done within wait period
- Then run `git commit -q -m "..."` as blocking (commit itself is fast after staging)

## Commit Message Format

`<type>(<scope>): <description>`

Types: feat, fix, docs, refactor, test, chore, style, perf

## Multi-Repo Commit (WORKSPACE Mode)

Detect by: WORKSPACE mode (main.code-workspace file exists in workspace root).

When WORKSPACE mode is detected, commit changes across multiple git repos:

1. Detect changes across all git repos in workspace
2. Commit order (product-first):
   1. Product repo first (primary deliverable)
   2. Dev repo second (documentation of product changes)
   3. All other workspace repos (Company, linked repos)
3. For each repo with changes:
   - Detect uncommitted changes
   - Analyze by type (feat, fix, docs, test, chore)
   - Use `git -C [repo_path]` for all git operations (explicit scoping)
   - Detect and use per-repo git config (user.name, user.email) - do not assume workspace-wide git identity
   - Create conventional commits per type
4. If a repo commit fails:
   - Report failure with error message
   - Continue with remaining repos
   - Summarize partial success at end
   - Do not roll back already-committed repos
5. Skip repos with no changes silently
6. Report committed changes per repo at end

Rationale: Product repo changes are the primary deliverable. Dev repo changes are secondary. Temporary inconsistency (product committed, dev not) is acceptable because dev repo content is not a runtime dependency.

In SINGLE-PROJECT and MONOREPO modes: existing single-repo commit behavior is unchanged.
