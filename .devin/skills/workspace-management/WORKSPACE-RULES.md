# Workspace Management Rules

Verifiable rules for workspace setup and integrity.

## Rule Index

Files (FL)
- WS-FL-01: DevRepo must contain required tracking files
- WS-FL-02: ProductRepo must contain README.md
- WS-FL-03: CompanyRepo must contain NOTES.md if it exists

Constants (CT)
- WS-CT-01: DevRepo NOTES.md must define all 8 workspace constants
- WS-CT-02: Constants must not contain hardcoded project-specific paths
- WS-CT-03: Constants must use [WORKSPACE_FOLDER] as base where applicable

Structure (ST)
- WS-ST-01: Agent folder must contain rules/, workflows/, skills/ subfolders
- WS-ST-02: All skills in [SKILL_CATEGORIES] must exist in skills/ folder
- WS-ST-03: All skills in skills/ folder must be registered in [SKILL_CATEGORIES]
- WS-ST-04: No deprecated files in agent folder

Sync (SY)
- WS-SY-01: SyncPolicy direction must be "downstream" or "upstream"
- WS-SY-02: SyncPolicy must define source_folder and target_folder
- WS-SY-03: Preserve list files must not be overwritten during sync
- WS-SY-04: .sync-timestamp must be created after sync completes
- WS-SY-05: Locally-modified files not in preserve list must trigger warning before overwrite

Templates (TM)
- WS-TM-01: Templates must use _TEMPLATE suffix
- WS-TM-02: Templates must follow TEMPLATE_RULES.md
- WS-TM-03: Templates must mark required vs optional sections

Privacy (PR)
- WS-PR-01: No real identifiers, project names, or paths in skill files
- WS-PR-02: No real identifiers in template examples or placeholder values

## WS-FL-01: Required DevRepo Files

DevRepo must contain:
- NOTES.md
- PROBLEMS.md
- PROGRESS.md
- ID-REGISTRY.md
- SOPS.md
- FAILS.md

BAD: DevRepo missing ID-REGISTRY.md - workspace IDs cannot be tracked
GOOD: All 6 required files present in DevRepo root

## WS-CT-01: Required Workspace Constants

DevRepo NOTES.md must define all 8 constants:
- [DEV_REPO_FOLDER]
- [PRODUCT_REPO_FOLDER]
- [COMPANY_REPO_FOLDER]
- [KNOWLEDGE_FOLDER]
- [KNOWLEDGE_SOURCE_FOLDER]
- [RULES_FOLDER]
- [RULES_SOURCE_FOLDER]
- [PRODUCT_DOCS_FOLDER]

BAD: NOTES.md defines [KNOWLEDGE_FOLDER] but not [KNOWLEDGE_SOURCE_FOLDER] - sync cannot find source
GOOD: All 8 constants defined with paths relative to [WORKSPACE_FOLDER]

## WS-CT-02: No Hardcoded Project Paths

Constants must use [WORKSPACE_FOLDER] as base, not absolute paths.

BAD: [PRODUCT_REPO_FOLDER]: e:\Dev\MyProject
GOOD: [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\MyProject

## WS-ST-01: Agent Folder Structure

Agent folder must contain rules/, workflows/, skills/ subfolders.

BAD: Agent folder has rules/ and workflows/ but no skills/ - skills cannot be loaded
GOOD: Agent folder has all three subfolders with content

## WS-ST-02: Skills Registered in CATEGORIES

All skills present in skills/ folder must be registered in NOTES.md [SKILL_CATEGORIES].

BAD: skills/pdf-tools/ exists but not in [SKILL_CATEGORIES] - skill is invisible to deploy-to-all-repos
GOOD: All skill folders have corresponding entry in [SKILL_CATEGORIES]

## WS-SY-01: Valid SyncPolicy Direction

SyncPolicy direction field must be "downstream" or "upstream".

BAD: direction: "both" - ambiguous, sync script cannot determine operation
GOOD: direction: "downstream" - clear, sync copies source to target

## WS-SY-03: Preserve List Enforcement

Files listed in preserve list must never be overwritten during sync, regardless of source changes.

BAD: Sync overwrites NOTES.md because source has newer version, destroying local customizations
GOOD: Sync skips NOTES.md because it is in preserve list, local customizations preserved

## WS-TM-01: Template Suffix

Template files must use _TEMPLATE suffix (SK-FL-07).

BAD: DEV_REPO_NOTES.md (looks like an operational file, may be used directly without adaptation)
GOOD: DEV_REPO_NOTES_TEMPLATE.md (clearly a template requiring adaptation)

## WS-PR-01: Privacy Gate

No real identifiers, project names, paths, names of real people, or session-specific references in skill files.

BAD: [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\MyRealProject
GOOD: [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\[product-repo-name]
