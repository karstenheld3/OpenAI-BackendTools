---
description: Global and local refactoring with exhaustive search and verification
auto_execution_mode: 1
---

# Rename / Refactor Workflow

Robust pattern replacement across files with analysis, planning, execution, and verification.

## Workflow

### Phase 1: Analysis

1. **Clarify scope** - Ask user if not clear:
  - Global (entire workspace) or Local (specific folder/files)?

2. **Search for all occurrences** - Use grep_search (case-insensitive by default):
  ```
  grep_search: Query="<old_pattern>", SearchPath="<scope>", CaseSensitive=false
  ```

3. **Build occurrence list** - For each match, record:
  - File path
  - Line number(s)
  - Context (surrounding text)

4. **Identify special cases**:
  - Protected files (e.g., `.windsurf/`, `node_modules/`)
  - Binary files (skip)
  - Case sensitivity issues (would changing casing break integrity?)

### Phase 2: Planning

5. **Create replacement plan** - Group by action type:
  - **Direct edits** - Files that can be edited
  - **Manual sync** - Protected folders needing file copy
  - **Skip** - Binary/generated files

6. **Present plan to user** - Show total occurrences
  - Only ask for confirmation if Step 1.4 yielded critical cases

### Phase 3: Execution

7. **Execute replacements**:
  - Edit accessible files with `replace_all=true` for multiple occurrences
  - For protected folders: use PowerShell to copy updated files

### Phase 4: Verification

9. **[VERIFY] Re-search for old pattern** - Should return zero results except user confirmed exceptions

10. **Report results** - Files updated, remaining occurrences, manual actions needed
