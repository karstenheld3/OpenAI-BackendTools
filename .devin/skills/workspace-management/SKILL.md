---
name: workspace-management
description: Manages multi-repo workspace setup, DevSystem synchronization, and knowledge distribution. Use when configuring workspace constants, syncing between source and target repos, verifying workspace integrity, or committing across multiple repos.
compatibility: PowerShell 7+ for diff/sync scripts
---

# Workspace Management

Manages workspace setup, DevSystem sync, and knowledge distribution across product/dev/company repo architectures.

References (loaded on demand):
- WORKSPACE-GUIDES.md - High-level guidance on workspace setup, product/dev separation, sync sources
- WORKSPACE-RULES.md - Verifiable rules for workspace integrity, required files and constants
- DEV_REPO_NOTES_TEMPLATE.md - Template for DevRepo NOTES.md with all workspace constants
- PRODUCT_REPO_README_TEMPLATE.md - Template for ProductRepo README.md
- COMPANY_REPO_NOTES_TEMPLATE.md - Template for CompanyRepo NOTES.md with sync policy tracking
- workspace_diff_template.ps1 - Diff script template (adapt before use)
- workspace_sync_template.ps1 - Sync script template (adapt before use)

## MUST-NOT-FORGET

1. All paths must come from workspace constants in DevRepo NOTES.md - never hardcode project-specific paths
2. Sync before deploy - always run diff and review changes before executing sync
3. Check preserve list before overwriting - files in preserve list are never overwritten during sync
4. Rollback on shared branches (main, master, remote-tracked) requires explicit confirmation - advise revert commit instead
5. Privacy gate - no real identifiers, project names, or paths in any skill file
6. Register skill in NOTES.md [SKILL_CATEGORIES] AND deploy-to-all-repos.md $skillCategories after creation

## Intent Lookup

User wants to...
- Compare workspace settings → Procedure 1, FR-15
- Update workspace from source → Procedure 2, FR-16
- Roll back workspace settings → Procedure 3, FR-17
- Check workspace integrity → Procedure 4, FR-18
- Compare DevSystem files → Procedure 1, FR-19
- Update DevSystem from source → Procedure 2, FR-20
- Roll back DevSystem → Procedure 3, FR-21
- Check DevSystem integrity → Procedure 4, FR-22
- Compare knowledge bundles → Procedure 1, FR-23
- Update knowledge from source → Procedure 2, FR-24
- Roll back knowledge → Procedure 3, FR-25
- Check knowledge integrity → Procedure 4, FR-26
- Commit across multiple repos → Procedure 5, FR-30

## Core Procedures

### 1. Compare

```
1. Read workspace constants from DevRepo NOTES.md
2. Determine sync area (WORKSPACE, DEVSYSTEM, KNOWLEDGE)
3. Determine sync source and target from constants
4. Run workspace_diff_template.ps1 with Source, Target, Filter parameters
5. Review structured diff report: new files, modified files, deleted files, skipped files
6. Note locally-modified files (modified after .sync-timestamp) for sync warning
```

Use before any sync operation to preview changes. Use before deploy to verify DevSystem is current.

### 2. Update

```
1. Run Compare procedure first
2. Review diff preview - check for breaking changes, locally-modified files
3. Read sync policy from downstream NOTES.md (priority 1) or CompanyRepo NOTES.md (priority 2)
4. Confirm sync: prompt user (yes/go/confirmed/execute/apply to proceed, no/cancel/abort/stop to abort)
5. Run workspace_sync_template.ps1 with DiffReport, Direction, PreserveList parameters
6. Verify .sync-timestamp updated in target folder root
7. Report results per file: added, modified, deleted, skipped, migrated
```

Use to sync DevSystem from source, knowledge from Company, or rules from Company. Downstream = sync from source to all targets. Upstream = sync from here back to source.

### 3. Rollback

```
1. Determine area to rollback (WORKSPACE, DEVSYSTEM, KNOWLEDGE)
2. Check current branch: if shared (main, master, remote-tracked), display warning
3. Advise manual revert commit for shared branches. Proceed only with explicit confirmation
4. For non-shared branches: use git history to identify previous version
5. Roll back using git checkout of previous committed version
6. Report what changed between current and rolled-back version
```

Use when sync introduced errors or unwanted changes. IG-07: rollback on shared branches is dangerous - always warn first.

### 4. Integrity Check

```
1. Determine area to check (WORKSPACE, DEVSYSTEM, KNOWLEDGE)
2. For WORKSPACE: verify required constants in DevRepo NOTES.md, required files exist, workspace structure matches declared mode
3. For DEVSYSTEM: verify agent folder has rules/, workflows/, skills/ subfolders, all skills registered in [SKILL_CATEGORIES], no deprecated files
4. For KNOWLEDGE: verify knowledge folder exists if [KNOWLEDGE_FOLDER] set, all bundles in sync policy exist, no empty bundles
5. Report gaps and incompatibilities
6. Fix actions: missing constant -> add with template default. Missing file -> create from template. Broken reference -> report only. Structural violation -> report only
```

Use via /verify workspace context. Downstream customizations are allowed and do not fail verification.

### 5. Multi-Repo Commit

```
1. Detect WORKSPACE mode (main.code-workspace exists)
2. Detect changes across all git repos in workspace
3. Commit order: 1) product repo, 2) dev repo, 3) all other workspace repos
4. For each repo with changes:
   a. Detect uncommitted changes
   b. Analyze by type (feat, fix, docs, test, chore)
   c. Use git -C [repo_path] for all git operations
   d. Detect and use per-repo git config (user.name, user.email)
   e. Create conventional commits
5. If a repo commit fails: report error, continue with remaining repos, summarize partial success
6. Skip repos with no changes silently
7. Report committed changes per repo at end
```

Use via /commit in WORKSPACE mode. SINGLE-PROJECT and MONOREPO modes use existing single-repo commit behavior.

## Gotchas

- Sync timestamp missing - If .sync-timestamp not found in target folder, full comparison runs (no incremental optimization). Timestamp created after sync completes
- Preserve list overrides overwrite rules - Files in preserve list are never overwritten, even if source has newer version. Check preserve list before sync
- Rollback on shared branches - Using git checkout on shared branches (main, master) can cause issues for other contributors. Always use revert commit instead. IG-07 requires explicit confirmation

## Quick Config

Minimal workspace constants in DevRepo NOTES.md:

```
## Workspace Constants
- [DEV_REPO_FOLDER]: [WORKSPACE_FOLDER]
- [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\[product-repo-name]
- [COMPANY_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\Company
- [KNOWLEDGE_FOLDER]: [DEV_REPO_FOLDER]\knowledge
- [KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
- [RULES_FOLDER]: [DEV_REPO_FOLDER]\rules
- [RULES_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\rules
- [PRODUCT_DOCS_FOLDER]: [PRODUCT_REPO_FOLDER]\docs
```

See DEV_REPO_NOTES_TEMPLATE.md for full template with defaults and instructions.
