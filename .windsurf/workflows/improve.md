---
description: Find and fix contradictions, inconsistencies, and improvement opportunities
auto_execution_mode: 1
---

# Improve Workflow

Autonomous self-improvement in four phases: scan with pre-flight research, fix violations, focus on one proven improvement, polish expression. Each run improves ONE thing exhaustively. Run multiple times for multiple improvements.

**Goal**: Proven, justified improvements - one at a time

**Why**: Breadth-first improvement produces half-baked, assumed, untested changes. Depth-first improvement proves each change is justified before applying. Phase 1 scans and researches to find where improvements are possible. Phase 2 fixes rule violations immediately. Phase 3 selects ONE improvement, researches exhaustively, proves justification. Phase 4 polishes expression with APAPALAN (As Precise As Possible, As Little As Necessary) / MECT (Minimal Explicit Consistent Terminology).

## Required Skills

- @skills:write-documents for APAPALAN_RULES, MECT_WRITING_RULES, templates, rules
- @skills:coding-conventions for MECT_CODING_RULES
- @skills:deep-research for research enrichment techniques

## MUST-NOT-FORGET

- **Depth over breadth** - Improve ONE thing exhaustively and prove it justified, not a large list of half-baked, assumed, untested improvements
- **STRUT self-tracking** - Create STRUT plan at start via `/write-strut`, track progress, delete STRUT file after completion
- Phase 1 (scan) → Phase 2 (fix violations) → Phase 3 (focused improvement) → Phase 4 (polish) - strict order
- Rule violations (Phase 2) are corrections, not improvements - apply immediately without pragmatic filter
- Phase 3 selects ONE improvement candidate, researches exhaustively, proves justification before applying
- Remaining candidates → log for next run (not lost, not applied without proof)
- Re-read context-specific templates and rules before assessing (see Phase 1 reads per context)
- Preserve existing IDs (FR-XX, NFR-XX, DD-XX, IS-XX, TC-XX, TK-XX, etc.)
- Never replicate `/verify` (rule-based formal verification) or `/critique` (logic flaw detection)
- Research enrichment adds value through new evidence, not fault-finding
- **Versioned backups** - Backup scoped files to `_vN` before modifying. Never delete backups - only user may delete them

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: README.md, !NOTES.md or NOTES.md, FAILS.md, ID-REGISTRY.md

## GLOBAL-RULES

Apply to ALL contexts before any context-specific steps.

### Issue Categories (all contexts)

Apply @write-documents `SOCAS_RULES.md` with context-appropriate subset. SOCAS criteria map to these categories:

1. Contradictions (SOCAS-01)
2. Inconsistencies (SOCAS-01)
3. Ambiguities (SOCAS-02)
4. Underspecified behavior (SOCAS-06)
5. Broken dependencies
6. Incorrect/unverified assumptions (SOCAS-10)
7. Flawed logic/thinking (SOCAS-10)
8. Unnecessary complexity (SOCAS-11)
9. New solutions for already solved problems (SOCAS-03)
10. Concept overlap (SOCAS-03)
11. Broken rules

### Pragmatic Filter (Phase 3, applied to selected improvement)

The selected improvement must pass this filter before applying. Answer:

1. **Already addressed?** - Check existing content, code, conversation for coverage
2. **Real risk or theoretical?** - Has this happened in practice, or is it speculative?
3. **Proportionate?** - Does the fix cost more than the risk it mitigates?
4. **Concept count justified?** - If this adds concepts, does the added clarity or coverage outweigh the added complexity?
5. **Simpler alternative?** - Can a comment, constraint, or one-liner replace a structural change?
6. **Proven?** - Is there evidence (research, test, example) that this improvement works, or is it assumed?

**Decision**:
- **APPLY** - passes all 6 questions → apply the improvement
- **DEFER** - fails any question → append to `[DEFERRED_FILE]` with assessment rationale, select next candidate

