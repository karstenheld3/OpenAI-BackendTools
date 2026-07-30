---
description: Verify work against specs and rules
auto_execution_mode: 1
---

# Verify Workflow

Verify work against specs, rules, and quality standards.

## Required Skills

Invoke based on context:
- @skills:write-documents for document verification
- @skills:coding-conventions for code verification

**CRITICAL**: Skill invocation returns instructions only. You MUST also read the supporting files listed in skill output (e.g., `PYTHON-RULES.md`, `WORKFLOW-RULES.md`) to get actual verification rules.

## MUST-NOT-FORGET

1. Apply fixes immediately without asking for permission - this workflow has authority to correct issues
2. Re-read session/project documents before verifying (see Mandatory Re-read)
3. Create internal MNF checklist and verify against it in Final Steps
4. Do not verify from memory. Search for applicable rule files, re-read them (mandatory: `core-conventions.md`), and build checklist from source before checking items. Never accept "matches existing style" as passing.

## Mandatory Re-read

**SESSION-MODE** - Re-read session folder documents:
- NOTES.md
- PROBLEMS.md
- PROGRESS.md
- FAILS.md
- LEARNINGS.md (if exists)
- If verifying within a `T##_*` topic folder: also read its tracking files

**PROJECT-MODE** - Re-read workspace-level documents:
- README.md
- !NOTES.md or NOTES.md
- !PROBLEMS.md or PROBLEMS.md (if exists)
- !PROGRESS.md or PROGRESS.md (if exists)
- FAILS.md
- LEARNINGS.md (if exists)

## Workflow

1. First find out what the context is (INFO, SPEC, IMPL, Code, TEST, Session, Workflow, Skill, Conversation, Translation Output)
2. Read GLOBAL-RULES and Verification Labels
3. Read the relevant Context-Specific section
4. Create a verification task list
5. Work through verification task list
6. Run Final Steps

## GLOBAL-RULES

Apply to ALL document types and contexts:

- Avoid excessive acronyms. Write out acronyms on first usage.
  - BAD: `SPN not supported.`
  - GOOD: `Service Principal Name (SPN) not supported.`
- Use verification labels consistently (see below)
- Re-read relevant rules and session files before verifying
- Make internal "MUST-NOT-FORGET" list and check after each step
- If product names are used, make sure there are spelled correctly. Do web research when needed.
  - BAD: Sharepoint -> GOOD: SharePoint
  - BAD: AI Foundry Remote SharePoint -> GOOD: "SharePoint tool" for Azure AI Foundry Agent Service
- **Avoid Markdown tables** - Convert to lists:
  - Tables found? → Convert to unnumbered lists with bold labels
  - Exception: README.md may use tables without `<DevSystem>` tag
  - Only [ACTOR] may add `<DevSystem MarkdownTablesAllowed=true />` exception to other files
  - If tables ARE allowed: verify formatting per `core-conventions.md` (aligned columns with spaces)
- **Avoid emojis** - Remove or replace with text:
  - Emojis found? → Replace with text equivalents (Yes/No/Warning)
  - Exception: README.md may use emojis without `<DevSystem>` tag
  - Only [ACTOR] may add `<DevSystem EmojisAllowed=true />` exception to other files
- **Preserve human-readable formatting** in INFO, SPEC, IMPL documents:
  - Bold for emphasis on key terms, framework names, or important concepts is acceptable
  - The "no bold" rule applies only to LLM-consumed skill resource files (see Skills section)
  - Do not strip formatting that aids human scanning and comprehension
- **Labels decodable at point of use (AP-PR-11)** - Scan for bracket labels with 1-2 characters:
  - Exempt: `[x]`/`[ ]` checkboxes, `[N]` retry counts
  - Exempt: Established system labels: `[ASSUMED]`, `[VERIFIED]`, `[TESTED]`, `[PROVEN]`
  - Short label found? Check: Is a legend visible at every usage point (no scrolling)? If yes: pass. If no: replace with full word or add legend.
  - For labels 3+ characters: apply Reconstruction Test - can the full term be recovered from the short form? If not, flag as opaque abbreviation

