# STRUT Template

Template for creating STRUT plans (Structured Thinking notation) that can be embedded in any document.

**Source**: `docs/specs/SPEC_STRUT_STRUCTURED_THINKING.md [STRUT-SP01]`

## When to Use

STRUT plans can be inserted into:
- **PROGRESS.md** - Session progress tracking
- **IMPL documents** - Implementation phase plans
- **TASKS documents** - Task execution plans
- **NOTES.md** - Capturing planned approaches
- Any document where structured planning with progress tracking is needed

## Core Rules

- Every phase, step, deliverable has unique ID: `P1`, `P1-S1`, `P1-D1`
- Steps use AGEN verbs: `[ ] P1-S1 [VERB](params)`
- Checkbox states: `[ ]` pending, `[x]` done, `[N]` done N times (retry count)
- **Objectives link to Deliverables**: `[ ] Goal ← P1-D1, P1-D2`
- Use box-drawing characters: `├─` `└─` `│` `└─>`
- IDs are unique within a STRUT plan (ephemeral, session-scoped)
- Verify STRUT plans via /verify workflow (Planning + Transition contexts)

## Phase Template

```
[ ] P1 [PHASE-NAME]: Description
├─ Objectives:
│   ├─ [ ] Goal 1 ← P1-D1, P1-D2
│   └─ [ ] Goal 2 ← P1-D3
├─ Strategy: Approach description (may include AWT estimate)
│   - Model: Claude Opus for analysis and implementation, Sonnet for fixes, Haiku for chores
│   - Sub-item if needed
├─ [ ] P1-S1 [VERB](params)
├─ [ ] P1-S2 [VERB](params)
├─ [ ] P1-S3 [VERB](params)
├─ Deliverables:
│   ├─ [ ] P1-D1: Outcome 1
│   └─ [ ] P1-D2: Outcome 2
└─> Transitions:
    - P1-D1, P1-D2 checked → [NEXT-PHASE]
    - Otherwise → P1-S2
```

## ID Formats

- **Phase ID**: `P1`, `P2`, `P3`...
- **Step ID**: `P1-S1`, `P1-S2`, `P2-S1`...
- **Deliverable ID**: `P1-D1`, `P1-D2`, `P2-D1`...

## Node Types

1. **Objectives** - Success criteria linked to Deliverables (`← P1-Dx`), checkboxes, no IDs
2. **Strategy** - Approach summary, may include AWT estimates and model hints
3. **Steps** - Actions using AGEN verbs (flat list with checkboxes and IDs)
4. **Deliverables** - Expected outputs (checkboxes with IDs)
5. **Transitions** - Flow control conditions at phase end

## Model Hints

Strategy sections may include model hints for auto model switching:

```
├─ Strategy: Analyze requirements, design solution
│   - Opus for analysis, Sonnet for implementation
```

**Source:** Model definitions and activity mappings are in `!NOTES.md` under `## Cascade Model Switching`.

Model hints are recommendations - agent decides based on actual task.

## Checkbox States

- `[ ]` - Not done (pending)
- `[x]` - Done (completed once)
- `[N]` - Done N times (e.g., `[2]` = executed twice, for loops/retries)

## Transition Targets

- `[PHASE-NAME]` - Next phase (e.g., `[DESIGN]`, `[IMPLEMENT]`)
- `[CONSULT]` - Escalate to [ACTOR]
- `[END]` - Plan complete

## Concurrent Blocks

Group steps that can run in parallel under a `Concurrent:` virtual step.

### Syntax

```
├─ [ ] P1-S1 [VERB](params)
├─ Concurrent: <strategy explaining why parallel>
│   ├─ [ ] P1-S2 [VERB](params)
│   ├─ [ ] P1-S3 [VERB](params)
│   └─ [ ] P1-S4 [VERB](params)
├─ [ ] P1-S5 [VERB](params)          ← implicit barrier, waits for S2-S4
```

### Rules

- `Concurrent: <strategy>` - Virtual step (no checkbox) describing parallel group
- Steps inside run concurrently
- First step after Concurrent block is implicit barrier (waits for all)
- Concurrent blocks can nest (discouraged beyond 1 level)

### Step Dependencies

Use `← Px-Sy` suffix for explicit dependencies within or after Concurrent blocks.

```
├─ Concurrent: Services layer
│   ├─ [ ] P1-S2 [IMPLEMENT](password hashing)
│   ├─ [ ] P1-S3 [IMPLEMENT](JWT tokens) ← P1-S2
│   └─ [ ] P1-S4 [IMPLEMENT](email service)
├─ [ ] P1-S5 [IMPLEMENT](login endpoint) ← P1-S2, P1-S3
```

**Dependency syntax:**
- `← P1-S2` - Wait only for S2 (starts when S2 completes)
- `← P1-S2, P1-S3` - Wait for S2 AND S3
- No arrow after Concurrent block = wait for ALL steps in block
- No arrow within Concurrent block = no dependencies (truly parallel)

### Example: Auth System with Mixed Dependencies

