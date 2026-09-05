# Workflow Document Rules

Rules for writing workflow documents with GOOD/BAD examples.

**Writing quality:** Apply `APAPALAN_RULES.md` to all workflow content. Key rules for workflows: AP-PR-07 (be specific), AP-BR-02 (sacrifice grammar for brevity), AP-ST-01 (goal first), AP-NM-01 (one name per concept).

## Rule Index

Header (HD)
- WF-HD-01: Frontmatter with description field required
- WF-HD-02: Include Goal and Why after title
- WF-HD-03: Brief description - no AGEN verb references
- WF-HD-04: Scope boundary - clarify what workflow does NOT do (optional)

Structure (ST)
- WF-ST-01: Use GLOBAL-RULES + CONTEXT-SPECIFIC pattern
- WF-ST-02: Steps must be numbered and actionable
- WF-ST-03: Include MUST-NOT-FORGET section
- WF-ST-04: Include Verification section
- WF-ST-05: Include Output format with expected structure
- WF-ST-06: Use Quality Gate for final checklist
- WF-ST-07: Phase and step enumeration starts at 1 with no gaps

References (RF)
- WF-RF-01: Workflow references use inline code: `/verify`
- WF-RF-02: Skill references use @skills: format: `@skills:skill-name`
- WF-RF-03: No hardcoded paths - use placeholders
- WF-RF-04: Cross-references use relative paths from `[AGENT_FOLDER]`
- WF-RF-05: Never replicate rule content from referenced files - reference by ID only (prevents drift and dependency problems)

Content (CT)
- WF-CT-01: Avoid AGEN verbs in prose descriptions
- WF-CT-02: Write out acronyms on first usage
- WF-CT-03: Avoid Markdown tables - use lists
- WF-CT-04: Avoid emojis - use text equivalents
- WF-CT-05: Product names spelled correctly
- WF-CT-06: APAPALAN requires examples - precision over brevity
- WF-CT-07: No Document History section in rule files
- WF-CT-08: Examples use generic placeholders, never real project data, never nonsensical or humorous content
- WF-CT-09: References in skill files only to `[AGENT_FOLDER]`-internal files, never project-specific documents

Execution (EX)
- WF-EX-01: Optimize for autonomous execution - no confirmation gates unless destructive

Branching (BR)
- WF-BR-01: Context branching by document type or mode
- WF-BR-02: Include "No Context Match" fallback
- WF-BR-03: Gate checks use checkbox format
- WF-BR-04: Use Trigger section for invocation patterns

## Table of Contents

