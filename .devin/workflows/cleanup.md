---
description: Delete temporary files and artifacts left by workflows and skills
auto_execution_mode: 3
---

# Cleanup Workflow

Delete temporary files, build artifacts, and workflow leftovers from workspace and tools folders.

**Goal**: Clean workspace with all temporary and intermediate files removed

**Why**: Workflows and skills leave behind temp scripts, Python cache, versioned backups, and MCP config backups that accumulate over time

Scope: File deletion only. Does NOT uninstall tools, remove sessions, or modify source code.

## MUST-NOT-FORGET

- **When in doubt, infer narrowest scope** - never block on scope questions
- Scan BEFORE deleting - always show preview of what will be removed
- NEVER delete `../.tools/` output folders (see Protected Locations)
- NEVER delete `/bugfix` `backup/` folders or `/go` backups/zips
- **All categories auto-delete after preview** - no confirmation needed
- User can run `/commit` before `/cleanup` if backups are needed

## Trigger

- `/cleanup` - infer scope from conversation context (narrowest scope wins), then scan
- `/cleanup [path]` - scope to specified path directly

## GLOBAL-RULES

Apply to all cleanup runs regardless of scope.

1. Scan all target locations and collect file list BEFORE deleting anything
2. Group findings by category in preview
3. Show full paths in preview - never abbreviate or truncate
4. Auto-delete all categories after preview (see Auto-Delete Categories)
5. Report deletion results with counts per category

## Auto-Delete Categories

All categories auto-delete after preview. No confirmation needed. User can run `/commit` before `/cleanup` if backups are needed.

- Category 1: Agent temp files (`.tmp_*`, `*.tmp`) - single-run scripts, always disposable
- Category 2: Python build artifacts (`__pycache__/`, `*.pyc`) - regenerated automatically
- Category 3: Improve workflow backups (`_vN.*`) - safety copies after improvement accepted
- Category 4: MCP config backups - superseded config snapshots
- Category 5: Critique review files (`*_REVIEW.md`) - findings should be addressed before cleanup
- Category 6: Workflow scaffolding (`__*.md`, legacy `STRUT_*`) - consumed process artifacts
- INFO marker stripping (`[VERIFIED]` labels) - in-place text modification

**Execution flow:**
1. Scan all categories and show preview
2. Delete all categories immediately (no confirmation needed)
3. Report results

## Post-Workflow Cleanup Trigger

Workflows that create disposable artifacts SHOULD self-clean on successful completion. When a workflow completes successfully, it should delete its own artifacts from the working directory:

- `/improve` → delete `_vN.*` backups of the improved file
- `/drift-detect` → (keep `__DRIFT_*` until `/drift-correct` runs)
- `/drift-correct` → delete `__DRIFT_*` file after all gaps closed
- `/deep-research` → delete `__STRUT_*`, `__TASKS_*`, `__TEMPLATE_*` after research complete
- `/go` → delete `__TASKS_*` after goal reached

If the parent workflow forgets, `/cleanup` catches them. But the goal is: **artifacts should not survive beyond their parent workflow's completion**.

# CONTEXT-SPECIFIC

Detection: determine applicable contexts from scope. Multiple contexts may apply in a single run.

## File Cleanup

**Applies**: Always (every `/cleanup` run)

Delete files and directories matching these patterns:

### 1. Agent Temp Files [AUTO-DELETE]

- **Pattern**: `.tmp_*` files, `*.tmp` files
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[DEFAULT_SESSIONS_FOLDER]` recursive
- **Source**: Agent scripts, `/test`, `/implement`, `/go`, `/improve` STRUT plans, youtube-downloader metadata
- **Note**: `.tmp_*` files are dotfiles - invisible to `fd`/`find_by_name` by default. Always use PowerShell `Get-ChildItem -Force` or `fd --hidden` to scan for them.

### 2. Python Build Artifacts [AUTO-DELETE]

- **Pattern**: `__pycache__/` directories, `*.pyc` files, `.pytest_cache/`, `.mypy_cache/`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[DEVSYSTEM_FOLDER]` recursive, `[AGENT_FOLDER]` recursive
- **Source**: Python script execution

### 3. Improve Workflow Artifacts [AUTO-DELETE]

- **Pattern**: `*_vN.*` versioned backups (filename ending in `_v` followed by digits before extension), `*_DEFERRED_IMPROVEMENTS.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, excluding `_Archive/` and `_OldDevSystemVersions/`
- **Source**: `/improve` workflow versioned backups and deferred improvement logs

### 4. MCP Config Backups [AUTO-DELETE]

- **Pattern**: `mcp_config.json._beforeRemoving*`, `mcp_config.json._backup_*`
- **Location**: MCP config directory (resolve from Windsurf/Codeium config path)
- **Source**: MCP server install/uninstall scripts (ms-playwright-mcp, playwriter-mcp)

### 5. Critique Review Files [AUTO-DELETE]

- **Pattern**: `*_REVIEW.md`, `_PROBLEMS_REVIEW.md`
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_Archive/` and `_OldDevSystemVersions/`
- **Source**: `/critique` workflow creates these per review run. Intended to be discarded after findings are addressed.

