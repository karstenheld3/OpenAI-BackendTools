---
name: git
description: Apply when working with Git repositories, commit history, or recovering files from previous commits
---

# Git Skill

Git operations with focus on commit history navigation and file recovery.

## MUST-NOT-FORGET

- Always verify repository root before operations: `git rev-parse --show-toplevel`
- Use `--name-status` to see A/M/D (Added/Modified/Deleted) per commit
- To recover deleted file: checkout from commit BEFORE deletion (use `^` suffix)
- Reflog survives even after reset/rebase - use it for recovery

## Setup

For installation, see `SETUP.md` in this skill folder.

## Commit History Navigation

### View Recent Commits

```powershell
# Last 10 commits, one line each
git log --oneline -10

# With file changes summary
git log --oneline --name-status -10

# With date and author
git log --format="%h %ad %an: %s" --date=short -10
```

### View Files Changed in Specific Commit

```powershell
# Show files with status (A=added, M=modified, D=deleted)
git show --name-status <commit_hash>

# Just the file list
git show --name-only <commit_hash>

# Full diff
git show <commit_hash>
```

### Navigate Commits Step by Step

```powershell
# Show current HEAD
git log --oneline -1

# Show parent of HEAD
git log --oneline HEAD^ -1

# Show N commits back
git log --oneline HEAD~5 -1

# Compare two commits
git diff <commit1> <commit2> --name-status
```

### Interactive Walkback (Step Through History)

To investigate commits one-by-one, walking backwards:

```powershell
# Step 1: Start at HEAD, show what changed
git log --oneline -1
git show --name-status HEAD

# Step 2: Move back one commit, show changes
git log --oneline HEAD^ -1
git show --name-status HEAD^

# Step 3: Continue back (use ~2, ~3, etc.)
git log --oneline HEAD~2 -1
git show --name-status HEAD~2

# Pattern: HEAD~N where N = steps back from current
```

**Tip:** Your current position is always HEAD. Use `git log --oneline -1` to confirm where you are.

## File Recovery

### Find When File Was Deleted

```powershell
# List all deleted files across history
git log --diff-filter=D --summary

# Find specific file deletion
git log --diff-filter=D --summary -- "**/filename.ext"

# Find EXACTLY which commit deleted a specific file (one-liner)
git log --diff-filter=D -1 -- path/to/file.ext

# With paths
git log --diff-filter=D --name-only --format="%H %s"
```

### Find Last Commit Where File Existed

```powershell
# Shows commits that touched the file (including deletion)
git log --all -- path/to/deleted/file.ext

# The first result is the deletion commit
# Use its parent (^) to get the version before deletion
```

### Recover Deleted File

```powershell
# From commit that deleted it (^ = parent commit)
git checkout <deletion_commit>^ -- path/to/file.ext

# From known good commit
git checkout <good_commit> -- path/to/file.ext

# Alternative (Git 2.23+): git restore --source=<commit> -- path/to/file

# Using show (outputs to stdout, redirect to file)
git show <commit>:path/to/file.ext > recovered_file.ext
```

### Recover File from Reflog

```powershell
# View reflog
git reflog

# Recover from specific reflog entry
git checkout HEAD@{n} -- path/to/file.ext
```

## Guided Recovery Workflow

When user needs to recover accidentally deleted files:

### Step 1: Identify Deletion

```powershell
# Find recent deletions
git log --diff-filter=D --name-only --format="=== %H %s ===" -5
```

**Note:** If file was renamed (not deleted), use `git log --follow -- oldname` to track renames.

### Step 2: Confirm Deletion Commit

```powershell
# Show what was deleted in that commit
git show --name-status <commit_hash>
```

### Step 3: Verify File Existed Before

```powershell
# Check file in parent commit
git show <commit_hash>^:<path/to/file>
```

### Step 4: Recover

```powershell
# Restore the file
git checkout <commit_hash>^ -- path/to/file
```

### Step 5: Verify Recovery

```powershell
# Check file exists
Get-Item path/to/file

# Check status
git status
```

## Batch Operations

### List All Files Deleted in Last N Commits

```powershell
git log --diff-filter=D --name-only --format="" -n 20 | Where-Object { $_ -ne "" } | Sort-Object -Unique
```

### Recover Multiple Files from Same Commit

```powershell
# List files first
git show --name-only <commit>^

# Recover specific files
git checkout <commit>^ -- file1.ext file2.ext file3.ext

# Recover entire directory
git checkout <commit>^ -- path/to/directory/
```

## Comparing Versions

### Compare File Across Commits

```powershell
# Between two commits
git diff <commit1> <commit2> -- path/to/file

# Between commit and working directory
git diff <commit> -- path/to/file

# Between commit and staged
git diff --cached <commit> -- path/to/file
```

### Show File Content at Specific Commit

```powershell
git show <commit>:path/to/file
```

## Undo Operations

### Undo Last Commit (Keep Changes)

```powershell
git reset --soft HEAD^
```

### Undo Last Commit (Discard Changes)

```powershell
git reset --hard HEAD^
```

### Restore File to Last Committed Version

```powershell
git checkout HEAD -- path/to/file
```

### Unstage File

```powershell
git reset HEAD -- path/to/file
```

## Status and Inspection

### Repository Status

```powershell
git status
git status --short
```

### Show Staged Changes

```powershell
git diff --cached
git diff --cached --name-status
```

### Show Unstaged Changes

```powershell
git diff
git diff --name-status
```

## Common Patterns

### Investigate Accidental Deletion

```powershell
# 1. Find what was deleted recently
git log --diff-filter=D --name-only -5

# 2. Identify the commit
git show <commit> --name-status

# 3. Recover
git checkout <commit>^ -- <file>
```

### Recover Workflow File Deleted by Commit Workflow

When `/commit` accidentally deletes a file:

```powershell
# 1. Check last few commits for deletions
git log --diff-filter=D --name-status -3

# 2. Find the workflow file
git log --diff-filter=D -- "**/*.md" --name-only -5

# 3. Recover from parent of deletion commit
git checkout <commit>^ -- .windsurf/workflows/filename.md
```

### Compare What Changed Between Sessions

```powershell
# Find commits from today
git log --since="today" --oneline

# Compare start to end
git diff <first_commit> <last_commit> --name-status
```