`[DEFERRED_FILE]` is additive - each run appends, never overwrites. Use reconcile's findings format. Run `/reconcile` on `[DEFERRED_FILE]` for pragmatic review.

### Quality Polish (Phase 4, all contexts)

**APAPALAN** - apply to all written documents and communications:
- **AP-PR-07**: Be specific - replace vague statements with concrete, verifiable ones
- **AP-PR-09**: Consistent patterns - same concept = same format everywhere
- **AP-BR-02**: Cut filler - drop articles, verbose constructions, redundant phrases
- **AP-NM-01**: One name per concept - find and fix synonyms and polysemy
- **AP-NM-05**: Use standard terms - replace invented jargon with established terminology
- **AP-ST-01**: Goal first - reader knows WHY before HOW

**MECT Writing** - apply to written documents:
- **MW-VO-01**: Active voice - actor before action
- **MW-VO-03**: Simplest verb - "review" not "carry out a review"
- **MW-VO-04**: Obligation words - must/must not/should/may, never "shall"
- **MW-WC-01**: Word-level precision - accuracy != precision, simple != simplistic
- **MW-TD-01**: Naming structure - explicit name -> specifiers -> states -> mnemonics
- **MW-HS-01**: Informative headings - state content, not topic
- **MW-DT-01**: Four description lenses - intentional/functional/technical/contextual

**MECT Coding** - apply to code:
- **MC-PR-01**: One name per concept across codebase - no synonyms across layers
- **MC-PR-03**: No meta-words without qualifier - qualify Manager, Service, Handler
- **MC-PR-05**: Error messages state what failed, why, and recovery action
- **MC-PR-06**: Log messages self-contained - each line understandable alone
- **MC-BR-04**: Boolean functions use predicate prefix (is_/has_/can_), not "check_"
- **MC-CO-01**: Corresponding pairs use same word stem (open/close, encode/decode)
- **MC-CO-03**: Convergent naming - same term in URL, payload, variable, log, docs
- **MC-ND-06**: Disambiguate by qualifying, not renaming

### Fix Rules (all contexts)

- Preserve IDs (FR-XX, NFR-XX, DD-XX, IS-XX, TC-XX, TK-XX)
- Pick simplest fix when multiple valid options
- Remove broken refs or add missing targets
- Apply APAPALAN + MECT to all text changes (precision first, then brevity)
- Apply MECT_CODING_RULES to all code changes (naming, logs, errors)

## Cross-Context Techniques

Three generative techniques any branch may invoke. Referenced from context-specific sections rather than duplicated.

1. **Pre-Mortem** (Gary Klein) - Imagine this artifact completed and failed in production/use. Write 5-10 plausible failure causes. For each, add a preventive measure to the artifact.
2. **Walkthrough** (Polson et al.) - Mentally execute the artifact as its intended consumer (user, agent, developer). At each step ask: (a) do I know what to do? (b) will I recognize I did it right? Flag every point that stalls.
3. **Alternative Generation** - For each key decision in the artifact, enumerate 2-3 alternatives not yet considered. Compare trade-offs. Either adopt a better alternative or document why the current choice wins.

# CONTEXT-SPECIFIC

**Persona**: Adversarial Collaborator (Kahneman) - improve through constructive challenge backed by new evidence. Each context applies a domain-specific methodological lens.

Detection: determine context from file naming and content, then apply matching section. Multiple contexts may apply. When scope is a folder, classify each file independently.

## Code

**Lens**: Refactoring Craftsman (Fowler) - make working code more readable, maintainable, and aligned with intent.

**Phase 1**: Research only - code generation is implementation, not improvement.

**Phase 1 research**: Check against @skills:coding-conventions with special focus on logging. Evaluate DRY application only if aligned with SPEC and goal. Search for 1) standardized existing algorithms, 2) tested and proven architectures, 3) community-reported bugs and problems for similar solutions, 4) possible performance issues and corrupted states, 5) better MECT-aligned names. Goals: a) improve code robustness, b) alignment with SPEC and IMPL, c) case coverage and testability, d) reduce moving parts and concepts.

