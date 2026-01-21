---
description: DESIGN phase - plan before executing
phase: DESIGN
---

# Design Workflow

## Required Skills

- @write-documents for document templates
- @edird-phase-model for gate details

## Phase: DESIGN

**Entry gate:** EXPLORE→DESIGN passed

### Verb Sequence

1. [PLAN] structured approach
2. [OUTLINE] high-level structure
3. [WRITE-SPEC] specification document
4. [PROVE] risky parts with POC (if COMPLEXITY-MEDIUM or higher)
5. [DECOMPOSE] into small testable steps
6. [WRITE-IMPL-PLAN] implementation plan
7. [WRITE-TEST-PLAN] test plan
8. [VALIDATE] design with [ACTOR] (if needed)

### For COMPLEXITY-LOW

Minimal documents - concise 1-2 page versions of SPEC, IMPL, TEST.

### For COMPLEXITY-HIGH

- [PROVE] required for risky parts
- [PROPOSE] options to [ACTOR] before proceeding

### Gate Check: DESIGN→IMPLEMENT

- [ ] Approach documented (outline, spec, or plan)
- [ ] Risky parts proven via POC (if COMPLEXITY-MEDIUM or higher)
- [ ] No open questions requiring [ACTOR] decision
- [ ] For BUILD: SPEC, IMPL, TEST documents created
- [ ] For BUILD: Plan decomposed into small testable steps
- [ ] For SOLVE: Structure/criteria validated

**Pass**: Run `/implement` | **Fail**: Continue [DESIGN]

## Output

Update NOTES.md with current phase. Create documents in session folder:
- `_SPEC_[TOPIC].md`
- `_IMPL_[TOPIC].md`
- `_TEST_[TOPIC].md` (if applicable)
