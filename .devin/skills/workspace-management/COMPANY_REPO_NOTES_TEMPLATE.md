# CompanyRepo NOTES Template

Template for CompanyRepo NOTES.md. Copy and adapt for your company repository.

Replace all `[placeholder]` values with your organization-specific content.

## Company Info

- Company folder: [COMPANY_REPO_FOLDER]
- Description: [one-sentence-description]
- Maintainer: [role-or-team]

## Downstream Repositories

### [downstream-repo-1]

- Repo path: [absolute-or-relative-path]
- Skill categories: Development, Infrastructure
- Knowledge bundles: [bundle-1], [bundle-2]
- Rules: [rule-set-1]
- Workflows: [workflow-1]
- DevSystem rules to sync: [rule-1], [rule-2]
- Overwrite rules:
  - Overwrite: rules/, workflows/, skills/
  - Preserve: NOTES.md, PROBLEMS.md, PROGRESS.md
- Content filters:
  - Include: *.md, *.ps1
  - Exclude: _*, .*

### [downstream-repo-2]

- Repo path: [absolute-or-relative-path]
- Skill categories: Research
- Knowledge bundles: [bundle-3]
- Rules: [rule-set-2]
- Workflows: [workflow-2]
- DevSystem rules to sync: [rule-3]
- Overwrite rules:
  - Overwrite: rules/, workflows/
  - Preserve: NOTES.md, *.local.md
- Content filters:
  - Include: *.md
  - Exclude: _*, .*, *.local.*

Instructions: Add one section per downstream repo. Define which skill categories, knowledge bundles, rules, and workflows each repo receives. Overwrite rules control which files are replaced vs preserved during sync. Content filters control which file patterns are included or excluded.

## Sync Policy Data Structure

Example sync policy entry in JSON format:

```json
{
  "repo_path": "[WORKSPACE_FOLDER]\\..\\[downstream-repo]",
  "skill_categories": ["Development", "Infrastructure"],
  "knowledge_bundles": ["[bundle-1]", "[bundle-2]"],
  "rules": ["[rule-set-1]", "[rule-set-2]"],
  "workflows": ["[workflow-1]", "[workflow-2]", "[workflow-3]"],
  "devsystem_rules": ["[rule-1]", "[rule-2]"],
  "overwrite": {
    "overwrite_paths": ["rules/", "workflows/", "skills/"],
    "preserve_patterns": ["NOTES.md", "PROBLEMS.md", "PROGRESS.md", "*.local.*"]
  },
  "content_filter": {
    "include_patterns": ["*.md", "*.ps1"],
    "exclude_patterns": ["_*", ".*"]
  }
}
```

Instructions: Adapt the data structure to your needs. The sync scripts read this structure to determine what to sync, what to overwrite, and what to preserve.
