# EDIRD Phase Model (Core)

For full model with gates, flows, and planning: invoke @edird-phase-planning skill

**Execution logic**: Execution rules are defined in `devsystem-core.md`.

## Phases

- **EXPLORE** - Understand before acting. [RESEARCH], [ANALYZE], [ASSESS], [SCOPE]
- **DESIGN** - Plan before executing. [PLAN], [DECOMPOSE], [WRITE-SPEC], [PROVE]
- **IMPLEMENT** - Execute the plan. [IMPLEMENT], [TEST], [FIX], [COMMIT]
- **REFINE** - Improve quality. [REVIEW], [VERIFY], [CRITIQUE], [RECONCILE]
- **DELIVER** - Complete and hand off. [VALIDATE], [MERGE], [DEPLOY], [CLOSE]

## Core Principles

- **Gates**: Checklist must pass before phase transition. Gate failures loop within phase.
- **Small cycles**: [IMPLEMENT]→[TEST]→[FIX]→green→next. Never large untestable steps.
- **Retry limits**: COMPLEXITY-LOW: infinite retries (until user stops). COMPLEXITY-MEDIUM/HIGH: max 5 attempts per phase, then [CONSULT].
- **Verb outcomes**: -OK (proceed), -FAIL (handle per verb), -SKIP (intentional).
- **Workflow type**: BUILD (code) or SOLVE (knowledge). Determined in EXPLORE, persists unless switched with [ACTOR] confirmation.
- **Complexity**: LOW=patch, MEDIUM=minor, HIGH=major (maps to semantic versioning).
- **Visual verification**: UI/game/graphics work MUST include visual [PROVE] before full implementation.

## Entry Rule

All workflows start in EXPLORE with [ASSESS] to determine workflow type and complexity/problem-type.

**Gate output is mandatory.** Before each phase transition, agent MUST output explicit gate evaluation (see @edird-phase-planning skill). No self-approval without evidence.

**Artifact verification.** Agent MUST list created artifacts (files) as gate evidence. Claiming "plan complete" without artifact files is gate bypass.

**Research before implementation.** If task requires accuracy to an external system, [RESEARCH] with cited sources is mandatory. Training data assumptions are not research.

**Visual reference for replicas.** Replica/clone work MUST include visual reference (screenshot/video) during EXPLORE, not just text research.

## Gate Summaries

- **EXPLORE→DESIGN**: Problem understood, scope defined, workflow type determined
- **DESIGN→IMPLEMENT**: SPEC, IMPL, TEST docs exist, plan decomposed, risks proven
- **IMPLEMENT→REFINE**: All steps implemented, tests pass, no TODO/FIXME
- **REFINE→DELIVER**: Reviews complete, issues reconciled, ready to merge
- **DELIVER→DONE**: Validated, merged, deployed (if applicable), session closed

## Phase Tracking

- Agent updates NOTES.md with current phase on transition. User adds notes manually.
- Agent maintains full phase plan in PROGRESS.md (phases with status: pending/in_progress/done).

## Planning Notation

Use appropriate notation based on scope:

- **STRUT** - Orchestrate complex multi-phase processes with goals, transitions, and verification
  - When: Multi-phase work, autonomous runs (/go), session-spanning tasks
  - Contains: Phases, Objectives (← linked to Deliverables), Strategy, Steps, Deliverables, Transitions
  - Invoke: @write-documents skill for STRUT_TEMPLATE.md
  - Verify: /verify workflow (STRUT Planning + STRUT Transition contexts)

- **TASKS** - Flat sequential to-do lists with testable buckets
  - When: Single-phase execution, partitioned IMPL steps
  - Contains: Task items with files, done-when criteria, verification commands
  - Created via: [PARTITION] verb from IMPL plan

## Workflow Types

### BUILD (`/build`)

Primary output is working code. Triggers: "Add a feature...", "Build...", "Implement..."

Assessment: COMPLEXITY-LOW / COMPLEXITY-MEDIUM / COMPLEXITY-HIGH

Required documents by complexity:
- **LOW**: Inline plan sufficient, documents optional
- **MEDIUM**: `_SPEC_*.md` + `_IMPL_*.md` required (NO EXCEPTIONS - create files before proceeding)
- **HIGH**: All documents required (`_INFO_*.md`, `_SPEC_*.md`, `_IMPL_*.md`, `_TEST_*.md`)

**Gate enforcement**: DESIGN→IMPLEMENT gate MUST list actual file paths created. If files don't exist, gate fails.

### SOLVE (`/solve`)

Primary output is knowledge, decisions, or documents. Triggers: "Research...", "Evaluate...", "Write...", "Decide..."

Assessment: RESEARCH / ANALYSIS / EVALUATION / WRITING / DECISION / HOTFIX / BUGFIX

Note: HOTFIX/BUGFIX are SOLVE because primary focus is understanding the problem; code fix is secondary.

## Stuck Detection

If no progress after retry limit:
1. [CONSULT] with [ACTOR]
2. Document in PROBLEMS.md
3. Either get guidance or [DEFER] and continue