### 6. Workflow Scaffolding [AUTO-DELETE]

- **Pattern**: `__*.md` files (double underscore prefix). Also legacy patterns: `STRUT_*.md` (not `STRUT_TEMPLATE.md`), `_TASKS_*.md` (files auto-created by `/go` before convention change)
- **Locations**: `[WORKSPACE_FOLDER]` recursive, `[SESSION_FOLDER]` recursive, excluding `_Archive/`, `_OldDevSystemVersions/`, and skill folders
- **Source**: `/deep-research` (STRUTs, TASKS, templates), `/go` (TASKS), `/bugfix` (STRUTs). These are process-tracking files auto-created by workflows. User-invoked outputs (`TASKS_[TOPIC].md` from `/write-tasks-plan`, `STRUT_[TOPIC].md` from `/write-strut`) are deliverables and MUST NOT be matched.
- **Transition note**: Legacy patterns (`STRUT_*.md` without `__`, `_TASKS_*.md`) exist in older sessions. Match both old and new conventions. Exclude `STRUT_TEMPLATE.md` and `TASKS_TEMPLATE.md` (skill resources).

## INFO Document Cleanup

**Applies**: When `_INFO_*.md` files exist in scope (excluding `_Archive/` and `_OldDevSystemVersions/`)

Strip verification markers in-place (text modification, not file deletion):

- **Pattern**: `[VERIFIED]` labels, `VERIFIED, ` prefixes
- **Source**: `/research`, `/write-info`, `/verify` workflows add these during authoring. After content is finalized, markers are noise.

## No Context Match

If scope contains no matching patterns and no INFO documents:
- Report "Workspace is clean - nothing to delete" and exit

## Protected Locations (NEVER Delete)

These folders and their contents are EXCLUDED from all cleanup operations:

- `[WORKSPACE_FOLDER]/../.tools/_pdf_to_jpg_converted/` - PDF conversion output
- `[WORKSPACE_FOLDER]/../.tools/_pdf_output/` - Compressed PDF output
- `[WORKSPACE_FOLDER]/../.tools/_screenshots/` - Desktop screenshots
- `[WORKSPACE_FOLDER]/../.tools/_web_screenshots/` - Web page screenshots
- `[WORKSPACE_FOLDER]/../.tools/_image_to_markdown/` - Transcription intermediates
- `[WORKSPACE_FOLDER]/../.tools/_installer/` - Downloaded tool installers
- `*/backup/` inside `_BugFixes/` session folders - `/bugfix` recovery data
- Any `.zip` or backup created by `/go` workflow
- `T##_*/` topic folders inside sessions - these are session subfolders, not temp artifacts

# EXECUTION

## Step 1: Determine Scope and Context

Read NOTES.md to resolve `[DEFAULT_SESSIONS_FOLDER]` and `[DEVSYSTEM_FOLDER]`.

**Scope resolution** (MANDATORY - resolve scope before scanning):

Six cleanup scopes exist, from narrowest to widest:

1. **Markers** - strip labels within document content (e.g., `[VERIFIED]`, `[IMPROVED]` from INFO docs)
2. **Document** - artifacts of a single document (its `_vN` backups, related temp files)
3. **Workflow/Skill** - artifacts from a specific workflow or skill execution (e.g., all `/improve` backups from one run)
4. **Folder** - everything in a specific directory matching cleanup patterns (e.g., a working subfolder in a session)
5. **Session** - everything in `[SESSION_FOLDER]` matching cleanup patterns
6. **Workspace** - everything in `[WORKSPACE_FOLDER]` and all known locations

**Resolution rules (narrowest scope wins):**
- **Narrowest scope principle**: Always infer the NARROWEST scope that covers the user's working context. Never broaden beyond what the conversation context requires.
- If all recent work is within a session subfolder (e.g., `Faro-Autokauf/`): scope = **Folder** (that subfolder), NOT Session
- If path arg provided: infer scope from path type (file → document, directory → folder/session)
- If conversation just finished a `/critique` or `/improve` run: suggest workflow scope
- If conversation spans multiple session subfolders or session root: scope = **Session**
- If ambiguous: infer narrowest scope from conversation context. Default to **Folder** (current working directory) if no context available
- Do NOT ask questions about scope, files, or folders - infer and scan