## Conceptual verification

When reviewing architecture, design and solution strategy, apply @skills:write-documents `SOCAS_RULES.md` with the Agent Output Review subset. Look for:
- inconsistencies (SOCAS-01)
- ambiguities (SOCAS-02)
- new solutions for already solved problems (SOCAS-03)
- overlapping concerns (SOCAS-03)
- underspecified behavior (SOCAS-06)
- unverified assumptions (SOCAS-10)
- flawed thinking and underestimated complexity (SOCAS-10)
- over-engineering and introduction of unwanted complexity (SOCAS-11)

## Verification Labels

Apply these labels to findings, requirements, and decisions in all document types:

- `[ASSUMED]` - Unverified assumption, needs validation
- `[VERIFIED]` - Finding verified by re-reading source or comparing with other sources
- `[TESTED]` - Tested in POC (Proof-Of-Concept) or minimal test script
- `[PROVEN]` - Proven to work in actual project via implementation or tests

**Usage by document type:**
- INFO: Label key findings and source claims
- SPEC: Label design decisions and assumptions
- IMPL: Label edge case handling and implementation choices
- TEST: Label expected behaviors and test assertions

**Progression:** `[ASSUMED]` → `[VERIFIED]` → `[TESTED]` → `[PROVEN]`

## Final Steps

1. Re-read previous conversation, provided and relevant files
2. Identify de-prioritized or violated instructions
3. Add tasks to verification task list
4. Work through verification task list
5. Verify again against MUST-NOT-FORGET list

# CONTEXT-SPECIFIC

## Deep Research Output (Multi-File Research Set)

Detect by: folder contains `_INFO_[TOPIC]-01_Summary.md` + `_INFO_[TOPIC]-02_Sources.md` + topic files + `__STRUT_[TOPIC].md`.

**Read**: @skills:deep-research `RESEARCH_RULES.md` - contains all RS-*, SC-*, SM-*, TF-*, ST-*, QA-* rules with verification procedure.

Execute the 6-step verification procedure from `RESEARCH_RULES.md`:
1. **Structure Check** (RS-01 through RS-06) - file set completeness
2. **Sources Check** (SC-01 through SC-09) - source collection quality
3. **Summary Check** (SM-01 through SM-11) - summary file quality
4. **Topic Files Check** (TF-01 through TF-10) - per-file quality
5. **STRUT Check** (ST-01 through ST-07) - process execution
6. **Quality Check** (QA-01 through QA-11) - cross-cutting quality

Additionally:
- Verify against @skills:write-documents `APAPALAN_RULES.md` (precision, brevity, structure, naming)
- Verify against @skills:write-documents `MECT_WRITING_RULES.md` (voice, word choice, terminology, headings, lists)

## Information Gathering (INFO)

**Priority 1: Factuality and clarity** (misinterpretation prevention)
- Think first: How would another person approach this? Is scope aligned with problem?
- Verify sources. Read them again and verify or complete findings.
- Drop all sources that can't be found.
- Ask questions that a reader might ask and clarify them.
- Verify against @skills:write-documents `APAPALAN_RULES.md` (precision, brevity, structure, naming)
- Verify against @skills:write-documents `MECT_WRITING_RULES.md` (voice, word choice, terminology, headings, lists)
- Apply conceptual verification (SOCAS) to analysis and conclusions sections

**Priority 2: Document structure** (template compliance)
- Read @skills:write-documents `INFO_RULES.md` and verify against all INFO-* rules
- If research document: verify optional sections positioned per @skills:write-documents `INFO_GUIDE.md`
- Read `[AGENT_FOLDER]/workflows/research.md` again and verify against instructions

## Specifications (SPEC)