**Phase 4 reads**: `MECT_CODING_RULES.md` (@skills:coding-conventions)

**Specialized issues** (in addition to GLOBAL):
- Duplicated code blocks (rule of three violated)
- Feature envy (method uses another class's data more than its own)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Code Smell Identification** - Walk through scope for Fowler's smells. Prioritize: long methods, large classes, duplication, feature envy, primitive obsession.
2. **Cognitive Complexity Reduction** - For methods with deep nesting or high branching, extract sub-methods, introduce guard clauses, flatten nested ifs.
3. **Extract / Inline / Rename** - Extract method for long blocks, extract variable for complex expressions, inline trivial indirection, rename for intent clarity.
4. **Architectural Boundary Restoration** - For each cross-layer call, verify it respects architecture. Flag upward or skip-layer dependencies. Propose restructuring.
5. **Testability Refactoring** - Find code hard to test (static dependencies, hidden state, tight coupling). Propose refactorings that make it testable.

## SPEC Documents

**Lens**: Scenario-Based Analyst (Sutcliffe/McDermott) - requirements are best discovered by walking concrete scenarios, both positive and negative.

**Phase 1 reads**: `SPEC_RULES.md`, `SPEC_TEMPLATE.md` (@skills:write-documents), source INFO documents

**Phase 1 research**: Search for 1) existing products solving the same problem, 2) established frameworks, 3) tested and proven architectures, 4) implementation patterns. Goals: a) align with industry terminology, b) reduce complexity and integration problems, c) improve SPEC focus and separation of concerns, d) avoid multiplicative design decisions (too many parameter/testing dimensions). Use time-tested, value-proven sources only. Rank sources using SOCAS (Source Evaluation subset).

**Specialized issues** (in addition to GLOBAL):
- Requirements phrased only as happy-path behavior
- No misuse cases or security/abuse scenarios
- Only one stakeholder perspective considered
- Non-functional requirements missing (performance, accessibility, observability)
- Design decisions without rationale or alternatives
- Multiplicative design decisions (too many testing configurations)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Primary Scenario Walkthrough** - Trace main user journey end-to-end. At each step: what data exists, what actions available, what can fail? Gaps become new FR-XX.
2. **Misuse Case Generation** - For each user action, consider malicious or erroneous use: invalid input, privilege escalation, resource exhaustion, race conditions. Map to security requirements.
3. **Stakeholder Viewpoint Rotation** - List all stakeholders (end-user, admin, operator, auditor, integrator, maintainer). For each: "what do I need from this system?" Missing perspectives produce new requirements.
4. **Non-Functional Requirements Generation** - For the system under spec, imagine it at 100x scale, operated by a hostile user, audited by compliance, translated into 5 languages. Each scenario revealing a missing requirement produces a new NFR-XX.
5. **Design Alternatives Generation** - For each DD-XX, add 1-2 alternatives with trade-offs if only one option is listed.

## IMPL Plans

**Lens**: Pre-Mortem Planner (Gary Klein) - prospective hindsight doubles identified risks. Imagine the implementation has already failed, then work backwards.

**Phase 1 reads**: `IMPL_TEMPLATE.md` (@skills:write-documents), source SPEC

**Phase 1 research**: Search for 1) tested and proven architectures, 2) implementation patterns and methodologies, 3) common pitfalls. Goals: a) align with industry terminology, b) use consistent explicit human-readable naming (MECT), c) produce independent and testable units of implementation, d) avoid over-engineering. Check locally against existing codebase and local API code to verify correct function signatures and avoid deprecated API usage.

