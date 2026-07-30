---
description: Generate MINTO-structured argument candidates for a Minto Pyramid article
auto_execution_mode: 1
---

# Propose Minto Workflow

Generate 3 candidate arguments with full AMINTON Root Sections from source material. Select the strongest and output a draft.

**Goal**: `__MINTO-DRAFT_[Article].md` with 3 scored candidates, one marked `[RECOMMENDED]`

**Why**: Ad-hoc synthesis produces arguments without traceable evidence or explicit selection criteria. This workflow ensures the strongest argument is identified through a structured funnel with scored dimensions.

**Scope**: Argument generation and selection only. Use `/write-minto` for drill-down development and final article rendering.

## Required Skills

- @skills:write-documents `MINTO_GUIDE.md` for strategic decisions (magnet, ordering, selection)
- @skills:write-documents `MINTO_RULES.md` for structural verification (quality gate)
- @skills:write-documents `MINTO-DRAFT_TEMPLATE.md` for output structure
- @skills:write-documents for APAPALAN/MECT compliance

## MUST-NOT-FORGET

- Selection funnel: 8 candidates → 3 selected (scored), 5 questions → 3 selected (scored), 5 answers → 3 selected
- Magnet Rule: every candidate A must connect to a listener motivator - eliminate before scoring
- Question ordering: must follow a stated logical method (see MINTO_GUIDE.md Section 3.1); Why-How-What is default for persuasion
- One-Argument Test: can tree collapse to 1Q with 3 answers? If yes, restructure
- Evidence traceability: every answer must be supportable from findings inventory
- MECE (Mutually Exclusive, Collectively Exhaustive) at every level: no overlapping questions, no overlapping answers
- Reference `_INFO_AGENTIC_MINTO_ARTICLES.md [MINTO-IN01]` for AMINTON notation and tree structure

## Trigger

- `/propose-minto [material-path]` - Generate candidates from specified material
- `/propose-minto` (no path) - Use all INFO documents in current session folder

## Prerequisites

- At least one INFO document or source file exists in scope
- If no source material found: stop and report "No source material in scope"

## Steps

### 1. Material Ingestion (FR-01)

Read all source material in scope. Build findings inventory:

```
- F01: [finding] (source: [file], label: [VERIFIED/ASSUMED])
- F02: [finding] (source: [file], label: [VERIFIED/ASSUMED])
- ...
```

Each finding: one fact, conclusion, or evidence item. Tag with source file and verification label.

**Minimum threshold**: 3 distinct findings required. Below 3: warn user, offer to proceed with reduced funnel or suggest `/research` for additional material (EC-02).

### 2. Argument Candidate Generation (FR-02)

Generate 8 root argument candidates from findings inventory:
- Each candidate: single declarative sentence (thesis statement)
- Candidates must be distinct (no paraphrases)
- Draw from different angles in the findings inventory

### 3. Magnet Rule Filter (FR-03, IG-07)

For each candidate, verify it connects to at least one listener motivator:
- Gaining an advantage others lack
- Reducing a risk currently carried
- Saving a resource currently wasted
- Gaining access otherwise unavailable

Eliminate candidates that don't hit a magnet. If all 8 eliminated: generate 4 additional candidates with explicit magnet prompting. If still all fail: report to user (EC-01).

### 4. Argument Selection (FR-03, IG-05)

Score remaining candidates against criteria (default weights):
- **Goal Alignment** (30%): Does it serve the article's stated purpose?
- **Supportability** (30%): Can we prove it from existing findings?
- **Impact** (25%): Does it matter to the reader?
- **Specificity** (15%): Is it precise enough to be falsifiable?

If user provided custom criteria or goals: override or extend defaults.

Select top 3 by composite score. Document rationale per candidate.

### 5. Question Development (FR-04, IG-06)

For each of the 3 selected arguments, generate 5 questions the reader would ask.

Score each question on two dimensions:
- **Impact** (1-3): High = urgency or measurable gain; Medium = credibility or proof; Low = descriptive only
- **Type**: Classify as Why (motivation, pain), How (mechanism, proof), What (scope, features), or other (investigation, evaluation, comparison)

Select top 3 questions. Order by one of Minto's four logical methods:
- **Comparative** (default for persuasion): highest-impact first, typically Why > How > What
- **Chronological**: cause-effect sequence (investigation, root-cause analysis)
- **Structural**: one question per division of the subject

Tiebreaker: the question with higher Impact score wins.

Excess candidates (4th, 5th) become drill-down material for `/write-minto`.

### 6. One-Argument Test (FR-11)

For each candidate's tree, ask: "Can I collapse this into ONE question with three answers?"
- If yes: restructure to single powerful question with deeper evidence
- If no: keep multi-question structure

Document result per candidate: "One-Argument Test: passed" or "One-Argument Test: collapsed to 1Q"

If all 3 candidates collapse to identical structures: keep highest-scoring, regenerate 2 different candidates (EC-03).

### 7. Answer Development (FR-05)

For each selected question in each candidate:
- Generate 5 candidate answers
- Select top 3 based on: evidence strength (traceable to inventory), clarity (single declarative statement), independence (no overlap)

Assemble complete AMINTON Root Section per candidate.

### 8. Draft Output (FR-06)

Mark highest-scoring argument as `[RECOMMENDED]`.

Write `__MINTO-DRAFT_[Article].md` with structure:

```markdown
# Minto Draft: [Article Title]

**Generated**: YYYY-MM-DD HH:MM
**Source material**: [list of files read]

## Findings Inventory

- F01: [finding] (source: [file], label: [VERIFIED])
- ...

## Selection Criteria

- **Goal Alignment**: [description] (weight: 30%)
- **Supportability**: [description] (weight: 30%)
- **Impact**: [description] (weight: 25%)
- **Specificity**: [description] (weight: 15%)

## Candidate 1 [RECOMMENDED]

Score: goal_alignment=N, supportability=N, impact=N, specificity=N (composite: N.NN)
One-Argument Test: [passed/collapsed]

[AMINTON Root Section tree]

## Candidate 2

[Same structure]

## Candidate 3

[Same structure]
```

Article slug: derived from root argument A, kebab-cased, truncated to 40 chars.

## Quality Gate

- [ ] Exactly 3 candidates present with complete AMINTON Root Sections
- [ ] One candidate marked `[RECOMMENDED]` (highest composite score)
- [ ] Selection criteria documented with rationale
- [ ] Magnet Rule: each A connects to a listener motivator
- [ ] Questions follow a stated logical ordering (MINTO-AQ-02)
- [ ] One-Argument Test documented per candidate
- [ ] MECE: questions under same A don't overlap; answers under same Q don't overlap
- [ ] Findings inventory present with source references
- [ ] All answers traceable to findings inventory

## Output

- `__MINTO-DRAFT_[Article].md` in `[SESSION_FOLDER]/` or `[SESSION_FOLDER]/MINTO/`
- Suggest: "Run `/write-minto` to develop full article from recommended argument"
