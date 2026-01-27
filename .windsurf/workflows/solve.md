---
description: SOLVE workflow - explore problems, evaluate ideas, make decisions
auto_execution_mode: 1
---

# Solve Workflow

Entry point for SOLVE workflow - research, analysis, evaluation, decisions.

## Required Skills

- @edird-phase-planning for phase gates and planning
- @session-management for session setup
- @write-documents for document templates

## Usage

```
/solve "Research authentication best practices"
/solve "Evaluate database migration options"
```

## Workflow

1. Run `/session-new` with task name
2. Invoke @edird-phase-planning skill
3. Follow phases: EXPLORE → DESIGN → IMPLEMENT → REFINE → DELIVER
4. Check gates before each transition
5. Run `/session-finalize` when done

## SOLVE-Specific Rules

- **Problem types**: RESEARCH, ANALYSIS, EVALUATION, WRITING, DECISION
- **Research triggers**: Must cite sources, not training data
- **Primary output**: INFO document with findings/recommendations
- **HOTFIX/BUGFIX**: Start as SOLVE (root cause), switch to BUILD for fix