**Specialized issues** (in addition to GLOBAL):
- Steps ordered by code structure rather than by risk
- No rollback strategy for destructive operations
- Incremental delivery not considered (big-bang integration)
- Hidden dependencies between steps
- Environment/library assumptions not validated before the step that needs them

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Pre-Mortem** - Imagine implementation completed and failed. Write 5-10 plausible failure causes. Add preventive steps earlier in the plan.
2. **Risk-First Ordering** - Identify step with highest uncertainty (unfamiliar API, complex algorithm, external dependency). Move it earlier so failure surfaces cheaply.
3. **Incremental Slicing** - Re-slice so that after each step (or small group) the system is still functional and testable.
4. **Parallelization Discovery** - Map dependencies between IS-XX steps. Identify which could execute concurrently. Propose reorganization into parallel tracks.
5. **Rollback Strategy** - For each state-modifying step (DB migration, config change, deploy): how to detect failure, how to revert, how to verify revert succeeded.

## TEST Plans

**Lens**: Mutation Tester (DeMillo/Lipton/Sayward) - a test suite is good if it can detect injected faults, not just confirm the happy path.

**Phase 1 reads**: `TEST_TEMPLATE.md` (@skills:write-documents), source SPEC + IMPL

**Phase 1 research**: Ensure full test coverage against SPEC requirements. For UI testing, verify Playwright can be used as test framework.

**Specialized issues** (in addition to GLOBAL):
- Tests cover only example inputs, not input classes
- No boundary tests (min, max, min-1, max+1, empty, null)
- Assertions check happy-path output but not side effects or error states
- Missing combinatorial coverage for interacting parameters
- No negative tests (system should reject invalid input)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Boundary Value Analysis** - For each numeric or bounded input, add tests at: min, min+1, max, max-1, zero, negative, empty collection, max-size collection.
2. **Equivalence Partitioning** - Group all possible inputs into equivalence classes (valid, invalid-type, invalid-range, invalid-format). Ensure at least one test per class.
3. **Mental Mutation Testing** - For each condition in code under test, ask: "if I inverted this (`<` to `<=`, `&&` to `||`, `true` to `false`), would any test fail?" If not, add a test that detects the mutation.
4. **Error Guessing** - Based on experience, identify fragile areas: concurrency, timezone handling, Unicode, number precision, retry logic. Add targeted tests.
5. **Negative Test Generation** - For each happy-path TC-XX, create a paired TC-XX that verifies rejection of invalid input.
6. **Pairwise Combinatorial** - For tests with 3+ interacting parameters, use pairwise design to cover all pairs with fewer than full-factorial tests.

## TASKS Plans

**Lens**: Critical Path Analyst (Kelley/Walker) - expose the critical path explicitly, distribute risk, ensure each task delivers standalone value.

**Phase 1 reads**: `TASKS_TEMPLATE.md` (@skills:write-documents), source IMPL + TEST

**Specialized issues** (in addition to GLOBAL):
- Tasks too large for single-session completion
- Dependencies between tasks not explicit (critical path hidden)
- Risk concentrated in one phase (all risky tasks at start or end)
- Tasks mixing implementation and testing concerns
- Parallelization opportunities not flagged

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Task Shrinking** - For each task larger than one session, propose decomposition into 2-3 sub-tasks that each deliver a testable increment.
2. **Critical Path Identification** - Build dependency graph. Identify longest path by effort - this drives delivery. Document explicitly.
3. **Pre-Mortem on Sequence** - Imagine delivery is late. Which task likely slipped? Why? Add buffer, split that task, or move it earlier.
4. **Done-Criteria Strengthening** - For each TK-XX, propose 2-3 measurable completion criteria the current plan does not state (e.g., "API responds within 500ms under 100 RPS" vs "performance acceptable").
5. **Risk Distribution** - Classify each task as high/medium/low risk. Avoid risk clusters and risk end-loading. Reorder or split to distribute.

## Workflows

**Lens**: Cognitive Walkthrough Analyst (Polson/Lewis/Rieman/Wharton) - evaluate a workflow by simulating a new agent attempting each step.

