# DRIFTS.md Template

Template for the drift log file created by `/drift-detect log`. Each entry captures enough context for pattern detection and heuristic development.

## File Header (create once)

```markdown
# Drift Log

Append-only log of agent drift deviations. Used to discover patterns, develop heuristics, and improve instruction design.

**Analysis dimensions**: What drifted, Why it drifted, What correlates with drift
```

## Entry Format (append per invocation)

```markdown
---

## [YYYY-MM-DD HH:MM] [TOPIC]

**Audited workflow**: /workflow-name
**Context**: [Code Implementation | Deep Research | Generic]
**Directive**: [directive or "full audit"]
**Complexity**: [LOW | MEDIUM | HIGH]
**Session phase**: [EXPLORE | DESIGN | IMPLEMENT | REFINE | DELIVER | unknown]
**Instruction length**: [short (<50 words) | medium (50-200 words) | long (>200 words)]

### Deviations

- **[FAIL|MISSED]** Cat [1|2] [Priority] — [Criterion]
  - Source: [document and section where requirement was defined]
  - Requirement depth: [top-level | subsection | inline | implicit]
  - Mentioned in MNF?: [yes | no]
  - Previous FAILS entry?: [none | FAILS-ID]

### Meta-Criteria

- **Present**: [list of observed cognitive behaviors]
- **Absent**: [list of missing cognitive behaviors]

### Execution Context

- **Instruction compound?**: [yes/no] (multiple sub-tasks in one prompt)
- **Sub-task count**: [N] (how many distinct deliverables requested)
- **Rules re-read?**: [yes/no/partial] (agent re-read rules mid-execution)
- **Planning created?**: [yes/no] (agent created STRUT/TASKS/plan before acting)
- **Self-corrected?**: [yes/no] (agent caught and fixed own errors)
- **Quantitative check?**: [yes/no] (agent verified ALL items processed)
- **Conversation length at drift**: [short (<10 msgs) | medium (10-30) | long (>30)]
- **Deviation position**: [early | middle | late] (where in task execution the drift occurred)
```

## Field Definitions

### Requirement Depth

Where the requirement lives in the source document:

- **top-level** - in document title, Goal, or first section heading
- **subsection** - in a nested section (requires scrolling/reading to find)
- **inline** - mentioned within running text, not a dedicated item
- **implicit** - not explicitly stated but expected from conventions or context

### Deviation Position

Where in the task execution timeline the drift occurred:

- **early** - first third of task steps
- **middle** - middle third
- **late** - final third (often: tracking updates, verification, cleanup)

### Execution Context Fields

Observable facts about the execution environment. Collected for correlation analysis - no interpretation needed:

- **Instruction compound / Sub-task count** - factual count of deliverables in prompt
- **Rules re-read** - observable from conversation history (tool calls to read rule files)
- **Planning created** - observable from file creation timestamps
- **Self-corrected** - observable from edit history (agent fixing own output)
- **Quantitative check** - observable from conversation (agent counting items)
- **Conversation length** - proxy for context budget consumption
- **Deviation position** - proxy for budget exhaustion (late = more likely budget-related)

## Analysis Patterns

After accumulating 10+ entries, look for:

1. **Category clusters** - which category drifts most? (expect Cat 2 >> Cat 1)
2. **Workflow clusters** - which workflows produce most drift?
3. **Requirement depth correlation** - do "implicit" and "subsection" requirements drift more?
4. **Execution context correlations** - does "planning created = no" predict Cat 2 drift?
5. **Recurring deviations** - same criterion failing across entries = systemic issue
6. **Complexity correlation** - HIGH complexity = more drift? If so, decompose tasks
7. **Position correlation** - drift concentrated "late"? Suggests budget exhaustion
8. **Conversation length correlation** - long conversations = more drift? Suggests context limits
9. **MNF effectiveness** - do "Mentioned in MNF = yes" items still drift? MNF design problem

## Example Entry

```markdown
---

## 2026-06-13 14:30 CRWL

**Audited workflow**: /build
**Context**: Code Implementation
**Directive**: full audit
**Complexity**: MEDIUM
**Session phase**: IMPLEMENT
**Instruction length**: medium (50-200 words)

### Deviations

- **FAIL** Cat 1 HIGH — SPEC section 4 acceptance criteria missing
  - Source: CRWL-SP01 section "Functional Requirements"
  - Requirement depth: subsection
  - Mentioned in MNF?: no
  - Previous FAILS entry?: none
- **MISSED** Cat 2 HIGH — /verify not run after implementation
  - Source: /build workflow MNF item 3
  - Requirement depth: top-level
  - Mentioned in MNF?: yes
  - Previous FAILS entry?: GLOB-FL-0012
- **FAIL** Cat 2 MEDIUM — PROGRESS.md not updated after completing step 3
  - Source: SMAP convention (session-management SKILL.md)
  - Requirement depth: implicit
  - Mentioned in MNF?: no
  - Previous FAILS entry?: none

### Meta-Criteria

- **Present**: Strategy Justification, Self-Correction
- **Absent**: Quantitative Completeness, Constraint Re-reading

### Execution Context

- **Instruction compound?**: yes
- **Sub-task count**: 4
- **Rules re-read?**: no
- **Planning created?**: yes
- **Self-corrected?**: yes
- **Quantitative check?**: no
- **Conversation length at drift**: medium (10-30)
- **Deviation position**: late
```