- [Frontmatter Format](#frontmatter-format)
- [Header Block](#header-block)
- [MUST-NOT-FORGET Section](#must-not-forget-section)
- [Mandatory Re-read Section](#mandatory-re-read-section)
- [GLOBAL-RULES Section](#global-rules-section)
- [CONTEXT-SPECIFIC Section](#context-specific-section)
- [Steps Format](#steps-format)
- [Phase and Step Enumeration](#phase-and-step-enumeration)
- [Gate Checks](#gate-checks)
- [Stuck Detection](#stuck-detection)
- [Verification Section](#verification-section)
- [Workflow References](#workflow-references)
- [Skill References](#skill-references)
- [Path Placeholders](#path-placeholders)
- [Acronyms](#acronyms)
- [Scope Boundary](#scope-boundary)
- [Output Format](#output-format)
- [Trigger](#trigger)
- [Quality Gate](#quality-gate)
- [Autonomous Execution](#autonomous-execution)

## Frontmatter Format

**BAD:**
```yaml
---
name: verify
type: workflow
---
```

**GOOD:**
```yaml
---
description: Verify work against specs and rules
auto_execution_mode: 1
---
```

## Header Block

Include Goal and Why after title.

**BAD:**
```markdown
# Verify Workflow

Verify work against specs, rules, and quality standards.

## Required Skills
...
```

**GOOD:**
```markdown
# Verify Workflow

Verify work against specs, rules, and quality standards.

**Goal**: Validated work with all issues identified and labeled

**Why**: Prevents shipping bugs, spec violations, and rule breaks

## Required Skills
...
```

## MUST-NOT-FORGET Section

Simple list of critical items. No subheadings or explanations.

**BAD:**
```markdown
## MUST-NOT-FORGET

### Critical Rules
The following rules must be followed:

1. **Rule 1**: Prerequisites ensure required documents exist
   - This is important because...
   
2. **Rule 2**: Run verification after completion
   - Verification catches issues early...
```

**GOOD:**
```markdown
## MUST-NOT-FORGET

- Prerequisites ensure required documents (SPEC, IMPL, TEST) exist
- GLOBAL-RULES apply BEFORE any code change
- Impact Assessment is MANDATORY before implementation
- Run `/verify` after implementation complete
```

## Mandatory Re-read Section

Branch by mode, list documents to re-read.

**BAD:**
```markdown
## Context Refresh

Before starting, you should read relevant documents based on the current mode.
In session mode, read session documents. In project mode, read project documents.
```

**GOOD:**
```markdown
## Mandatory Re-read

SESSION-MODE: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

PROJECT-MODE: README.md, !NOTES.md, FAILS.md
```

## GLOBAL-RULES Section

Universal rules that apply before context-specific steps.

**BAD:**
```markdown
## Rules

- Do impact assessment
- Check scope
- Various other rules that may or may not apply
```

**GOOD:**
```markdown
## GLOBAL-RULES

Apply to ALL contexts before any context-specific steps.

1. Trace scope - identify all affected artifacts
2. Assess impact - what depends on changes
3. Define verification - checkpoints to catch regressions
```

## CONTEXT-SPECIFIC Section

Use H1 for section, H2 for contexts. Include fallback.

**BAD:**
```markdown
## When IMPL exists

Do these steps...

## When SPEC exists

Do other steps...
```

**GOOD:**
```markdown
# CONTEXT-SPECIFIC

## IMPL exists

1. Read IMPL plan
2. Execute steps in order
3. Run tests after each step

## SPEC only (no IMPL)

1. Run `/write-impl-plan` first
2. Then proceed with IMPL steps

## No Context Match

1. Ask user for clarification
```

## Steps Format

Numbered, actionable, concise.

**BAD:**
```markdown
## Workflow

First, you should analyze the context to understand what documents exist.
Then, you need to gather the relevant input by reading the documents.
After that, execute the main action of the workflow.
Finally, write the output to the appropriate location.
```

**GOOD:**
```markdown
## Steps

1. Detect context (INFO, SPEC, IMPL, Code, TEST)
2. Read GLOBAL-RULES section
3. Read relevant CONTEXT-SPECIFIC section
4. Execute steps
5. Run `/verify`
```

## Phase and Step Enumeration

Phases and top-level steps start at `1` and increase by `1` with no gaps. Do not use `Phase 0` / `Step 0` to mean "pre-flight" — pre-flight work is Phase 1. Do not skip numbers when reordering.

**BAD:**
```markdown
## Phase 0: Pre-Flight Checks
...
## Phase 1: Capture
...
## Phase 3: Update
```

**GOOD:**
```markdown
## Phase 1: Pre-Flight Checks
...
## Phase 2: Capture
...
## Phase 3: Update
```

Same rule applies to `Step N`, `Stage N`, `Part N` and any other numbered top-level section type.

**Sub-numbering must be numeric only** (`1.1`, `1.2`, `1.3`). Alphabetic sub-numbering (`1a`, `1b`, `1c`) is **not allowed** because it breaks sortability, does not nest further (no `1a.i`), and mixes numeric and alphabetic scales in one identifier. Sub-numbering starts at `.1` under its parent and increments by 1 with no gaps.

**BAD:**
```markdown
## Phase 2: DOM Extraction

### 2a. Anthropic
### 2b. OpenAI Standard
### 2d. Model ID Resolution
```

**GOOD:**
```markdown
## Phase 2: DOM Extraction

### 2.1 Anthropic
### 2.2 OpenAI Standard
### 2.3 Model ID Resolution
```

## Gate Checks

Checkbox format with Pass/Fail actions.

**BAD:**
```markdown
## Transition Check

Before moving to the next phase, ensure:
- All steps are implemented
- Tests pass
- No TODOs remain

If all conditions are met, proceed. Otherwise, continue working.
```

**GOOD:**
```markdown
## Gate Check: IMPLEMENT→COMPLETE

- [ ] All steps from IMPL plan implemented
- [ ] Tests pass
- [ ] No TODO/FIXME left unaddressed

Pass: Run `/verify` | Fail: Continue implementing
```

## Stuck Detection

Clear threshold and actions.

**BAD:**
```markdown
## If Things Go Wrong

If you encounter problems, try to fix them. If you can't fix them,
ask for help or document the issue somewhere.
```

**GOOD:**
```markdown
## Stuck Detection

If 3 consecutive attempts fail:
1. Document in PROBLEMS.md
2. Ask user for guidance
3. Either get guidance or defer and continue
```

## Verification Section

Reference `/verify` with specific checks.

**BAD:**
```markdown
## Final Steps

Make sure everything is correct before finishing.
```

**GOOD:**
```markdown
## Verification

Run `/verify` to check:
1. All steps completed
2. Output matches expected format
3. MNF items addressed
```

## Workflow References

Use inline code format with slash prefix.

**BAD:**
```markdown
Run the verify workflow after completion.
See the implement workflow for details.
```

**GOOD:**
```markdown
Run `/verify` after completion.
See `/implement` for details.
```

## Skill References

Use @ format with skill name.

**BAD:**
```markdown
Read the coding conventions skill for Python rules.
Use write-documents for templates.
```

**GOOD:**
```markdown
Read @coding-conventions for Python rules.
Use @write-documents for templates.
```

## No Content Replication

Never copy rule descriptions, examples, or checklists from a referenced file. Reference by file + rule ID. If the source changes, replicas drift silently.

**BAD** (replicates rule content - creates maintenance dependency):
```markdown
Effective Writing (see APAPALAN_RULES.md)
- AP-CM-01: Accountable commitments - every commitment states action, deliverable, and timing
- AP-CM-02: Labeled questions and requests - own paragraph, blank-line separated, labeled
- AP-CM-03: Time precision - weekday + ISO date, timezone when scheduling
```

**GOOD** (reference only):
```markdown
Effective Writing - see `APAPALAN_RULES.md` Communication (CM) section: AP-CM-01, AP-CM-02, AP-CM-03
```

**GOOD** (in MNF or workflow steps - ID-only reference):
```markdown
- AP-CM-01, AP-CM-02, AP-CM-03 apply to every draft
- Verify against Anti-Pattern Index in `CONVERSATION_HUMANIZING_RULES.md`
```

## Path Placeholders

Never hardcode paths.

**BAD:**
```markdown
Output to `E:\Dev\IPPS\_Sessions\current\output.md`
Read from `.devin/skills/pdf-tools/`
```

**GOOD:**
```markdown
Output to `[SESSION_FOLDER]/output.md`
Read from `[AGENT_FOLDER]/skills/pdf-tools/`
```

**Standard placeholders:**
- `[WORKSPACE_FOLDER]` - Workspace root
- `[PROJECT_FOLDER]` - Project root (monorepo)
- `[SESSION_FOLDER]` - Current session folder
- `[AGENT_FOLDER]` - `.devin/` or `.claude/`
- `[DEVSYSTEM_FOLDER]` - Current DevSystem version

## Acronyms

Write out on first usage.

**BAD:**
```markdown
Check MNF items before completing.
Run VCRIV pipeline for quality.
```

**GOOD:**
```markdown
Check MUST-NOT-FORGET (MNF) items before completing.
Run Verify-Critique-Reconcile-Implement-Verify (VCRIV) pipeline for quality.
Run Fact-check-Reconcile-Implement-Verify (FACRIV) pipeline for factual verification.
```

## Scope Boundary

One line clarifying what workflow does NOT do.

**BAD:**
```markdown
This workflow finds assumptions and logic flaws. It does not check formatting.
Use /verify for convention compliance. There is no overlap between these workflows.
```

**GOOD:**
```markdown
Scope: Logic flaws only. Use `/verify` for conventions.
```

## Output Format

Show expected output structure inline.

**BAD:**
```markdown
## Output

**After building sequence (Step 1):**
**Executed**: [item description]
**Result**: [OK/FAIL]
**Remaining**: [count] items
```

**GOOD:**
```markdown
## Output

`Executed: [item] | Result: OK/FAIL | Remaining: [N]`
```

## Trigger

How workflow is invoked.

**BAD:**
```markdown
## When to Use

This workflow can be triggered when the user reports a failure,
or when the agent suspects something might be wrong.
```

**GOOD:**
```markdown
## Trigger

- `/fail [description]` - User reports failure
- `/fail` - Agent detects issue
```

## Quality Gate

Final checklist before completion.

**BAD:**
```markdown
## Final Checklist

Before completing, you should verify that:
- The workflow rules were re-read
- Findings were included in entry
- Severity was correctly classified
```

**GOOD:**
```markdown
## Quality Gate

- [ ] Rules re-read
- [ ] Findings documented
- [ ] Severity classified
```

## Generic Examples

Examples in workflows must use generic placeholders or fictional names. Never reference real project filenames, session names, failure IDs, or user-specific content. Workflows are reusable across projects.

Never use nonsensical, whimsical, or humorous examples. LLMs interpret playful content as a quality signal and will reproduce the tone in output. All examples must be professional and instructive.

**BAD** (real project data):
```markdown
- Example: scope `_INFO_DIGLDR_10-BENCHMARKS.md` → `_INFO_DIGLDR_10-BENCHMARKS_DEFERRED_IMPROVEMENTS.md`
```

**BAD** (nonsensical/humorous):
```markdown
Q1: Why should pigs be kept as pets?
  Q1A1: They are beautiful.
  Q1A2: They could be bred to fascinating variations.
```

**GOOD** (generic, professional):
```markdown
- Example: scope `_INFO_CRAWLER_SOURCES.md` → `_INFO_CRAWLER_SOURCES_DEFERRED_IMPROVEMENTS.md`
```

## Autonomous Execution

Workflows must execute without unnecessary pauses. Only request confirmation for destructive or ambiguous actions.

**Destructive** (confirmation required): renaming files, deleting content, overwriting user data, sending emails.

**Ambiguous** (confirmation required): multiple candidates and no way to determine correct one.

**Non-destructive** (no confirmation): creating new files, extracting data, reading context, populating templates, setting defaults. User can review and edit output after.

**BAD:**
```markdown
## Step 2: Extract Data

Extract contact information from chat context.

Present extracted data to user for confirmation before proceeding.

## Step 3: Read Variables

Read translation settings from NOTES.md.

Present the values to the user for confirmation.

## Step 4: Create File

Create the output file.
```

**GOOD:**
```markdown
## Step 2: Extract Data

Extract contact information from chat context.
Proceed directly to file creation. User can review and edit after.

## Step 3: Read Variables

Read translation settings from NOTES.md.
If missing, add with defaults.

## Step 4: Create File

Create the output file.
```

## GRUC Verification (Guides, Rules, Checks)

GRUC documents are skill resource files consumed by LLMs. They have distinct verification requirements from human-facing documents. Detect by: filename pattern `*_GUIDES.md`, `*_RULES.md`, or `*_CHECKS.md` inside a skill folder.

### Branching by GRUC Type

**Guide (`*_GUIDES.md`)** - Strategic decision instructions:
- Numbered decision steps present (not free prose)
- No verification checklists (those belong in `*_RULES.md`)
- Purpose stated in first line (what to read BEFORE doing what)
- References companion `*_RULES.md` for verification
- Each section is actionable (tells agent what to DO, not what to know)

**Rules (`*_RULES.md`)** - Verification criteria with examples:
- Rule Index present at top (all rule IDs listed with one-line descriptions)
- Every non-trivial rule has BAD/GOOD example pair
- Rule IDs use consistent prefix format: `[PREFIX]-[CATEGORY]-[NN]`
- No Document History section (WF-CT-07)
- Rules are testable (can answer yes/no for any given artifact)

**Checks (`*_CHECKS.md`)** - Execution-time verification lists:
- Each check item has: action + evidence + failure indicator
- Checks reference rule IDs they verify
- Ordered by execution sequence (not alphabetical, not by importance)
- Can be consumed as a checklist during workflow execution

### Common GRUC Requirements (all three types)

- No visual-only formatting (no bold for emphasis, no filler phrases) - LLMs cannot see bold
- No Markdown tables - use lists (WF-CT-03)
- No emojis (WF-CT-04)
- Examples use generic placeholders only (WF-CT-08)
- No redundancy with referenced files (`core-conventions.md`, templates, other rule files)
- Self-contained: agent must not need external context beyond referenced companion files (WF-CT-09)
- References point only to files within `[AGENT_FOLDER]` (skills, workflows, rules). Never reference project-specific research (`Docs/`, `_INFO_*.md`), external URLs, or documents outside agent folder hierarchy
- APAPALAN: precise, minimal, goal-first (AP-PR-07, AP-BR-02, AP-ST-01)
- MECT: one name per concept, no synonyms across the document (AP-NM-01)

### GRUC Verification Checklist

- [ ] Correct file type detected (_GUIDE / _RULES / _CHECKS)
- [ ] Type-specific requirements met (see branching above)
- [ ] No visual-only formatting (bold used only in BAD/GOOD labels)
- [ ] No Markdown tables
- [ ] No emojis
- [ ] All examples generic and professional (no project data, no humor)
- [ ] No Document History section
- [ ] No redundancy with companion files or `core-conventions.md`
- [ ] All references point to `[AGENT_FOLDER]`-internal files only (WF-CT-09)
- [ ] APAPALAN/MECT compliance in all content
- [ ] All rule IDs unique and consistently formatted
