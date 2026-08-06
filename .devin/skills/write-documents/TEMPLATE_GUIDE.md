# Template Guide

Read BEFORE writing or modifying templates. Follow `TEMPLATE_RULES.md` for verification.

## 1. Core Principle

The template IS the document. Every template file is a skeleton that the agent copies, fills in, and strips of XML comments.

Every line is one of:
- **Template content** - Markdown headings, fields, placeholder values. Becomes part of the output document.
- **XML comment** - Annotations: rules, conditional markers, optional fields. Removed after instantiation.

Templates do not teach. Teaching belongs in `*_RULES.md` and `*_GUIDE.md` companion files.

## 2. Why Template Design Matters

Template inconsistencies compound: every document inherits them, and mixed formats prevent `/verify` from determining which is correct. A `[conditional - ...]` in one template and `<!-- Conditional: ... -->` in another teaches agents both are valid.

- **MECT** - Inconsistent annotation formats are noise that agents amplify
- **APAPALAN AP-PR-09** - "Repeat established structures" - templates ARE the structures
- **SOCAS-08** - Annotations that look like content are noise; XML comments are invisible
- **GRUC** - Rules define WHAT, Guides explain HOW, INFO documents explain WHY

## 3. Template Categories

### 3.1 Per-Task Documents

Created once per task, versioned, referenced by Doc ID. Require: Doc ID, Goal, Timeline, Document History.

Templates: INFO, SPEC, IMPL, TEST, TASKS, REVIEW, MINTO, DEFERRED_IMPROVEMENTS, FIXES.

### 3.2 Other Templates

Tracking logs, scaffolding, reusable artifacts, or embedded notation. Doc ID, Timeline, and Document History do not apply.

Templates: FAILS, LEARNINGS, MINTO-DRAFT, CONVERSATION, SKILL, WORKFLOW, STRUT.

## 4. Template Structure

`````
<!-- TOP COMMENT BLOCK (optional)
Template metadata: naming convention, creation trigger, lifecycle.
"Remove this comment block after creating the document."
-->

# [Document Title]: [PLACEHOLDER]

**Doc ID**: [TOPIC]-[TYPE][NN]
<!-- Topic IDs: 7-14 uppercase chars. Inside T##/S## folders use nested: [TOPIC]-[SUBTOPIC]-[TYPE][NN] -->
**Goal**: [Single sentence]
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)

## Section 1

<!-- Instruction: when to include, what to put here. -->

[Template content with [PLACEHOLDERS]]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial document created

<!-- EXAMPLE: Reference only. Do not copy into new documents. -->

## Full Example

```markdown
[Complete filled-in example]
```
`````

## 5. Annotation Types

All annotations are XML comments. Choose the appropriate type:

- **Removal instruction** - Template metadata to strip: `<!-- Remove this comment block after creating the document. -->`
- **Inline rule** - Guidance for specific field: `<!-- D-[NN] numbering is sequential across all runs, never reused. -->`
- **Optional fields** - Multi-line field options: `<!-- Optional fields per candidate:\n- **Status**: PARTIALLY ADDRESSED | SUPERSEDED -->`
- **Conditional section** - Section with insertion criteria: `<!-- Conditional: insert when 3+ audiences benefit. Per RULES.md SD-ES-06 -->`
- **Example annotation** - Before full example: `<!-- EXAMPLE: Reference only. Do not copy into new documents. -->`
- **Scope restriction** - Limit section to context: `<!-- Include only for UI specifications. -->`

## 6. Placeholder Types

- **Value to fill**: `[Single sentence describing purpose]`
- **Enumerated choice**: `[Minimal | Low | Medium | High]`
- **ID pattern**: `[TOPIC]-DF[NN]`
- **Date pattern**: `YYYY-MM-DD` (format IS the placeholder, no brackets)
- **Repeating pattern**: `[NN]`, `[NNNN]`

## 7. Conditional Header Fields

Per-task documents may include these fields when applicable:
- **Target file(s)** - Documents that reference code or files. Always list format.
- **Feature** - `[FEATURE_SLUG]`. Used in SPEC, IMPL, TEST, TASKS.
- **Depends on** - List of document dependencies.
- **Does not depend on** - Explicit exclusions (SPEC only).
- **Source** - Reference to upstream documents (TASKS, MINTO).

## 8. Dynamic Template Components

Design these active guidance elements before construction. They determine how well the filling agent can use the template.

- **Conditional sections** - Sections that apply only in certain contexts. Mark with `<!-- Conditional: insert when [criteria]. Per [RULE_ID] -->`. Derive candidates from exemplar analysis: sections present in some instances but not all are conditional candidates.
- **Agent instructions** - XML comments that guide the filling agent at non-obvious sections. Include when: field purpose is ambiguous, expected depth varies, format has constraints, or section has dependencies on other sections. The filling agent should never wonder "what goes here?"
- **Full Example** - A complete filled-in example in a fenced code block at template end (TMPL-ST-05). Include when template has 3+ sections, uses conditional sections, or has complex placeholder patterns. The example shows what a correctly completed instance looks like, resolving ambiguities that instructions alone cannot.

## 9. Exemplar Templates

Study these for the correct pattern:
- `INFO_TEMPLATE.md` - Clean header, MNF with `<!-- Remove this section -->`, Sources
- `DEFERRED_IMPROVEMENTS_TEMPLATE.md` - Top comment block for naming convention, inline XML comments for field options
- `RESEARCH_SUMMARY_TEMPLATE.md` (deep-research skill) - Conditional sections with `<!-- Conditional: ... -->` XML comments
