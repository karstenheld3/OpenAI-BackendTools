# DevRepo NOTES Template

Template for DevRepo NOTES.md. Copy and adapt for your workspace.

Replace all `[placeholder]` values with your workspace-specific content.

## Workspace Constants

- [DEV_REPO_FOLDER]: [WORKSPACE_FOLDER]
- [PRODUCT_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\[product-repo-name]
- [COMPANY_REPO_FOLDER]: [WORKSPACE_FOLDER]\..\Company
- [KNOWLEDGE_FOLDER]: [DEV_REPO_FOLDER]\knowledge
- [KNOWLEDGE_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\knowledge
- [RULES_FOLDER]: [DEV_REPO_FOLDER]\rules
- [RULES_SOURCE_FOLDER]: [COMPANY_REPO_FOLDER]\rules
- [PRODUCT_DOCS_FOLDER]: [PRODUCT_REPO_FOLDER]\docs

Instructions: Replace [product-repo-name] with your product repository folder name. Adjust [COMPANY_REPO_FOLDER] if your company folder is in a different location. All paths should be relative to [WORKSPACE_FOLDER].

## Sync Sources

Direction definitions:
- Downstream = sync from source to all targets (distribute content to dependent repos)
- Upstream = sync from here back to source (push local changes back to origin)

### Prompt System
- Source: [WORKSPACE_FOLDER]\..\[devsystem-source-name]\DevSystemV*
- Target: [DEV_REPO_FOLDER]\[AGENT_FOLDER]
- Direction: downstream
- Filter: skill categories from [SKILL_CATEGORIES]

### Knowledge
- Source: [KNOWLEDGE_SOURCE_FOLDER]
- Target: [KNOWLEDGE_FOLDER]
- Direction: downstream
- Filter: bundle names from sync policy

### Rules
- Source: [RULES_SOURCE_FOLDER]
- Target: [RULES_FOLDER]
- Direction: downstream
- Filter: file patterns from sync policy

Instructions: Adjust source paths if your DevSystem source or Company folder is in a different location. Set direction to "upstream" for target-to-source sync.

## Project Info

- Project name: [project-name]
- Project goal: [one-sentence-description]
- Workspace mode: WORKSPACE
- Version strategy: SINGLE-VERSION

Instructions: Replace placeholder values with your project information.

## Build/Test Rules

- Build command: [build-command]
- Test command: [test-command]
- Lint command: [lint-command]

Instructions: Define commands for building, testing, and linting your product repo.

## Skill Categories

[SKILL_CATEGORIES]
- Development: [list-of-development-skills]
- Infrastructure: [list-of-infrastructure-skills]
- Research: [list-of-research-skills]

Instructions: Register all skills installed in your agent folder. Categories determine which skills are synced to which downstream repos.
