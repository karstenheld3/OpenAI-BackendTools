---
description: Create conventional commits
auto_execution_mode: 1
---

# Commit Workflow

Create conventional commits for staged changes.

## Required Skills

- @git-conventions for commit message format

## Steps

1. Analyze what was done since last commit
2. If multiple activities with different files, plan multiple commits
3. Identify chronological order by file modification times
4. Separate into commits by type:
   - Research, specifications, plans (docs)
   - Implementation (feat/fix)
   - Tests (test)
   - Documentation (docs)
5. Follow @git-conventions for message format
6. Execute commits until all changes committed

## Commit Message Format

`<type>(<scope>): <description>`

Types: feat, fix, docs, refactor, test, chore, style, perf
