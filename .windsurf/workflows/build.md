---
description: BUILD workflow - create software, features, systems
auto_execution_mode: 1
---

# Build Workflow

Entry point for BUILD workflow - creating software, features, systems.

## Required Skills

- @edird-phase-planning for phase gates and planning
- @session-management for session setup
- @write-documents for document templates

## Usage

```
/build "Add user authentication API"
```

## Workflow

1. Run `/session-new` with feature name
2. Invoke @edird-phase-planning skill
3. Follow phases: EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER
4. Check gates before each transition
5. Run `/session-close` when done

## BUILD-Specific Rules

- **UI work**: Visual reference (screenshot/video) is MANDATORY
- **UI work**: Max 100 lines before visual verification
- **Artifacts**: SPEC, IMPL, TEST documents required (depth per complexity)
- **Gate bypass forbidden**: Must list actual artifact paths as evidence