- Verify Timeline field is present and accurate (Created date, update count, date range)
- Verify MUST-NOT-FORGET section exists and rules are followed
- Verify against spec requirements and existing code.
- Look for bugs, inconsistencies, contradictions, ambiguities, underspecified behavior.
- Think of corner cases we haven't covered yet.
- Ensure detailed changes/additions plan exists.
- Ensure exhaustive implementation verification checklist at end.
- Verify Document History section exists and is up to date
- Verify UI mockups use Unicode box-drawing characters (SPEC-DG-06: `┌ ├ └ │ ─` not `+ - |`)
- Verify no implementation details in SPEC (SPEC-CT-02): no code snippets, no source file line numbers, no function signatures, no `[VERIFIED: file lines]` tags. Implementation details belong in IMPL.
- Read @skills:write-documents skill again and verify against rules.
- Verify against @skills:write-documents `SPEC_RULES.md` (required for all SPEC documents)
- Verify against @skills:write-documents `APAPALAN_RULES.md` (precision, brevity, structure, naming)
- Verify against @skills:write-documents `MECT_WRITING_RULES.md` (voice, word choice, terminology, headings, lists)

## Implementation Plans (IMPL)

- Verify Timeline field is present and accurate (Created date, update count, date range)
- Verify MUST-NOT-FORGET section exists and rules are followed
- Read spec again and verify against spec.
- Anything forgotten or not implemented as in SPEC?
- Verify Document History section exists and is up to date
- Read @skills:coding-conventions skill again and verify against rules.
- Verify against @skills:write-documents `APAPALAN_RULES.md` (precision, brevity, structure, naming)
- Verify against @skills:write-documents `MECT_WRITING_RULES.md` (voice, word choice, terminology, headings, lists)

## Implementations (Code)

- Read specs and plans again and verify against specs.
- Are there existing tests that we can run to verify?
- Can we do quick one-off tests to verify we did not break things?
- Read @skills:coding-conventions skill again and verify against rules.
- Verify against @skills:coding-conventions `MECT_CODING_RULES.md` (precision, brevity, consistency, naming design, documentation)

**Logging Verification (automatic, language-agnostic):**

If code contains logging, output, or print statements:

1. Read @skills:coding-conventions `LOGGING-RULES.md` (general rules)
2. Identify logging type and read corresponding rules file:
   - User-facing (console, SSE) → `LOGGING-RULES-USER-FACING.md`
     - Goal: Users always know what is happening
   - App-level (server logs, debug) → `LOGGING-RULES-APP-LEVEL.md`
     - Goal: Human-readable AND machine-parseable
   - Script-level (test/QA output) → `LOGGING-RULES-SCRIPT-LEVEL.md`
     - Goal: All failure info in logs alone
3. Verify against core principles:
   - APAPALAN (as precise as possible, as little as necessary)
   - Least Surprise (predictable patterns across solutions)
   - Full Disclosure (each line understandable without context, provides enough to assess complexity + processing time)
   - Visible Structure (logs reveal workflow, not just progress)
   - Announce > Track > Report (three-phase pattern)
4. Verify code against all applicable LOG-* rules

## Testing (TEST)

- Verify Timeline field is present and accurate (Created date, update count, date range)
- Verify MUST-NOT-FORGET section exists and rules are followed
- Verify test strategy matches spec requirements
- Verify against @skills:write-documents `APAPALAN_RULES.md` (precision, brevity, structure, naming)
- Verify against @skills:write-documents `MECT_WRITING_RULES.md` (voice, word choice, terminology, headings, lists)
- Check test priority matrix:
  - MUST TEST: Critical business logic covered?
  - SHOULD TEST: Important workflows included?
  - DROP: Justified reasons for skipping?
- Verify test cases:
  - All edge cases from IMPL plan have corresponding TC-XX
  - Format: Description -> ok=true/false, expected result
  - Grouped by category
- Check test data:
  - Required fixtures defined?
  - Setup/teardown procedures clear?
- Verify test phases:
  - Ordered execution sequence logical?
  - Dependencies between phases documented?
