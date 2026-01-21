---
description: EXPLORE phase - understand before acting
phase: EXPLORE
---

# Explore Workflow

## Required Skills

- @edird-phase-model for gate details

## Phase: EXPLORE

**Entry:** Start of workflow or explicit `/explore` call

### Verb Sequence

1. [RESEARCH] existing solutions and patterns
2. [ANALYZE] affected code/context/data
3. [GATHER] requirements and constraints
4. [ASSESS] → workflow type (BUILD/SOLVE) and complexity/problem-type
5. [SCOPE] define boundaries
6. [DECIDE] approach

### For BUILD

Assessment determines: COMPLEXITY-LOW / COMPLEXITY-MEDIUM / COMPLEXITY-HIGH

### For SOLVE

Assessment determines: RESEARCH / ANALYSIS / EVALUATION / WRITING / DECISION / HOTFIX / BUGFIX

### Gate Check: EXPLORE→DESIGN

- [ ] Problem or goal clearly understood
- [ ] Workflow type determined (BUILD or SOLVE)
- [ ] Assessment complete (complexity or problem-type)
- [ ] Scope boundaries defined
- [ ] No blocking unknowns requiring [ACTOR] input

**Pass**: Run `/design` | **Fail**: Continue [EXPLORE]

## Output

Update NOTES.md with:
```markdown
## Current Phase

**Phase**: EXPLORE
**Workflow**: BUILD | SOLVE
**Assessment**: COMPLEXITY-HIGH | RESEARCH | etc.
```
