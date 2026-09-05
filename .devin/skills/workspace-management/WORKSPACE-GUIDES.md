# Workspace Management Guides

High-level guidance for setting up and managing multi-repo agentic workspaces.

## When to Use Product/Dev Separation

Use product/dev separation when:
- Dev repo contains proprietary specs, sessions, evaluations, knowledge - not for public release
- Product repo contains shipped code, tests, config - safe for public release
- Workspace has multiple independent repos that need coordinated management

Do not use when:
- Single project with no separation between development artifacts and shipped code
- Monorepo where all content lives in one repository

## How to Structure a Workspace

A WORKSPACE mode workspace has:

- DevRepo (workspace root) - contains main.code-workspace, specs, sessions, knowledge, SOPs, agent folder
- ProductRepo - contains shipped code, tests, config, product docs. Referenced in main.code-workspace
- CompanyRepo (optional) - central source folder for knowledge and rules shared across multiple workspaces

Detection: WORKSPACE mode is detected by presence of main.code-workspace file in workspace root.

DevRepo structure:
- main.code-workspace (references ProductRepo and other repos)
- NOTES.md (workspace constants, project info, build/test rules)
- PROBLEMS.md, PROGRESS.md, ID-REGISTRY.md, SOPS.md, FAILS.md
- [AGENT_FOLDER]/ (rules, workflows, skills)
- knowledge/ (knowledge bundles)
- rules/ (rules bundles from Company)
- _PrivateSessions/ or session folders

ProductRepo structure:
- README.md (from PRODUCT_REPO_README_TEMPLATE.md)
- src/ (source code)
- tests/ (test code)
- docs/ (product documentation)
- Optional: [product-agent-folder]/ (product-specific agent folder)

CompanyRepo structure:
- NOTES.md (from COMPANY_REPO_NOTES_TEMPLATE.md, tracks downstream repos and sync policies)
- knowledge/ (knowledge bundles shared to downstream repos)
- rules/ (rules bundles shared to downstream repos)

## How to Configure Sync Sources

Direction definitions:
- Downstream = sync from source to all targets (distribute content to dependent repos)
- Upstream = sync from here back to source (push local changes back to origin)

Three sync sources, each with downstream and upstream directions:

1. Prompt System
   - Source: DevSystem source (latest DevSystemV* folder)
   - Target: [AGENT_FOLDER] in DevRepo and/or ProductRepo
   - Content: rules, workflows, skills
   - Filter: skill categories (not all repos get all skills)

2. Knowledge
   - Source: [KNOWLEDGE_SOURCE_FOLDER] (CompanyRepo)
   - Target: [KNOWLEDGE_FOLDER] (DevRepo)
   - Content: knowledge bundles (topic folders with reference documents)
   - Filter: bundle names from sync policy

3. Rules
   - Source: [RULES_SOURCE_FOLDER] (CompanyRepo)
   - Target: [RULES_FOLDER] (DevRepo)
   - Content: rules, workflows, design guidelines, SOPs
   - Filter: file patterns from sync policy

Sync policy lookup order:
1. Downstream repo NOTES.md (highest priority - local customizations)
2. CompanyRepo NOTES.md (central defaults)
3. Workspace constants (fallback if no policy found)

## How to Manage Knowledge Bundles

A knowledge bundle is a folder of reference documents for a specific topic (e.g., Windsurf/, AI-Standards/, OpenAI/).

To add a new knowledge bundle:
1. Create folder in [KNOWLEDGE_SOURCE_FOLDER] (CompanyRepo)
2. Add reference documents (.md files) to the folder
3. Update sync policy in CompanyRepo NOTES.md to include the new bundle
4. Run sync to distribute to downstream repos

To remove a knowledge bundle:
1. Remove from sync policy in CompanyRepo NOTES.md
2. Run sync - bundle will be marked for deletion in downstream repos
3. Confirm deletion during sync preview

Sub-bundles (nested folders) are supported (e.g., Windsurf/HowCascadeWorks/).

## Workspace Mode Detection Logic

```
Workspace root
├─> main.code-workspace exists?
│   ├─> Yes -> WORKSPACE mode
│   │   └─> Read .code-workspace folders to identify ProductRepo and other repos
│   └─> No
│       ├─> Multiple project subfolders?
│       │   ├─> Yes -> MONOREPO mode
│       │   └─> No -> SINGLE-PROJECT mode
```

In WORKSPACE mode, version strategy (SINGLE-VERSION vs MULTI-VERSION) is detected per repo, not workspace-wide.

## Sync Flow

```
User runs /sync workspace
├─> Read workspace constants from DevRepo NOTES.md
├─> Resolve sync policy (downstream NOTES.md -> CompanyRepo NOTES.md -> defaults)
├─> For each sync source (Prompt System, Knowledge, Rules):
│   ├─> Run diff script (compare source vs target)
│   ├─> Show preview: new, modified, deleted, skipped files
│   ├─> Mark locally-modified files (modified after .sync-timestamp)
│   └─> Mark breaking changes (structural changes requiring content migration)
├─> Prompt user for confirmation
├─> If confirmed:
│   ├─> For each sync source:
│   │   ├─> Run sync script (copy, delete, migrate)
│   │   ├─> Update .sync-timestamp
│   │   └─> Report results per file
│   └─> Summary: X added, Y modified, Z deleted, W skipped
└─> If not confirmed: abort, no changes made
```

## Verify Flow

```
User runs /verify workspace
├─> Read WORKSPACE-RULES.md from skill folder
├─> Read workspace constants from DevRepo NOTES.md
├─> Check required files per workspace type
├─> Check required constants (8 constants)
├─> Check agent folder structure (rules/, workflows/, skills/)
├─> Report gaps:
│   ├─> Missing constant -> add with template default
│   ├─> Missing required file -> create from template
│   ├─> Broken reference -> report only (requires user judgment)
│   └─> Structural violation -> report only
└─> Report all fixes with what changed and why
```

Downstream customizations are allowed and do not fail verification.
