---
description: Create purpose-built document templates that produce consistent, comparable instances
auto_execution_mode: 1
---

# Write Template Workflow

Create purpose-built document templates that produce consistent, comparable instances.

**Goal**: A TMPL-* compliant template that serves stated goals and produces comparable documents

**Why**: Ad-hoc templates produce inconsistent documents. Structured template creation ensures each instance answers the same questions in the same order, enabling comparison and quality verification.

## Required Skills

- @skills:write-documents for `TEMPLATE_GUIDE.md`, `TEMPLATE_RULES.md`, `APAPALAN_RULES.md`

## MUST-NOT-FORGET

- Template IS the document skeleton, not a description of one (TMPL-ST-01)
- All annotations use XML comments only - no italic, bracket, or prose annotations (TMPL-AN-01)
- Primary and secondary goals must be answerable from every template instance
- Instances must be comparable: same sections, same order, same depth
- Verify against `TEMPLATE_RULES.md` audit checklist before delivering
- Repeatable items show ONE instance only (TMPL-ST-04)
- Complex rules go in companion `*_RULES.md` files, not in the template (TMPL-ST-06)

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: !NOTES.md or NOTES.md, FAILS.md

# EXECUTION

## Phase 1: Collect Context

1. Read conversation history, attached files, and session goals
2. Identify trigger: who needs the template, why, and where it will live
3. Identify domain: what system, workflow, skill, or research area needs this template
4. Check for existing templates in the target domain - reuse or extend before creating new
5. Collect exemplar documents: any existing instances that the template should standardize

## Phase 2: Extract Goals

1. **Primary goal** - single most important question every template instance must answer
2. **Secondary goals** - additional questions each instance should address (2-5 items)
3. **Comparison dimension** - what aspect will instances be compared on (if applicable)
4. Record goals explicitly - they drive all subsequent decisions and become the `**Goal**:` field

## Phase 3: Decompose Prompt

Read @skills:write-documents `TEMPLATE_GUIDE.md` before this phase.

Answer these design questions:

1. **Target audience** - Who fills in this template? Agent during research, agent during implementation, user, workflow step?
2. **Usage context** - When are instances created? During research, during planning, during execution, on-demand?
3. **Exemplar analysis** - If exemplar documents exist from Phase 1 step 5:
   - Extract common sections across all exemplars
   - Identify sections present in some but not all (candidate conditional sections)
   - Note ordering patterns and depth conventions
   - Identify questions answered by exemplars but NOT covered in goals (gap = goal refinement or new section)
   - Derive base section list from the strongest exemplar pattern
4. **Key questions** - What are the most relevant questions each instance must answer or provide information for? Derive from primary/secondary goals and exemplar analysis.
5. **Section design** - Group questions into logical sections. Each section serves one purpose. Start from exemplar-derived base if available.
6. **Section ordering** - Choose order for the target audience:
   - Findings-first: key results at top, details below (research pattern)
   - Process-first: steps in execution order (implementation pattern)
   - Comparison-first: key differentiators first, background later (comparison pattern)
7. **Conditional sections** - Identify sections that apply only in certain contexts
8. **Repeatable sections** - Identify sections that repeat per item (show one instance)
9. **Dynamic components** - Plan the template's active guidance elements:
   - **Conditional markers**: For each conditional section from step 7, draft the insertion criteria: `<!-- Conditional: insert when [specific criteria] -->`
   - **Agent instructions**: At each section, ask: "Will the filling agent know what to put here without extra guidance?" If not, plan an XML comment instruction covering: what content belongs here, expected depth/format, and what to avoid
   - **Full Example**: Include when template has 3+ sections, uses conditional sections, or has complex placeholder patterns. Plan what the filled-in example should demonstrate (TMPL-ST-05)

## Phase 4: Assemble Requirements

Read @skills:write-documents `TEMPLATE_RULES.md`.

1. Determine template category per `TEMPLATE_GUIDE.md` Section 3:
   - Per-task document → Doc ID, Goal, Timeline, Document History required
   - Other template → these fields do not apply
2. Build consolidated requirements list from:
   - Phase 2 goals (primary, secondary, comparison)
   - Phase 3 section design and ordering
   - All applicable TMPL-* rules
   - Domain-specific constraints from Phase 1 context
3. Convert each requirement into a concrete task: "Add [what] to [where] because [why]"

## Phase 5: Construct Template

Write the template file following the skeleton from `TEMPLATE_GUIDE.md` Section 4.

1. Write top comment block if template has naming conventions or lifecycle rules
2. Write title with placeholder: `# [Document Type]: [PLACEHOLDER]`
3. Write header block with required fields (per category from Phase 4)
4. Add Topic ID XML comment after Doc ID if applicable (TMPL-HD-03)
5. Write MUST-NOT-FORGET section if planning document (TMPL-SN-02)
6. Write Table of Contents if 4+ numbered sections (TMPL-SN-03)
7. Write each section:
   - Placeholder content showing expected format and depth
   - XML comment annotations for instructions (TMPL-AN-01)
   - Conditional markers where applicable (TMPL-AN-02)
8. Add Document History section if per-task document (TMPL-SN-01)
9. Add full example at end if template has complex structure (TMPL-ST-05)

## Phase 6: Verify and Refine

1. Run audit checklist from `TEMPLATE_RULES.md`
2. **Goal alignment check**:
   - Can every instance answer the primary goal? If not → add missing section
   - Can every instance answer the secondary goals? If not → add or adjust
   - Will instances be comparable in structure? If not → standardize section names and order
3. **Audience walkthrough**: mentally fill in the template as the target audience. At each section:
   - Do I know what to put here? If not → improve XML comment instruction
   - Will I recognize I did it right? If not → add format example or constraint
   - Is there ambiguity about scope or depth? If yes → add precision to instruction
4. Fix issues and fill gaps
5. Re-run audit checklist after fixes

# FINALIZATION

## Quality Gate

- [ ] Template IS document skeleton (TMPL-ST-01)
- [ ] All annotations use XML comments (TMPL-AN-01)
- [ ] Primary goal answerable from every instance
- [ ] Secondary goals covered by template sections
- [ ] Instances comparable (same sections, same order)
- [ ] Audit checklist from `TEMPLATE_RULES.md` passes
- [ ] No redundancy with existing templates in target domain
- [ ] Companion `*_RULES.md` created if template has complex verification rules (TMPL-ST-06)

## Output

- Template file: `[NAME]_TEMPLATE.md` in target skill or workflow folder
- Companion rules (if needed): `[NAME]_RULES.md` in same folder