**After scope is resolved, scan immediately:**
- **Markers** → all INFO docs in scope
- **Document** → infer from conversation or current file, scan its directory
- **Workflow/Skill** → infer from conversation context, scan for its artifacts
- **Folder** → use provided path or infer from conversation context
- **Session** → scan `[SESSION_FOLDER]`
- **Workspace** → scan `[WORKSPACE_FOLDER]` and all known locations

Detect applicable contexts:
- File Cleanup: always active
- INFO Document Cleanup: active if `_INFO_*.md` files exist in scope

## Step 2: Scan

Scan per active context. Collect full paths.

**File Cleanup scan:**

```powershell
# 1. Agent temp files (dotfiles: -Force required)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Force | Where-Object { $_.Name -like '.tmp_*' -or $_.Name -like '*.tmp' }

# 2. Python artifacts
Get-ChildItem -Path "[SCOPE]" -Recurse -Directory | Where-Object { $_.Name -in @('__pycache__', '.pytest_cache', '.mypy_cache') }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*.pyc"

# 3. Improve artifacts (_vN backups: filename_vN.ext where N is one or more digits)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.BaseName -match '_v\d+$' -and $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*_DEFERRED_IMPROVEMENTS.md" | Where-Object { $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }

# 4. MCP config backups (resolve MCP config directory first)
Get-ChildItem -Path "[MCP_CONFIG_DIR]" -File | Where-Object { $_.Name -match '^mcp_config\.json\._' }

# 5. Critique review files
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "*_REVIEW.md" | Where-Object { $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' }

# 6. Workflow scaffolding (__ prefix + legacy patterns)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "__*.md" | Where-Object { $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions|skills' }
# Legacy: standalone STRUT files (not STRUT_TEMPLATE.md, not in skill folders)
Get-ChildItem -Path "[SCOPE]" -Recurse -File | Where-Object { $_.Name -match '^STRUT_' -and $_.Name -ne 'STRUT_TEMPLATE.md' -and $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions|skills' }
```

**INFO Document Cleanup scan:**

```powershell
# 7. INFO verification markers (count files and occurrences)
Get-ChildItem -Path "[SCOPE]" -Recurse -File -Filter "_INFO_*.md" | Where-Object {
    $_.DirectoryName -notmatch '_Archive|_OldDevSystemVersions' -and
    (Select-String -Path $_.FullName -Pattern '\[VERIFIED\]|VERIFIED, ' -Quiet)
}
```

Filter out protected locations from results.

## Step 3: Preview

Display grouped results in chat:

```
Cleanup Preview
===============

Agent Temp Files (N files):
  [full path 1]
  [full path 2]

Python Build Artifacts (N items):
  [full path 1]
  [full path 2]

Improve Workflow Artifacts (N files):
  [full path 1] (backup _v0)
  [full path 2] (deferred)

MCP Config Backups (N files):
  [full path 1]

Critique Review Files (N files):
  [full path 1]
  [full path 2]

Workflow Scaffolding (N files):
  [full path 1] (__STRUT_*)
  [full path 2] (__TASKS_*)

INFO Verification Markers (N files to modify):
  [full path 1] (M occurrences)
  [full path 2] (M occurrences)

Total: N items to delete, N files to modify
```

If no items found: report "Workspace is clean - nothing to delete" and exit.

## Step 4: Execute

Delete all found items immediately after preview:
- Files: `Remove-Item -Force -Confirm:$false`
- Directories (`__pycache__/`, `.pytest_cache/`, `.mypy_cache/`): `Remove-Item -Recurse -Force -Confirm:$false`
- INFO markers: strip `[VERIFIED]` and `VERIFIED, ` via text replacement

```powershell
# Strip verification markers from INFO documents
$content = Get-Content -Path $file -Raw -Encoding UTF8
$content = $content -replace ' \[VERIFIED\]', ''
$content = $content -replace 'VERIFIED, ', ''
Set-Content -Path $file -Value $content -Encoding UTF8 -NoNewline
```

## Step 5: Report

```
Cleanup Complete
================

Deleted:
  Agent Temp Files: N files
  Python Build Artifacts: N items
  Improve Workflow Artifacts: N files
  MCP Config Backups: N files
  Critique Review Files: N files
  Workflow Scaffolding: N files
  INFO Markers Stripped: N files

Total: N items deleted, N files modified
Errors: [count and paths if any]
```

# FINALIZATION

## Quality Gate

- [ ] Scope inferred as narrowest that covers working context
- [ ] All target locations scanned before any deletion
- [ ] Protected locations excluded from results
- [ ] Preview shown in chat with full paths
- [ ] All categories deleted without asking (user runs `/commit` before if backups needed)
- [ ] Deletion results reported with counts

## Output

- Clean workspace with temporary files removed
- Deletion report in chat with per-category counts