**Phase 1 reads**: `WORKFLOW_RULES.md`, `WORKFLOW_TEMPLATE.md` (@skills:write-documents)

**Phase 1 research**: Search for similar agentic workflows or skills. Evaluate a) missing edge cases, b) more robust, stable, or simplified approaches, c) good ideas to improve usefulness. Avoid overlap with other existing workflows in use. Apply pragmatic principle per finding: Is the improvement introducing enough value?

**Specialized issues** (in addition to GLOBAL):
- Steps requiring unstated context knowledge
- No failure recovery at each step
- Branching logic without explicit conditions for each branch
- Workflow assumes state that prior steps did not establish

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Agent Simulation Walkthrough** - Execute workflow as a fresh agent with no prior context. At each step: (a) do I know what to do? (b) will I recognize success? (c) what if unclear? Flag failures.
2. **FMEA Per Step** - For each step, enumerate failure modes: input missing, tool unavailable, output malformed, dependency broken. Specify detection and recovery for each.
3. **Dry-Run with Edge Inputs** - Simulate with: empty input, conflicting input, missing prerequisite, partial prior execution. Find steps that break.
4. **Vague Verb Concretion** - For each vague verb ("review", "ensure", "handle", "address", "consider"), generate a concrete replacement with verb + object + success criterion.

## Skills

**Lens**: Tacit Knowledge Externalizer (Nonaka/Takeuchi) - convert tacit expert knowledge into explicit instructions a novice agent can execute.

**Phase 1 reads**: `SKILL_RULES.md`, `SKILL_TEMPLATE.md` (@skills:write-documents)

**Phase 1 research**: Search for similar agentic skills or knowledge bases. Evaluate a) missing edge cases, b) more robust, stable, or simplified approaches, c) good ideas to improve usefulness. Avoid overlap with other existing skills in use. Apply pragmatic principle per finding: Is the improvement introducing enough value?

**Specialized issues** (in addition to GLOBAL):
- Skill assumes prior domain knowledge not documented
- Decision points without explicit criteria (expert would "just know")
- Gotchas known to author but not documented
- Intent Lookup entries without corresponding procedure
- Examples covering only the obvious use case

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Intent-to-Action Trace** - For each Intent Lookup entry, trace to action steps. Can a fresh agent execute without loading reference files? If not, promote essential content into SKILL.md.
2. **Gotcha Externalization** - Ask: "what mistakes would a new user make that the author catches instantly?" Document each as a Gotchas entry.
3. **Reference Collapse** - For each "See X.md" in SKILL.md, ask: "would a new agent succeed without reading X.md?" If not, inline the essential 3-5 sentences.
4. **Example Generation from Novice Perspective** - For each primary use case, write the example a new agent would most need. Include edge cases and error handling examples.

## Research Output (INFO Documents)

**Lens**: Evidence-Finding Collaborator (Kahneman) - improve through constructive challenge backed by new evidence. Not fault-finding; evidence-finding.

**Phase 1 reads**: `INFO_TEMPLATE.md` (@skills:write-documents), `RESEARCH_STRATEGY_MEPI.md` or `RESEARCH_STRATEGY_MCPI.md` (@skills:deep-research)

