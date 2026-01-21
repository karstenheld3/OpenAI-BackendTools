---
description: Archive a completed session folder
auto_execution_mode: 1
---

# Archive Session Workflow

## Required Skills

Invoke these skills before proceeding:
- @session-management for archive conventions

Use this workflow to move a completed session folder to the archive.

## Steps

1. **Move session folder to Archive**
// turbo
   ```powershell
   Move-Item -Path "[SESSION_FOLDER]" -Destination "[SESSION_ARCHIVE_FOLDER]"
   ```
   Replace `[SESSION_FOLDER]` with actual folder name (e.g., `_2026-01-10_DontOverwriteWithEmptyValues`)

2. **Commit archive**
// turbo
   ```powershell
   git add -A && git commit -m "[type](scope): [description] - archive session"
   ```

## Example

```powershell
Move-Item -Path "_2026-01-10_DontOverwriteWithEmptyValues" -Destination "_Archive\"
git add -A && git commit -m "fix(sap-import): preserve user data during SAP import - archive session"
```
