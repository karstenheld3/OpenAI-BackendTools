---
name: github
description: Apply when working with GitHub repositories, issues, PRs, or authentication
---

# GitHub CLI Guide

Rules and usage for GitHub CLI in `[WORKSPACE_FOLDER]/.tools/gh/`.

## MUST-NOT-FORGET

- Authenticate before first use: `gh auth login`
- Use `--repo` flag when not in a git directory
- Check auth status if commands fail: `gh auth status`

## Authentication

### Login to GitHub
```powershell
& ".tools/gh/bin/gh.exe" auth login
```

### Check authentication status
```powershell
& ".tools/gh/bin/gh.exe" auth status
```

### Setup git credential helper
```powershell
& ".tools/gh/bin/gh.exe" auth setup-git
```

## Repository Operations

### Create new repository
```powershell
# Public repo
& ".tools/gh/bin/gh.exe" repo create <name> --public --source=. --remote=origin --push

# Private repo
& ".tools/gh/bin/gh.exe" repo create <name> --private --source=. --remote=origin --push

# From current directory with defaults
& ".tools/gh/bin/gh.exe" repo create --source=. --push
```

### Clone repository
```powershell
& ".tools/gh/bin/gh.exe" repo clone <owner>/<repo>
```

### View repository info
```powershell
& ".tools/gh/bin/gh.exe" repo view
& ".tools/gh/bin/gh.exe" repo view <owner>/<repo>
```

### List your repositories
```powershell
& ".tools/gh/bin/gh.exe" repo list
& ".tools/gh/bin/gh.exe" repo list --limit 50
```

## Issues

### Create issue
```powershell
& ".tools/gh/bin/gh.exe" issue create --title "Bug: something broke" --body "Description"
```

### List issues
```powershell
& ".tools/gh/bin/gh.exe" issue list
& ".tools/gh/bin/gh.exe" issue list --state open
& ".tools/gh/bin/gh.exe" issue list --label "bug"
```

### View issue
```powershell
& ".tools/gh/bin/gh.exe" issue view <number>
```

### Close issue
```powershell
& ".tools/gh/bin/gh.exe" issue close <number>
```

## Pull Requests

### Create PR
```powershell
& ".tools/gh/bin/gh.exe" pr create --title "Add feature" --body "Description"
& ".tools/gh/bin/gh.exe" pr create --fill  # Use commit info
```

### List PRs
```powershell
& ".tools/gh/bin/gh.exe" pr list
& ".tools/gh/bin/gh.exe" pr list --state open
```

### View PR
```powershell
& ".tools/gh/bin/gh.exe" pr view <number>
& ".tools/gh/bin/gh.exe" pr view --web  # Open in browser
```

### Merge PR
```powershell
& ".tools/gh/bin/gh.exe" pr merge <number>
& ".tools/gh/bin/gh.exe" pr merge <number> --squash
```

### Checkout PR locally
```powershell
& ".tools/gh/bin/gh.exe" pr checkout <number>
```

## Releases

### Create release
```powershell
& ".tools/gh/bin/gh.exe" release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"
```

### List releases
```powershell
& ".tools/gh/bin/gh.exe" release list
```

### Download release assets
```powershell
& ".tools/gh/bin/gh.exe" release download v1.0.0
```

## Gists

### Create gist
```powershell
& ".tools/gh/bin/gh.exe" gist create file.txt --public
& ".tools/gh/bin/gh.exe" gist create file1.txt file2.txt --desc "My gist"
```

### List gists
```powershell
& ".tools/gh/bin/gh.exe" gist list
```

## Workflow / Actions

### List workflows
```powershell
& ".tools/gh/bin/gh.exe" workflow list
```

### View workflow runs
```powershell
& ".tools/gh/bin/gh.exe" run list
& ".tools/gh/bin/gh.exe" run view <run-id>
```

### Trigger workflow
```powershell
& ".tools/gh/bin/gh.exe" workflow run <workflow-name>
```

## Common Patterns

### Create repo and push existing project
```powershell
& ".tools/gh/bin/gh.exe" repo create <name> --private --source=. --remote=origin --push
```

### Fork and clone
```powershell
& ".tools/gh/bin/gh.exe" repo fork <owner>/<repo> --clone
```

### Open repo in browser
```powershell
& ".tools/gh/bin/gh.exe" repo view --web
```

## Setup

For initial installation, see `SETUP.md` in this skill folder.

**Tool location:** `.tools/gh/bin/gh.exe`