**Specialized issues** (in addition to GLOBAL):
- Sources concentrated on single search engine or database
- All sources in one language when topic has international coverage
- Missing primary sources (only secondary/community tier)
- Stale sources (>12 months for fast-moving topics)
- Claims without verification labels
- Findings marked [ASSUMED] but testable
- Alternative interpretations not considered
- Search queries too narrow (premature narrowing)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Key Assumptions Check** - Extract 3-5 implicit assumptions from findings. For each: is there evidence, or is it assumed?
2. **Query Generalization** - Extract original search queries from source URLs/context. Broaden with synonyms, alternative terminology, related concepts. Compare expanded results against existing source list.
3. **Method Challenge** - Evaluate the research method itself: Was the question decomposed correctly? Were the right source types consulted (web search vs academic databases vs official docs vs code repos)? Was the strategy appropriate (MEPI (Most Effective, Practical, Informative) vs MCPI (Most Complete, Precise, Informative))? If a different method would yield different results, execute it and compare.
4. **Competing Hypothesis Search** - Formulate the strongest alternative explanation not yet considered. Design 2-3 queries that would confirm or deny it.
5. **Alternative Language Search** - Re-search key topics in relevant alternative languages (determine from topic domain).
6. **Citation Chain** - Follow references from existing tier 1-2 sources. Check "cited by" for newer work.
7. **Temporal Freshness** - For sources >6 months old in fast-moving fields, search for superseding content.
8. **Source Validation** - Verify top 5 primary sources still accessible (use Playwright MCP with classic Google search if available).

**Integration**: New findings marked `[IMPROVED]`, challenged claims marked `[CHALLENGED]`. Update Sources section and Document History.

## Translation Output

**Lens**: Back-Translation Critic (Brislin) - evaluate translation quality by checking if meaning survives a round-trip back to source language.

**Phase 1 reads**: `TRANSLATION_RULES.md` (@skills:write-documents), source file (remove `_[LANG]` suffix to find it), NOTES.md for TRANSLATION_TERM_PAIRS

**Phase 1 research**: Evaluate against the 4 quality dimensions (TR-QD-01): accuracy, fluency, style, terminology. Search for domain-specific terminology standards in target language.

**Specialized issues** (in addition to GLOBAL):
- Translationese - source language word order or calques that sound unnatural to native speakers (TR-QD-03)
- Semantic drift - translation says something subtly different from source (TR-QD-02)
- Register inconsistency - formal/informal mixing across sections (TR-QD-04)

**Adversarial Collaborator techniques** (execute in order, skip if not applicable):

1. **Back-Translation Spot Check** - Select 3-5 key passages. Mentally back-translate to source language. If back-translation diverges from original, propose more faithful phrasing.
2. **Native Expression Improvement** - Read as native speaker of target language. Identify translationese (calques, non-idiomatic constructions). Propose natural phrasing preserving meaning.
3. **Term Consistency Audit** - Grep each TRANSLATION_TERM_PAIR across document. Flag inconsistent translations of same source term.

## Problem Solving Approaches

**Phase 1 reads**: PROBLEMS.md, FAILS.md, LEARNINGS.md

**Applies to**: Solution approaches in PROBLEMS.md, PROGRESS.md, session NOTES.md, or conversation context where an approach to solving a problem is described or attempted.

**Specialized issues** (in addition to GLOBAL):
- Steps too large (single failure blocks entire approach)
- Assumptions treated as facts without verification
- No fallback if primary approach fails
- Missing intermediate verification points
- Jumping to implementation before confirming diagnosis
- Optimistic assumptions about environment or dependencies

**Improvement techniques** (apply to solution approaches):

1. **Decompose further** - Break steps that could fail into smaller, independently verifiable sub-steps
2. **Add assumption gates** - Before each step that depends on an assumption, add explicit verification of that assumption
3. **Conservative ordering** - Reorder to execute cheapest/fastest validations first (fail fast, fail cheap)
4. **Add rollback points** - Identify where to revert if a step fails, before executing it
5. **Verify-before-act** - For each action that modifies state, verify the precondition holds first

## No Context Match

1. Apply GLOBAL Issue Categories only (Phase 1 scan)
2. Fix violations (Phase 2)
3. Skip Phase 3 (Focused Improvement) - no context-specific research possible
4. Execute Phase 4 (Quality Polish) only

# EXECUTION

## Setup

