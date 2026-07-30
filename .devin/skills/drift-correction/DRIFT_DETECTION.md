# Drift Detection Knowledge

Knowledge source for the `/drift-detect` workflow. Contains drift lenses, context detection, DoD extraction rules, and assessment criteria.

## Drift Lenses

Every DoD item belongs to one of two scored categories. Meta-Criteria is observational only.

**Category 1 - Output Structure** (scored, ~high agent compliance):
- File/folder count, names, locations
- Content structure (sections, headers, fields)
- Cross-references, IDs, dependencies
- No placeholders, no truncation

**Category 2 - Process Discipline** (scored, ~low agent compliance):
- Step sequence followed as specified
- Processing depth (thorough, not superficial)
- Gate conditions respected
- Tracking files updated (NOTES, PROGRESS, PROBLEMS)
- Required verifications/tests actually run

**Meta-Criteria** (observational, not scored):
Cognitive behaviors that predict instruction-following quality. Noted for pattern detection, not included in DoD table:
- Prompt Decomposition - compound instructions broken down before acting
- Current/Target Comparison - existing state checked before modifying
- Constraint Re-reading - rules re-read mid-execution, not just at start
- Self-Correction - errors detected and fixed during work
- Backtracking - failing approaches abandoned
- Strategy Justification - WHY stated before major decisions
- Quantitative Completeness - ALL items verified processed, not just "enough"

Meta-criteria observations are noted in the report for user awareness.

**Boundary**: Neither `/drift-detect` nor `/drift-correct` modify FAILS.md or LEARNINGS.md. Only the user triggers `/fail` or `/learn`.

## Context Detection

```
IF SPEC or IMPL or TASKS exist in scope → Code Implementation context
ELIF /deep-research just completed OR _INFO_*_Summary.md exists → Deep Research context
ELSE → Generic context
```

**Precedence**: If both conditions match (e.g., research produced a SPEC), Code Implementation wins. Research-specific checks are skipped.

## Default Sources (all contexts)

Read in order, extract DoD items from each:

1. **Directive** - if user passed `[directive]` after `/drift-detect`, this is the primary focus. Filter all other sources through this lens.
2. **Original instruction** - the user prompt that triggered the work. Primary authoritative source.
3. **Planning artifacts** - any `__STRUT_[TOPIC].md`, `__TASKS_[TOPIC].md`, IMPL docs the agent created.
4. **Target workflow MNF** - process requirements the workflow specified.
5. **FAILS.md scan** - past violations of this topic or workflow (prevent recurrence).

For each source, extract requirements and assign:
- **Priority**: HIGH (missing files/sections, universal FAILS violations), MEDIUM (format, incomplete content), LOW (polish, optional)
- **Category**: 1 (Output Structure) or 2 (Process Discipline)

## Code Implementation Context

**Additional sources** (read BEFORE default sources):

1. **SPEC** - Functional requirements (FR-XX), design decisions (DD-XX), implementation guarantees (IG-XX)
2. **IMPL** - Implementation steps (IS-XX), edge cases (EC-XX), verification checklist (VC-XX)
3. **TASKS** - Work items (TK-XX) with completion status
4. **TEST** - Test cases (TC-XX) and expected results

**DoD extraction:**

- Each FR-XX → DoD item: "Requirement FR-XX implemented" (Category 1, HIGH)
- Each IG-XX → DoD item: "Guarantee IG-XX upheld in code" (Category 1, HIGH)
- Each IS-XX → DoD item: "Step IS-XX executed" (Category 2, MEDIUM)
- Each EC-XX → DoD item: "Edge case EC-XX handled" (Category 1, MEDIUM)
- Each unchecked TK-XX → DoD item: "Task TK-XX completed" (Category 2, HIGH)
- Each TC-XX → DoD item: "Test TC-XX passes" (Category 2, HIGH)
- IMPL verification checklist items → DoD items (Category 2, MEDIUM)

**Category 2 specifics for code:**
- Were tests actually run (not just written)?
- Were tracking files updated after implementation?
- Was `/verify` run after completion?
- Were commit messages created for completed steps?

## Deep Research Context

**Additional sources** (read BEFORE default sources):

1. **DEEP_RESEARCH_RULES.md** - from `@skills:deep-research` skill
2. **STRUT plan** - if `__STRUT_[TOPIC].md` exists, extract unchecked deliverables
3. **Research brief/prompt** - the original research question and scope

**DoD extraction:**

- Each STRUT deliverable → DoD item (Category 1, HIGH if unchecked)
- RULES file requirements → DoD items:
  - Source count thresholds met? (Category 1, HIGH)
  - All sources verified with real URLs? (Category 2, HIGH)
  - Synthesis document complete (no placeholder sections)? (Category 1, HIGH)
  - Multiple perspectives represented? (Category 2, MEDIUM)
  - Contradictions explicitly addressed? (Category 2, MEDIUM)

**Category 2 specifics for research:**
- Were sources actually visited (not hallucinated from training data)?
- Was search performed via specified tools (e.g., Playwright for Google)?
- Were findings cross-verified between sources?

## Generic Context

Build DoD entirely from conversation and planning artifacts (default sources only). No additional sources beyond the defaults.

**DoD extraction:**

- Each explicit deliverable mentioned in user prompt → DoD item (Category 1, HIGH)
- Each file/folder the agent created → DoD item: "matches requested structure" (Category 1, MEDIUM)
- Each workflow step the agent claimed to follow → DoD item: "step actually executed" (Category 2, MEDIUM)
- Each MNF item from target workflow → DoD item (Category 2, HIGH)

**Category 2 specifics for generic:**
- Were tracking files updated (NOTES, PROGRESS, PROBLEMS)?
- Was scope confirmed before acting (not assumed)?
- Were rules re-read before applying (not from memory)?
- Was `/verify` or equivalent quality check run?

## Assessment Statuses

For each DoD item, verify against actual output:

- **PASS** - criterion met
- **FAIL** - not met, fixable now (generates TODO for `/drift-correct`)
- **MISSED** - needed during execution, cannot retroactively fix (e.g., backup before modify, STRUT self-tracking)
- **N/A** - not applicable to this context

## DRIFTS.md Format

Used by `/drift-detect log` mode. Append-only file that accumulates deviations across multiple runs for later heuristic analysis. Structured for pattern detection across sessions.

Format specification is in `@skills:drift-correction` `DRIFTS_TEMPLATE.md`.

**Rules:**
- Append new entries at the end (chronological order, oldest first)
- Never modify or delete previous entries
- One entry per `/drift-detect log` invocation
- If DRIFTS.md does not exist, create with header from template
- Every field matters for analysis - do not skip fields, use "unknown" if uncertain
