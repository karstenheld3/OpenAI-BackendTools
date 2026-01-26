# Learnings Log

Populated by `/learn` workflow. Extracts transferable lessons from resolved problems.

**Goal**: Extract transferable lessons from resolved problems through structured retrospective analysis

## Table of Contents

1. [Learnings](#learnings)
2. [Document History](#document-history)

## Learnings

### [DATE] - [Context/Topic]

#### `[TOPIC]-LN-001` Learning Title

**Problem reference**: `[TOPIC]-PR-NNN` in PROBLEMS.md
**Linked failures**: `[TOPIC]-FL-NNN` in FAILS.md (if any)

**Original problem type**:
- Workflow: BUILD | SOLVE
- BUILD complexity: COMPLEXITY-LOW | COMPLEXITY-MEDIUM | COMPLEXITY-HIGH
- SOLVE type: RESEARCH | ANALYSIS | EVALUATION | WRITING | DECISION | HOTFIX | BUGFIX | CHORE | MIGRATION

**Context at decision time**:
- Available information: [What was known]
- Missing information: [What should have been known but wasn't]
- Constraints: [Time, resources, dependencies]

**Assumptions made**:
- [VERIFIED] [Assumption that was confirmed correct]
- [UNVERIFIED] [Assumption made without evidence]
- [CONTRADICTS] [Assumption that conflicted with reality]

**Rationale reconstructed**:
- Requirements specified: [FR-XX, DD-XX, IG-XX referenced]
- Design decisions: [What was decided and why]
- Trade-offs accepted: [What was sacrificed for what]

**Actual outcome**:
- What happened: [Actual result]
- Divergence point: [When/where plan failed]
- Missed signals: [What could have warned us]

**Evidence collected**:
- Conversation: [Key excerpts or references]
- Code: [Diffs, commits, file:line references]
- Logs: [Error messages, test output]
- Documents: [Spec/IMPL/TEST references]

**Problem dependency tree**:
```
[Root Cause]
├─> [Contributing Factor 1]
│   └─> [Symptom A]
└─> [Contributing Factor 2]
    ├─> [Symptom B]
    └─> [Symptom C]
```

**Root cause**: [Single sentence identifying the fundamental issue]

**Counterfactual**: If we had [done X instead], then [Y would have happened]

**Prevention**: Next time, we should [specific actionable guidance]

**FAILS.md updates**: (after analysis, update linked FL entries)
- `[TOPIC]-FL-NNN`: Updated "Why it went wrong" with [insight]
- `[TOPIC]-FL-NNN`: Updated "Suggested fix" with [recommendation]

## Location Rules

- **SESSION-BASED**: `[SESSION_FOLDER]/LEARNINGS.md`
- **PROJECT-WIDE + SINGLE-PROJECT**: `[WORKSPACE_FOLDER]/LEARNINGS.md`
- **PROJECT-WIDE + MONOREPO**: `[PROJECT_FOLDER]/LEARNINGS.md`

## Management Rules

- Run `/learn` workflow after marking problem as resolved
- Most recent entries at top
- Never delete entries
- Always update linked FAILS.md entries with insights
- Include in `/prime` workflow to load lessons learned

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial learnings log created