1. **Scope**: file path → that file; folder → all .md/code; none → conversation context
2. **Detect context** per file:
   - `_INFO_*` or Sources section with source IDs → Research Output
   - `_SPEC_*` or FR-XX/DD-XX IDs → SPEC Document
   - `_IMPL_*` or IS-XX IDs → IMPL Plan
   - `_TEST_*` or TC-XX IDs → TEST Plan
   - `_TASKS_*` / `__TASKS_*` or TK-XX IDs → TASKS Plan
   - `.py`, `.ps1`, `.js`, `.ts` etc. → Code
   - `*_[LANG].md` or `*_[LANG].srt` with corresponding source file → Translation Output
   - Workflow folder `.md` files → Workflow
   - Skill folder files → Skill
   - Solution approaches in tracking docs → Problem Solving
   - No match → No Context Match
3. **Re-read dependencies**:
   - Rules: `[AGENT_FOLDER]/rules/*.md`
   - Context-specific templates and rules (see Phase 1 reads per context)
   - Writing quality: `APAPALAN_RULES.md` + `MECT_WRITING_RULES.md` (@skills:write-documents)
   - Code quality: `MECT_CODING_RULES.md` (@skills:coding-conventions)
   - Workspace: README, NOTES, ID-REGISTRY, FAILS, LEARNINGS
   - Session: NOTES, PROBLEMS, PROGRESS (if SESSION-MODE)
4. **Derive `[DEFERRED_FILE]`** - Unique per improve chain to enable parallel runs:
   - **Single file**: `<filename_without_ext>_DEFERRED_IMPROVEMENTS.md` in same directory
   - **Folder**: `<foldername>_DEFERRED_IMPROVEMENTS.md` in that folder
   - **Conversation context**: `<session_topic_or_timestamp>_DEFERRED_IMPROVEMENTS.md` in session folder
   - Example: scope `_INFO_CRAWLER_SOURCES.md` → `_INFO_CRAWLER_SOURCES_DEFERRED_IMPROVEMENTS.md`
5. **Create STRUT plan** via `/write-strut` - Track phases 1-4 with checkboxes. Save as `.tmp_STRUT_IMPROVE_<YYYY-MM-DD_HH-MM>.md` in scope folder (or session folder in SESSION-MODE).
6. **Backup scoped files** - Before any modification, create versioned backups:
   - **Detect version**: Find highest existing `_vN` backup for each file. No backups → N=0.
   - **Backup**: Copy each scoped file to `<name>_vN.<ext>` in same directory.
   - Documents: `_SPEC_CRAWLER.md` → `_SPEC_CRAWLER_v0.md`
   - Code: `src/utils/auth.py` → `src/utils/auth_v0.py`
   - Subsequent runs increment: `_v1`, `_v2`, etc.
   - **Working file keeps original filename** - all improvements go to original path. Imports, references, and tests work without changes.
   - **Never delete `_vN` backups** - only user may delete them.

## Phase 1: Pre-flight Scan + Research

Lightweight pass to discover what CAN be improved and how easily.

1. **Scan** - Apply GLOBAL Issue Categories (SOCAS) + context-specific specialized issues. Classify each finding as:
   - **Rule violation** - Broken ref, ID error, SOCAS violation, formatting issue → bucket for Phase 2
   - **Improvement candidate** - Enrichment opportunity requiring research → bucket for Phase 3
2. **Pre-flight research** - Execute context-specific Phase 1 research (see each context section) to understand effort and impact of each improvement candidate. Code: research only, no generation.
3. **Rank candidates** - Order improvement candidates by impact-to-effort ratio based on research findings. Each candidate gets a one-line summary: what, why, estimated effort.

**Output**: Two lists - rule violations (Phase 2) and ranked improvement candidates (Phase 3).

### Gate: Phase 1 → Phase 2

- [ ] All files in scope scanned
- [ ] Rule violations separated from improvement candidates
- [ ] Pre-flight research completed for improvement candidates
- [ ] Candidates ranked by impact-to-effort ratio

Pass: Proceed to Phase 2 | Fail: Continue Phase 1

## Phase 2: Fix Violations

Apply rule violations immediately. These are corrections, not improvements - no pragmatic filter needed.

