---
description: Remove session content, conversation content, or specific files with preview and confirmation
auto_execution_mode: 1
---

# Remove Workflow

Remove session artifacts, Cascade conversations, or specified files from disk. Handles dependency cleanup. ALWAYS previews before removal.

**Goal**: Remove specified content with full preview, dependency cleanup, and explicit confirmation

**Why**: Sessions accumulate, conversations persist encrypted on disk, and manual cleanup is error-prone

Scope: Destructive file deletion. Requires explicit confirmation after preview.

## MUST-NOT-FORGET

- ALWAYS preview before deleting - no silent deletions
- NEVER delete without explicit user confirmation after preview
- NEVER delete active session files without user explicitly naming them
- Check dependencies (references from other files) before deleting documents
- Cascade .pb files are encrypted - identification by date/size only
- Close Windsurf before deleting cascade conversations to avoid file handle conflicts
- NEVER delete `.devin/`, `DevSystemV4.1/`, or `_OldDevSystemVersions/`
- NEVER delete `ID-REGISTRY.md`, `FAILS.md`, `LEARNINGS.md`, `!NOTES.md`, `!PROBLEMS.md`, `!PROGRESS.md`

## Trigger

- `/remove session content` - remove session folder and clean up references
- `/remove conversation` - remove Cascade conversation .pb files from disk
- `/remove [path]` - remove specific file or folder

## GLOBAL-RULES

Apply to all delete operations regardless of context.

1. Identify targets before any deletion
2. Scan for dependencies (grep for references to target in other files)
3. Show preview with full paths and sizes
4. Require explicit "yes" confirmation
5. Report results with counts and freed space

# CONTEXT-SPECIFIC

Detection: determine context from trigger arguments.

## Session Content

**Applies**: `/remove session content` or when user specifies a session folder

**Todo list for session deletion:**

1. Identify session folder (from argument, current session, or ask user)
2. Check if session is active (has uncommitted changes or is current working session)
3. Scan for outbound references:
   - `ID-REGISTRY.md` entries referencing session topic
   - `!PROGRESS.md` or `!PROBLEMS.md` entries referencing session
   - Other sessions referencing this session's documents
4. Scan for inbound references:
   - Files inside the session that reference external documents
5. Preview: list all files, total size, reference scan results
6. Confirm with user
7. Clean up references (remove ID-REGISTRY entries, update PROGRESS/PROBLEMS)
8. Delete session folder
9. Report results

**Preview format:**
```
_2026-05-14_CrawlerRefactor/
  12 files, 3.8 MB total
  Status: inactive (last commit 2026-05-14)
  - Outbound references (will be cleaned): 2
      ID-REGISTRY.md:142 - CRAWLENG topic registered
      !PROGRESS.md:28 - "Crawler refactor complete"
  - Inbound references (informational): 1
      _Sessions\_2026-06-01_IndexerV2\NOTES.md:15 - "See _SPEC_CRAWLENG-01.md for API format"

IMPORTANT: This will permanently delete the session folder and clean 2 outbound references.
Confirm? (yes/no)
```

## Conversation Content

**Applies**: `/remove conversation` or when user mentions Cascade conversation removal

Cascade conversations are stored as encrypted .pb files in `~/.codeium/windsurf/cascade/`.
Files are encrypted on disk but the agent has access to conversation content via `trajectory_search` tool.

**Scripts**: `[DEVSYSTEM_FOLDER]/skills/session-management/cascade-search.ps1` and `cascade-delete.ps1`

**Todo list for conversation deletion:**

1. Run cascade-search.ps1 to list recent conversations (default: last 10)
2. For each conversation, use `trajectory_search` (empty query) to retrieve title and messages
3. Build preview with: title, first 2 messages (truncated to 80 chars), last 2 messages (truncated to 80 chars)
4. Present preview to user - user selects by number or title
5. Run cascade-delete.ps1 with specified parameters (uses -DryRun first)
6. Confirm with user
7. Execute deletion
8. Report results, advise Windsurf restart

**Correlation strategy**: Match .pb file LastWriteTime with conversation timestamps from `trajectory_search`. The cascade ID from the trajectory metadata maps to the .pb filename UUID.

**Selection methods:**
- By number: "delete conversation 3" or "delete conversations 3-7"
- By title: "delete the one about authentication"
- By date: "delete conversations before 2026-06-01"
- By age: "delete conversations older than 30 days"
- Current: "delete this conversation" (match by current cascade ID)
- All: "delete all conversations" (requires double confirmation)

