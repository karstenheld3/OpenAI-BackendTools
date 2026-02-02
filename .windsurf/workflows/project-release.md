# Project Release Workflow

Create a dated release with comprehensive release notes.

## Prerequisites

- All work committed and pushed
- GitHub CLI (`gh`) installed and authenticated
- No uncommitted changes

## Steps

### 1. Determine Release Scope

```powershell
# Find last release tag
git tag --sort=-creatordate | Select-Object -First 1
```

Compare changes since last release:
- List commits: `git log [LAST_TAG]..HEAD --oneline`
- List changed files: `git diff --name-status [LAST_TAG]..HEAD`

### 2. Inventory Sessions

Find all session folders in `_Sessions/`:
```powershell
Get-ChildItem "_Sessions" -Directory | Where-Object { $_.Name -notlike "_Archive*" }
```

For each session, collect:
- Session name and date
- Goal (from NOTES.md header)
- Status (from PROGRESS.md - complete/in-progress)
- Artifacts: `_INFO_*.md`, `_SPEC_*.md`, `_IMPL_*.md`, `_STRUT_*.md`
- Key findings (from NOTES.md "Important Findings" section)

### 3. Generate Release Notes

Create `RELEASE_NOTES_[YYYY-MM-DD].md` using template:

```markdown
# Release Notes: [YYYY-MM-DD]

## Summary

This release covers [N] sessions from [date range], focusing on [themes].

## Sessions Overview

### [N]. [Session_Name]

**Goal**: [from NOTES.md]

**Outcome**: [summary of what was achieved]

**Artifacts:**
- `[filename]` - [description]

**Key Findings:** (if any)
- [finding 1]
- [finding 2]

---

[Repeat for each session]

## New Skills Deployed

[List any new skills added to .windsurf/skills/]

## New Workflows

[List any new workflows added to .windsurf/workflows/]

## Workspace Files

[List changes to workspace-level files: FAILS.md, !NOTES.md, etc.]

## Statistics

- **Total Sessions**: [N]
- **Total Documents Created**: [N]
- [Other relevant stats]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial release notes created
```

### 4. Commit Release Notes

```powershell
git add "RELEASE_NOTES_[YYYY-MM-DD].md"
git commit -m "docs: add release notes for [YYYY-MM-DD]"
```

### 5. Create Tag

Tag format: `YYYY-MM-DD` (e.g., `2026-01-27`)

```powershell
git tag -a "[YYYY-MM-DD]" -m "Release [YYYY-MM-DD]: [brief summary]"
git push origin "[YYYY-MM-DD]"
git push
```

### 6. User Confirmation

Present summary to user:
- Number of sessions
- Key artifacts
- Tag name

Ask: "Create GitHub release with these notes? (y/n)"

### 7. Create GitHub Release

```powershell
gh release create "[YYYY-MM-DD]" --title "Release [YYYY-MM-DD]" --notes-file "RELEASE_NOTES_[YYYY-MM-DD].md"
```

Report release URL to user.

## Example Output

```
Release created: https://github.com/[owner]/[repo]/releases/tag/2026-01-27

Sessions: 6
Artifacts: 50+ documents
Tag: 2026-01-27
```

## Notes

- Use today's date for tag unless user specifies otherwise
- Include ALL sessions since last release, not just completed ones
- Mark in-progress sessions clearly in release notes
- If `gh` not installed, provide manual release URL