1. **Fix plan** - CRITICAL first, then HIGH, group related fixes
2. **Execute fixes** - Apply corrections, preserve IDs
3. **Verify** - Re-read fixed output, check for regressions

### Gate: Phase 2 → Phase 3

- [ ] All rule violations fixed
- [ ] No regressions from fixes
- [ ] IDs preserved

Pass: Proceed to Phase 3 | Fail: Continue Phase 2

## Phase 3: Focused Improvement

Select ONE improvement. Research exhaustively. Prove justification. Apply or defer.

1. **Select** - Pick highest-ranked candidate from Phase 1. If previous `[DEFERRED_FILE]` exists, check it to avoid re-proposing deferred items.
2. **Deep research** - Execute context-specific Adversarial Collaborator techniques for the selected improvement only. Gather evidence: web research, local codebase analysis, examples, tests.
3. **Pragmatic filter** - Run the 6 pragmatic questions (see GLOBAL-RULES). Requires evidence for question 6 (Proven?).
4. **Decision**:
   - **APPLY** - passes all 6 questions → apply the improvement, update Document History
   - **DEFER** - fails any question → append to `[DEFERRED_FILE]` with assessment rationale, select next candidate (repeat from step 1)
5. **Log remaining** - Unprocessed candidates → append to `[DEFERRED_FILE]` for next run

### Gate: Phase 3 → Phase 4

- [ ] ONE improvement selected and researched exhaustively
- [ ] Pragmatic filter applied with evidence
- [ ] APPLY decision has proof, not assumption
- [ ] Remaining candidates logged for next run

Pass: Proceed to Phase 4 | Fail: Continue Phase 3

## Phase 4: Quality Polish

Apply APAPALAN + MECT to all changes made in Phase 2 and Phase 3.

1. **Polish** - Apply Quality Polish rules (see GLOBAL-RULES) to all modified text and code
2. **Verify** - Re-read polished output, check for regressions
3. **Update Document History** - Summarize all changes (violations fixed + improvement applied)

## Evaluation

After Phase 4, compare working file against its `_vN` backup:
- **Documents**: Diff working file vs `_vN`. Run SOCAS on both. Improved version must not score worse.
- **Code**: Run tests on working file. Compare results against `_vN`. No new failures allowed.
- **If degraded**: Revert by copying `_vN` back to working filename. Log failed improvement to `[DEFERRED_FILE]` with "caused regression" rationale.

## Stuck Detection

If 3 consecutive fix attempts cause regressions:
1. Revert from `_vN` backup to working filename
2. Document in PROBLEMS.md
3. Ask user for guidance

# FINALIZATION

## Quality Gate

- [ ] All rule violations fixed (Phase 2)
- [ ] ONE improvement applied with proof of justification (Phase 3), or all candidates deferred
- [ ] IDs preserved (no broken FR-XX, NFR-XX, DD-XX, IS-XX, TC-XX references)
- [ ] No regressions vs `_vN` backup (Evaluation passed)
- [ ] APAPALAN/MECT compliance in all modified text (Phase 4)
- [ ] STRUT plan checkboxes all checked

## Cleanup

1. Delete `.tmp_STRUT_IMPROVE_<timestamp>.md` - plan is complete
2. Keep all `_vN` backups - only user may delete them
3. If `[DEFERRED_FILE]` has entries, suggest `/reconcile` for pragmatic review

## Output

- Modified files in place (original filenames, newest version)
- `_vN` backups preserved for comparison and rollback
- Document History updated with improvement summary
- `[DEFERRED_FILE]` with remaining candidates (if any)
- PROBLEMS.md updated if stuck or regression occurred

## Verification

Run `/verify` to check:
1. All phases completed (STRUT checkboxes)
2. Versioned backups exist for all modified files
3. No regressions vs `_vN` backup
4. APAPALAN/MECT compliance in modified text
5. MNF items addressed