**Preview format:**
```
[ 1 / 3 ] "Fix authentication bug in login flow"
  2026-07-08 14:32 | 4.3 MB
  First: [user] Fix the auth bug that causes 401 on refresh token...
         [agent] I'll investigate the token refresh logic in...
  Last:  [user] looks good, commit it
         [agent] Committed: fix(auth): handle expired refresh...

[ 2 / 3 ] "Add /remove workflow for session management"
  2026-07-06 10:18 | 1.3 MB
  First: [user] Draft /remove workflow to support session removal...
         [agent] Here's a workflow for removal operations...
  Last:  [user] where is the remove.md workflow?
         [agent] The /remove workflow doesn't exist on disk...

[ 3 / 3 ] "Research vector databases for RAG"
  2026-07-01 16:00 | 0.6 MB
  First: [user] /deep-research "Compare vector databases for RAG"
         [agent] Starting deep research on vector databases...
  Last:  [agent] Research complete. Summary in _INFO_VECDB-01...
         [user] /session-save

3 conversations, 6.2 MB total.
Enter number(s) to delete (e.g., "1", "1-3", "all"):
```

## Specific Path

**Applies**: `/remove [path]` or when user names a specific file/folder

**Todo list for specific path deletion:**

1. Verify path exists
2. Check if path is in protected locations (abort if yes)
3. If directory: list contents recursively with sizes
4. If file: show file info (path, size, last modified)
5. Scan for references to this path in other files (grep basename)
6. Preview with dependency info
7. Confirm with user
8. Delete
9. Report results

**Preview format (directory):**
```
e:\Dev\IPPS\_Sessions\_2026-05-14_CrawlerRefactor/
  Directory, 12 files, 3.8 MB total
  Last modified: 2026-05-14 17:42
  - Contents:
      _INFO_CRAWLENG-01.md              42 KB
      _SPEC_CRAWLENG-01.md              18 KB
      _IMPL_CRAWLENG-01.md              31 KB
      __STRUT_CRAWLENG.md                6 KB
      NOTES.md                           4 KB
      PROBLEMS.md                        2 KB
      PROGRESS.md                        3 KB
      poc/test_crawler.py               12 KB
      poc/results.json                 3.7 MB
  - References found: 3
      ID-REGISTRY.md:142 - CRAWLENG topic registered
      !PROGRESS.md:28 - "Crawler refactor complete (2026-05-14)"
      _Sessions\_2026-06-01_IndexerV2\NOTES.md:15 - "See _SPEC_CRAWLENG-01.md for API format"

IMPORTANT: This will permanently delete the directory and all 12 files.
Confirm? (yes/no)
```

**Preview format (file):**
```
e:\Dev\IPPS\_Sessions\_2026-05-14_CrawlerRefactor\_INFO_CRAWLENG-01.md
  File, 42 KB
  Last modified: 2026-05-14 11:23
  - References found: 1
      _IMPL_CRAWLENG-01.md:8 - "Depends on: _INFO_CRAWLENG-01.md [CRAWLENG-IN01]"

WARNING: Other documents depend on this file.
Confirm? (yes/no)
```

# EXECUTION

## Step 1: Determine Context

Parse user input to determine which context applies:
- Contains "session" → Session Content
- Contains "conversation" or "cascade" → Conversation Content
- Contains a file/folder path → Specific Path
- Ambiguous → ask user which context (one question only)

## Step 2: Gather Targets

Per context-specific todo list above.

## Step 3: Dependency Scan

```powershell
# Scan for references to target basename in workspace
$basename = Split-Path $targetPath -Leaf
Get-ChildItem -Path "[WORKSPACE_FOLDER]" -Recurse -Include "*.md" |
    Select-String -Pattern ([regex]::Escape($basename)) -SimpleMatch |
    Where-Object { $_.Path -ne $targetPath } |
    Select-Object Path, LineNumber, Line
```

Skip dependency scan for conversation deletion (no cross-references possible).

## Step 4: Preview

Show grouped results per context-specific format above. Include:
- Full paths (never abbreviated)
- File sizes
- Dependency scan results
- Warnings for irreversible operations

## Step 5: Confirm

Require explicit "yes" response. Accept: `yes`, `y`, `confirm`.
Anything else = abort.

For "delete all conversations": require typing "DELETE ALL" (double confirmation).

## Step 6: Execute

- Sessions: clean references first, then delete folder
- Conversations: run cascade-delete.ps1 with -Confirm flag
- Specific paths: Remove-Item -Recurse -Force

## Step 7: Report

```
OK. Deletion complete.
  - Deleted: 12 files
      _INFO_CRAWLENG-01.md
      _SPEC_CRAWLENG-01.md
      _IMPL_CRAWLENG-01.md
      ...
  - Freed: 3.8 MB
  - References cleaned: 2
      ID-REGISTRY.md:142 - removed CRAWLENG entry
      !PROGRESS.md:28 - removed line

HINT: Restart Windsurf for conversation changes to take effect.
```

# FINALIZATION

## Quality Gate

- [ ] Targets identified before any deletion
- [ ] Protected locations checked and excluded
- [ ] Dependencies scanned (except for conversations)
- [ ] Preview shown with full paths
- [ ] User confirmed with explicit "yes"
- [ ] Deletion results reported with freed space
- [ ] References cleaned (for session deletion)

## Output

- Target files/folders removed from disk
- Cross-references cleaned (ID-REGISTRY, PROGRESS, PROBLEMS)
- Deletion report in chat
