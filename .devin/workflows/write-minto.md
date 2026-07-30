---
description: Develop a full Minto Pyramid article from a MINTO draft
auto_execution_mode: 1
---

# Write Minto Workflow

Develop a selected argument into a complete Minto Pyramid article with drill-down sections, evidence, and closing.

**Goal**: `_MINTO_[Article].md` - top-down structured article with AMINTON tree appendix

**Why**: A draft contains root-level structure (A + Q + A) but lacks proof depth. This workflow adds sub-questions, evidence, and closing to create a complete, verifiable argument rendered as readable prose.

**Scope**: Drill-down development and article rendering. Requires an existing `__MINTO-DRAFT_*.md` (or runs `/propose-minto` first).

## Required Skills

- @skills:write-documents `MINTO_GUIDE.md` for prose style, closing rules, structure decisions
- @skills:write-documents `MINTO_RULES.md` for structural verification (quality gate)
- @skills:write-documents `MINTO_TEMPLATE.md` for output structure
- @skills:write-documents for APAPALAN/MECT compliance

## MUST-NOT-FORGET

- Every E-node must reference a source finding from the inventory (IG-01)
- No orphan nodes: every Q has A, every A in drill-down has S, every S has E (IG-02)
- Closing introduces no new claims - only restates proved branches (IG-03)
- MECE (Mutually Exclusive, Collectively Exhaustive) at all levels (IG-04)
- Structure: 3-5 questions, max 3 answers each (DD-03)
- Bottom-up synthesis (thinking) precedes top-down communication (writing)
- Confirm before overwriting existing `_MINTO_*.md`
- Reference `_INFO_AGENTIC_MINTO_ARTICLES.md [MINTO-IN01]` for AMINTON notation and tree structure

## Trigger

- `/write-minto [draft-path]` - Develop full article from specified draft
- `/write-minto [material-path]` - Run full pipeline (calls `/propose-minto` first)
- `/write-minto` (no path) - Look for existing draft in session; if none, use all session INFO docs

## Prerequisites

- Existing `__MINTO-DRAFT_*.md` with `[RECOMMENDED]` argument, OR source material for `/propose-minto`
- If no draft and no source material: stop and report

## Steps

### 1. Prerequisite Check (FR-10)

Check for existing `__MINTO-DRAFT_*.md` in scope:
- **Found**: Read draft, use `[RECOMMENDED]` argument as starting point
- **Not found**: Execute `/propose-minto` first, then continue with its output

### 2. Re-read Source Material

Re-read all source material listed in draft's "Source material" section. Focus on evidence relevant to the selected argument's Q-branches.

### 3. Drill-Down Development (FR-07)

For each QnAn (answer) in the Root Section:

1. **Develop sub-question** (QnAn-S1): What must be proved for this answer to be credible?
2. **Find evidence** from findings inventory (QnAn-S1E1..E3):
   - Each E-node references a specific finding (Fnn) from the inventory
   - Target: 2-3 evidence items per sub-question
   - Minimum: 1 evidence item per sub-question

If evidence not found for an answer: mark with `[ASSUMED - no evidence in inventory]` and flag for `/improve` (EC-04).

Additional sub-questions (S2, S3) may be added where the answer requires multiple proof angles.

### 4. Closing Generation (FR-08)

Generate closing section:
- One summary line per answer, grouped by parent question
- Restate A as conclusion (final line)
- Verify: closing contains no claims absent from the tree (IG-03)

### 5. Extended Draft Update

Update `__MINTO-DRAFT_[Article].md` with full AMINTON tree (all levels through E-nodes) and closing section.

### 6. Article Rendering (FR-09)

Convert complete AMINTON tree into prose article. Structure:

```markdown
# [Article Title]

**Doc ID**: [TOPIC]-MINTO-[NN]
**Source**: __MINTO-DRAFT_[Article].md
**Argument**: [Root argument A restated]

## Executive Summary

[SCQA: Situation (what reader knows) -> Complication (what changed) -> Answer (restate A). 2-3 paragraphs max. See MINTO_TEMPLATE.md.]

## [Q1 as section heading]

[Q1A1 as paragraph with supporting evidence from S/E level]
[Q1A2 as paragraph with supporting evidence]
[Q1A3 as paragraph with supporting evidence]

## [Q2 as section heading]

[Q2A1-Q2A3 as paragraphs with evidence]

## [Q3 as section heading]

[Q3A1-Q3A3 as paragraphs with evidence]

## Conclusion

[Closing: summary of proved branches, restated A]

## Appendix: AMINTON Structure

[Full AMINTON tree with all levels for machine verification]
```

Write to `_MINTO_[Article].md`. If file exists: confirm with user before overwriting.

## Quality Gate

- [ ] Root Section complete (A + all Qs + all QnAns)
- [ ] Every QnAn has at least one sub-question (QnAn-S1)
- [ ] Every sub-question has at least one evidence item
- [ ] No orphan nodes (IG-02)
- [ ] Every E-node references source material (IG-01)
- [ ] Closing section present with one line per answer
- [ ] Closing introduces no new claims (IG-03)
- [ ] MECE at all levels (IG-04)
- [ ] AMINTON tree appendix matches prose structure
- [ ] Prose follows top-down order: conclusion, arguments, evidence
- [ ] Article Doc ID assigned

## Output

- `_MINTO_[Article].md` in `[SESSION_FOLDER]/` or `[SESSION_FOLDER]/MINTO/`
- Updated `__MINTO-DRAFT_[Article].md` with full AMINTON tree
- Suggest: "Run `/verify` to check structural completeness, `/critique` for logic flaws"