- Cross-check against spec:
  - Every FR-XX has at least one TC-XX
  - Every EC-XX has corresponding test
- Verify Document History section exists and is up to date

## Workflows, Skills, Skill Resource Files

Read the rule file for your context and verify against all rules. Also verify against @skills:write-documents `APAPALAN_RULES.md` and `MECT_WRITING_RULES.md`.

- Workflows → @skills:write-documents `WORKFLOW_RULES.md` (all WF-*), also @skills:coding-conventions `WORKFLOW-RULES.md` (design principles)
- Skills → @skills:write-documents `SKILL_RULES.md` (all SK-*)
  - If SETUP.md exists: verify UNINSTALL.md also exists (not in SK-* rules)
- Skill Resource Files (`*_RULES.md`, `*_GUIDE.md`, `*_CHECKS.md` in skill folders) → @skills:write-documents `WORKFLOW_RULES.md` (applicable WF-*)
  - Verify SK-CT-05: no visual-only formatting (no bold, no filler phrases)
  - Verify SK-CT-06: no Document History section
  - For _RULES: Rule Index present, BAD/GOOD pairs for non-trivial rules
  - For _GUIDE: numbered decision steps, no verification checklists (belongs in _RULES)
  - For _CHECKS: action + evidence + failure indicator per check item
  - No redundancy with referenced files (`core-conventions.md`, templates, other rule files)

## Minto Documents

Detect by: filename pattern `__MINTO-DRAFT_*.md` (draft) or `_MINTO_*.md` (article).

**Read**: @skills:write-documents `MINTO_RULES.md`, `MINTO-DRAFT_TEMPLATE.md`, `MINTO_TEMPLATE.md`

**Verification checklist for Minto Draft (`__MINTO-DRAFT_*`):**
- Structure matches `MINTO-DRAFT_TEMPLATE.md` (MINTO-DS-06):
  - Header block: Generated, Source material, Purpose, Listener, Action
  - Findings Inventory section with Fnn entries (source + label)
  - Selection Criteria section with weights
  - Per candidate: Score, Magnet, One-Argument Test, Question ordering, AMINTON tree, Same Kind check
- Verify against MINTO-DS-* rules (3 candidates, recommended marked, criteria, inventory)
- Verify against MINTO-AQ-* rules (magnet, ordering, one-argument test, declarative answers, same kind)
- Verify against MINTO-ME-* rules (MECE at all levels)

**Verification checklist for Minto Article (`_MINTO_*`):**
- Structure matches `MINTO_TEMPLATE.md` (MINTO-AS-08):
  - Header block: Doc ID, Source, Argument
  - Executive Summary with SCQA (Situation, Complication, Answer)
  - One section per Q with idea-stating heading (not category label)
  - Bold claim per answer, evidence woven into paragraphs
  - Conclusion: one summary line per Q + restated A
  - Appendix: full AMINTON tree (A through E-nodes with source Fnn refs)
- Verify against MINTO-TI-* rules (sub-questions, evidence, no orphans, source references)
- Verify against MINTO-AS-* rules (Doc ID, SCQA Executive Summary, section per Q, appendix, top-down order)
- Verify against MINTO-CL-* rules (closing present, one line per answer, no new claims)
- Verify against MINTO-ME-* rules (MECE at all levels)
- Every prose paragraph maps to an AMINTON node (no unmapped content)

## Translation Output

Detect by: file has `_[LANG]` suffix (e.g., `report_DE.md`, `video_DE.srt`) and a corresponding source file exists, or context indicates this is `/translate` output.

- Read @skills:write-documents `TRANSLATION_RULES.md` and verify against all TR-* rules
- Run Step 5 Phase 1 checks from `/translate` workflow (grep term pairs, native chars, addressing form, structure counts, CJK if applicable)
- Compare source and target: paragraph count, heading count, code block count
- Verify no source language fragments in translated prose (outside code/URLs)