```
[ ] P1 [IMPLEMENT]: Build auth system
├─ [ ] P1-S1 [IMPLEMENT](User model)
├─ Concurrent: Independent services, build in parallel
│   ├─ [ ] P1-S2 [IMPLEMENT](password hashing)
│   ├─ [ ] P1-S3 [IMPLEMENT](JWT tokens) ← P1-S2
│   └─ [ ] P1-S4 [IMPLEMENT](email service)
├─ [ ] P1-S5 [IMPLEMENT](login endpoint) ← P1-S2, P1-S3
├─ [ ] P1-S6 [IMPLEMENT](register endpoint) ← P1-S4, P1-S5
├─ [ ] P1-S7 [TEST]
```

**Execution order:**
1. S1 runs first (sequential)
2. S2, S4 start concurrently (S3 waits for S2)
3. S3 starts when S2 completes
4. S5 starts when S2 AND S3 complete (S4 may still be running)
5. S6 starts when S4 AND S5 complete
6. S7 starts when S6 completes (default sequential)

## Example: Simple Hotfix

```
[ ] P1 [IMPLEMENT]: Fix and verify
├─ Objectives:
│   └─ [ ] Bug no longer reproduces ← P1-D2, P1-D3
├─ Strategy: Locate bug, apply minimal fix, test, commit
├─ [ ] P1-S1 [ANALYZE](stack trace)
├─ [ ] P1-S2 [IMPLEMENT](null check fix)
├─ [ ] P1-S3 [TEST]
├─ [ ] P1-S4 [FIX](if tests fail)
├─ [ ] P1-S5 [COMMIT]("fix: null check in getUserById")
├─ Deliverables:
│   ├─ [ ] P1-D1: Root cause identified
│   ├─ [ ] P1-D2: Fix implemented
│   ├─ [ ] P1-D3: Tests pass
│   └─ [ ] P1-D4: Committed
└─> Transitions:
    - P1-D1 - P1-D4 checked → [END]
    - Tests fail after 3 attempts → [CONSULT]
```

## Example: Multi-Phase Feature

```
[ ] P1 [EXPLORE]: Understand requirements
├─ Objectives:
│   ├─ [ ] Know what to build ← P1-D3
│   └─ [ ] Assess complexity ← P1-D1, P1-D2
├─ Strategy: Ready for design in 5min AWT
├─ [ ] P1-S1 [GATHER](requirements from ticket)
├─ [ ] P1-S2 [ANALYZE](existing code)
├─ [ ] P1-S3 [ASSESS](complexity)
├─ Deliverables:
│   ├─ [ ] P1-D1: Workflow = BUILD
│   ├─ [ ] P1-D2: Complexity determined
│   └─ [ ] P1-D3: Requirements list
└─> Transitions:
    - P1-D1 - P1-D3 checked → P2 [DESIGN]

[ ] P2 [DESIGN]: Plan implementation
├─ Objectives:
│   └─ [ ] SPEC, IMPL, TEST ready ← P2-D1, P2-D2, P2-D3
├─ Strategy: TBD based on P1 findings
├─ [ ] P2-S1 [WRITE-SPEC]
├─ [ ] P2-S2 [WRITE-IMPL-PLAN]
├─ [ ] P2-S3 [WRITE-TEST-PLAN]
├─ Deliverables:
│   ├─ [ ] P2-D1: SPEC created
│   ├─ [ ] P2-D2: IMPL plan created
│   └─ [ ] P2-D3: TEST plan created
└─> Transitions:
    - P2-D1 - P2-D3 checked → P3 [IMPLEMENT]
```

## Example: Research Task (Single Phase)

```
[ ] P1 [EXPLORE]: Research OAuth providers
├─ Objectives:
│   ├─ [ ] Understand OAuth landscape ← P1-D1, P1-D2, P1-D3
│   └─ [ ] Make recommendation ← P1-D4
├─ Strategy: Gather, research, define criteria, evaluate, recommend
├─ [ ] P1-S1 [GATHER](provider list)
├─ [ ] P1-S2 [RESEARCH](Auth0, Okta, Firebase)
├─ [ ] P1-S3 [DEFINE](criteria: price, docs, SDKs)
├─ [ ] P1-S4 [EVALUATE](each provider)
├─ [ ] P1-S5 [RECOMMEND](winner)
├─ Deliverables:
│   ├─ [ ] P1-D1: Providers identified
│   ├─ [ ] P1-D2: Criteria defined
│   └─ [ ] P1-D3: Recommendation made
└─> Transitions:
    - P1-D1 - P1-D3 checked → [END]
```

## Usage

**Creating:** Phase header → Objectives → Strategy → Steps → Deliverables → Transitions

**Executing:** Start at P1-S1, execute steps, check Deliverables, follow Transitions until `[END]`

**Resuming:** Find first unchecked Deliverable, read Strategy, continue

## Embedding in Documents

When inserting STRUT into documents:
1. Add under a section heading (e.g., `## Plan`, `## Phase Plan`)
2. Maintain existing document structure
3. STRUT IDs are local to the plan (not TDID system)