## Session Tracking (NOTES, PROBLEMS, PROGRESS)

**Verify NOTES.md:**
- Session Info complete (Started date, Goal)?
- Key Decisions documented?
- Important Findings recorded?
- Workflows to Run on Resume listed?
- Agent instructions still valid?

**Verify PROBLEMS.md:**
- All discovered issues documented?
- Status marked (Open/Resolved/Deferred)?
- Root cause identified for resolved items?
- Deferred items have justification?
- **Sync check**: Which problems should move to project-level PROBLEMS.md?

**Verify PROGRESS.md:**
- To Do list current?
- Done items marked with [x]?
- Tried But Not Used documented (avoid re-exploring)?
- Test coverage analysis up to date?
- **Sync check**: Which findings should move to project-level docs?

**Session Close Sync Checklist:**
- [ ] Resolved problems with project impact → sync to project PROBLEMS.md
- [ ] Reusable patterns/decisions → sync to project NOTES.md
- [ ] Discovered bugs in unrelated code → create issues or sync to PROBLEMS.md
- [ ] New agent instructions → sync to project rules or NOTES.md

## Conversations

- Read @skills:write-documents `CONVERSATION_RULES.md` and verify against all CV-* rules

**If verifying a conversation DRAFT (email/message written AS user):**

Read all three rule layers and verify in priority order:

1. Read @skills:write-documents `APAPALAN_RULES.md` - verify AP-CM-01, AP-CM-02, AP-CM-03:
   - [ ] Every commitment has action + deliverable + weekday + ISO date + time (AP-CM-01)
   - [ ] Every question in own paragraph, "Question:" label, self-contained (AP-CM-02)
   - [ ] Every request in own paragraph, "Request:" label, explicit timing (AP-CM-02)
   - [ ] All dates: weekday + ISO date. Periods include year. Timezone when scheduling. (AP-CM-03)
2. Read @skills:write-documents `CONVERSATION_HUMANIZING_RULES.md` - verify against Anti-Pattern Index:
   - [ ] Full grammar preserved (no dropped pronouns/articles) - CV-HM-07
   - [ ] Greeting/closing from user's History, not invented or rotated - CV-HM-06
   - [ ] Sentence rhythm varies, no 3+ uniform lengths - CV-HM-05
   - [ ] No LLM vocabulary, no formal connectives in casual context
   - [ ] No translationese - reads as native speaker wrote it - CV-HM-07
   - [ ] No over-humanizing (precision intact) - CV-HM-01
3. Read @skills:write-documents `CONVERSATION_RULES.md` - verify format:
   - [ ] Email header format correct if email - CV-EM-01
   - [ ] Draft marked if unsent - CV-EM-04
   - [ ] Native characters used - CV-TR-03

## STRUT Plans (Planning Phase)

Verify when STRUT plan is created or updated:

- [ ] Every Objective links to at least one Deliverable (`← P1-Dx`)
- [ ] Unlinked Objectives flagged - require [ACTOR] confirmation at transition
- [ ] All Deliverables have clear completion criteria
- [ ] Transitions reference Deliverables (not Objectives)
- [ ] Steps use valid AGEN verbs with `[VERB](params)` format
- [ ] Problem/goal addressed by Objectives?
- [ ] Strategy includes approach summary (AWT estimate optional)

## STRUT Plans (Transition Phase)

Verify before phase transition (when evaluating Transitions):

- [ ] All Deliverables in Transition condition are checked?
- [ ] For each Objective: are ALL linked Deliverables checked?
- [ ] Deliverable evidence supports Objective claim?
- [ ] Unlinked Objectives: [ACTOR] confirmation obtained?
- [ ] Transition target is valid (`[PHASE-NAME]`, `[CONSULT]`, or `[END]`)?

**Objective Verification Rule:**
- Objective is verified when ALL linked Deliverables are checked
- Check Objective checkbox only after confirming linked Deliverables
- If Objective has no links (`←`), require explicit [ACTOR] confirmation
