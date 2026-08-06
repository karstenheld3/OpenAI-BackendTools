# Template Rules

Verification priority:
1. Structure - template IS the document, not a description of it
2. Annotations - XML comments only, no italic/bracket markers
3. Header and sections - Doc ID, Topic ID comment, Document History

## Rule Index

Structure (ST)
- TMPL-ST-01: Template is the document skeleton (no meta-wrapper)
- TMPL-ST-02: No prose descriptions between template sections
- TMPL-ST-03: No meta-headings describing sections
- TMPL-ST-04: Repeatable items show one instance
- TMPL-ST-05: Full example at end with `<!-- EXAMPLE: -->` annotation
- TMPL-ST-06: Complex rules in companion `*_RULES.md` or `*_GUIDE.md` files

Annotation (AN)
- TMPL-AN-01: All annotations use XML comments
- TMPL-AN-02: Conditional sections use `<!-- Conditional: ... -->` format
- TMPL-AN-03: No bracket markers for annotations
- TMPL-AN-04: No italic markers for annotations
- TMPL-AN-05: No inline teaching examples (BAD/GOOD comparisons)
- TMPL-AN-06: No instruction sections disguised as content

Placeholder (PH)
- TMPL-PH-01: Values and IDs in brackets
- TMPL-PH-02: Date patterns without brackets

Header (HD)
- TMPL-HD-01: Doc ID label without suffixes
- TMPL-HD-02: Doc ID for per-task documents only
- TMPL-HD-03: Topic ID XML comment after Doc ID field
- TMPL-HD-04: Target file(s) plural with list format
- TMPL-HD-05: Timeline for per-task documents only

Sections (SN)
- TMPL-SN-01: Document History in per-task templates
- TMPL-SN-02: MUST-NOT-FORGET in planning documents (SPEC, IMPL, TEST)
- TMPL-SN-03: Table of Contents when 4+ numbered sections

## TMPL-ST-01: Template is the Document Skeleton

The template IS the document. Every line is either template content (becomes output) or an XML comment (removed after instantiation). Templates wrapped in code blocks with descriptive headings are meta-wrappers.

**BAD:**
`````markdown
# TASKS Template

Template for creating task plan documents.

## Header Block

```markdown
# TASKS: [TOPIC] Tasks Plan
**Doc ID**: [TOPIC]-TK01
```

## Task Item Structure

```markdown
- [ ] **[TOPIC]-TK-001** - Description
```
`````

**GOOD:**
```markdown
<!-- TASKS TEMPLATE. Remove this comment after creating. -->

# TASKS: [TOPIC] Tasks Plan

**Doc ID**: [TOPIC]-TK01
**Goal**: Partitioned tasks for [TOPIC] implementation
```

**Justified exceptions**: Templates requiring YAML frontmatter (SKILL, WORKFLOW) or defining append-only entry formats (DRIFTS) may use the meta-wrapper pattern when the template content would be interpreted by markdown processors.

## TMPL-ST-02: No Prose Between Sections

If a section needs explanation, use an XML comment inside it. Prose paragraphs between sections look like template content and get preserved in output.

**BAD:**
```markdown
## 2. Edge Cases

Derive from domain objects and actions:

**Categories to consider:**
- Input boundaries (empty, null, max length)
- State transitions (invalid state, concurrent modifications)
```

**GOOD:**
```markdown
## 2. Edge Cases

<!-- Derive from domain objects and actions. Categories: input boundaries, state transitions, external failures, data anomalies. -->

- **[PREFIX]-IP01-EC-01**: [Boundary/failure description] -> [Expected behavior]
```

## TMPL-ST-03: No Meta-Headings

Never use headings that describe what a section is. The sections ARE the template.

**BAD:** `## Header Block`, `## Section Structure`, `## Full Example Description`, `## Task Item Structure`

**GOOD:** `## Task Overview`, `## Document History`, `## Full Example`

## TMPL-ST-04: Repeatable Items

Show one instance of repeatable items. Agent understands repetition from the pattern.

**BAD:** Three `### D-01:`, `### D-02:`, `### D-03:` entries showing the same structure.

**GOOD:** One `### D-01:` entry with all fields. Agent generates D-02, D-03 following the pattern.

## TMPL-ST-05: Full Example at End

Include a full example when the template has 3+ sections, uses conditional sections, or has complex placeholder patterns. The example must be in a fenced code block at the end, preceded by the example annotation.

`````markdown
<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed document with real values. -->

## Full Example

```markdown
[Complete filled-in example]
```
`````

## TMPL-ST-06: Rules in Companion Files

Complex rules, decision logic, categories, and verification procedures belong in `*_RULES.md` or `*_GUIDE.md` companion files. The template is the skeleton only.

**BAD:** Template contains 20-line rule explanation with decision tree.

**GOOD:** Template contains `<!-- See SPEC_RULES.md SPEC-LG-01 for logging decision tree. -->` and the rules live in the companion file.

## TMPL-AN-01: XML Comments for All Annotations

All template annotations use XML comments. No exceptions.

Annotation types:
- **Removal instruction**: `<!-- Remove this section/block after creating the document. -->`
- **Inline rule**: `<!-- D-[NN] numbering is sequential across all runs, never reused. -->`
- **Optional fields**: `<!-- Optional fields per candidate:\n- **Field**: [values] -->`
- **Conditional section**: `<!-- Conditional: insert when [criteria]. Per [rule reference] -->`
- **Example annotation**: `<!-- EXAMPLE: Reference only. Do not copy into new documents. -->`
- **Scope restriction**: `<!-- Include only for UI specifications. -->`

## TMPL-AN-02: Conditional Section Format

Conditional sections use XML comment with insertion criteria and rule reference.

**BAD:** `[conditional - insert when 3+ audiences benefit]`

**GOOD:** `<!-- Conditional: insert when 3+ audiences benefit. Per RESEARCH_SUMMARY_RULES.md SD-ES-06 -->`

## TMPL-AN-03: No Bracket Markers

Bracket markers `[text]` overlap with the placeholder convention, creating polysemy (AP-NM-01). Agents cannot distinguish `[conditional - insert when...]` from `[value to fill in]`.

**BAD:** `[conditional - insert when research produces actionable conclusions]`

**GOOD:** `<!-- Conditional: insert when research produces actionable conclusions. Per INFO_GUIDE.md Section 3.3 -->`

## TMPL-AN-04: No Italic Markers

Italic markers `*(text)*` are visible noise in rendered output (SOCAS-08). They appear as formatted text in the document instead of being invisible annotations.

**BAD:** `*(For UI specs only)*`, `*(If fixing rule violations)*`

**GOOD:** `<!-- Include only for UI specifications. -->`, `<!-- Conditional: include if fixing rule violations. -->`

## TMPL-AN-05: No Inline Teaching Examples

BAD/GOOD code comparisons embedded in template sections confuse instruction with template content. Wrap in XML comments or move to companion files.

**BAD:**
`````markdown
## 4. Functional Requirements

**BAD:**
```
- Toast notifications should support info, success, error types
```

**GOOD:**
```
**UI-FR-01: Toast Notifications**
- Support info, success, error, warning message types
```
`````

**GOOD:**
```markdown
## 4. Functional Requirements

<!-- BAD: "Toast notifications should support info, success, error types" (no ID, vague)
     GOOD: "**UI-FR-01: Toast Notifications** - Support info, success, error, warning message types" (ID + specific) -->

**[PREFIX]-FR-01: [Requirement Title]**
- [Requirement detail 1]
```

## TMPL-AN-06: No Instruction Sections as Content

Sections containing rules, categories, or management instructions that look like document content must be wrapped in XML comments.

**BAD:**
```markdown
## Failure Categories

- `[CRITICAL]` - Flawed assumption causing production failure
- `[HIGH]` - Logic error likely to cause failure

## Location Rules

- **SESSION-MODE**: `[SESSION_FOLDER]/FAILS.md`
```

**GOOD:**
```markdown
<!-- Failure categories:
- [CRITICAL] - Flawed assumption causing production failure
- [HIGH] - Logic error likely to cause failure

Location: SESSION-MODE -> [SESSION_FOLDER]/FAILS.md, PROJECT-MODE -> [WORKSPACE_FOLDER]/FAILS.md -->
```

## TMPL-PH-01: Bracket Placeholders

Values, IDs, and enumerated options use bracket notation.

- **Value to fill**: `[Single sentence describing purpose]`
- **Enumerated choice**: `[Minimal | Low | Medium | High]`
- **ID pattern**: `[TOPIC]-DF[NN]`
- **Repeating pattern**: `[NN]`, `[NNNN]`

## TMPL-PH-02: Date Patterns Without Brackets

Date format IS the placeholder. No brackets needed.

**BAD:** `[YYYY-MM-DD]`, `[date]`

**GOOD:** `YYYY-MM-DD`, `YYYY-MM-DD HH:MM`

## TMPL-HD-01: Doc ID Label

Use `**Doc ID**:` without suffixes. `(TDID)` is redundant - all Doc IDs follow the Topic-based pattern (AP-NM-01).

**BAD:** `**Doc ID (TDID)**: [TOPIC]-SP[NN]`

**GOOD:** `**Doc ID**: [TOPIC]-SP[NN]`

## TMPL-HD-02: Doc ID Applicability

Doc ID required for per-task documents only: INFO, SPEC, IMPL, TEST, TASKS, REVIEW, MINTO, DEFERRED_IMPROVEMENTS, FIXES.

Not applicable for: tracking logs (FAILS, LEARNINGS), scaffolding (MINTO-DRAFT, STRUT), reusable artifacts (SKILL, WORKFLOW), embedded notation, or conversation tracking (CONVERSATION).

## TMPL-HD-03: Topic ID XML Comment

All templates with a Doc ID field must include the Topic ID guidance comment immediately after Doc ID.

```markdown
**Doc ID**: [TOPIC]-SP[NN]
<!-- Topic IDs: 7-14 uppercase chars. Inside T##/S## folders use nested: [TOPIC]-[SUBTOPIC]-SP[NN] -->
```

## TMPL-HD-04: Target File(s) Format

Always use plural `Target file(s):` with list format, even for single targets.

**BAD:** `**Target file**: [path/to/file.py]`, `**Target files**: [path]`

**GOOD:**
```markdown
**Target file(s)**:
- `[path/to/file1.py]`
- `[path/to/file2.py]`
```

## TMPL-HD-05: Timeline Field

Per-task documents only. Not applicable for tracking logs, scaffolding, or reusable artifacts.

Format: `Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)`

## TMPL-SN-01: Document History

Required in all per-task document templates. Format per `core-conventions.md`: reverse chronological, action prefixes (Added, Changed, Fixed, Removed, Moved).

Not required for: tracking logs, scaffolding, reusable artifacts, embedded notation.

## TMPL-SN-02: MUST-NOT-FORGET Section

Required for planning documents: SPEC, IMPL, TEST.

Also used in: INFO (research scope), CONVERSATION (formatting rules).

Not required for: REVIEW, MINTO, MINTO-DRAFT, FIXES, DEFERRED, FAILS, LEARNINGS, TASKS.

## TMPL-SN-03: Table of Contents

Required when template has 4+ numbered sections.

## Audit Checklist

When creating or reviewing a template, verify all rules:

- [ ] TMPL-ST-01: Template IS the document, not wrapped in code blocks
- [ ] TMPL-AN-01: Annotations as XML comments (no prose, brackets, or italic markers)
- [ ] TMPL-AN-05: BAD/GOOD examples wrapped in XML comments, not inline
- [ ] TMPL-ST-06: Complex rules in companion `*_RULES.md` or `*_GUIDE.md`
- [ ] TMPL-HD-01: Doc ID uses `**Doc ID**:` not `**Doc ID (TDID)**:`
- [ ] TMPL-HD-02: Doc ID present for per-task documents, absent for others
- [ ] TMPL-HD-03: Topic ID XML comment present after Doc ID
- [ ] TMPL-HD-04: `**Target file(s)**:` with list format
- [ ] TMPL-HD-05: Timeline present for per-task documents
- [ ] TMPL-SN-01: Document History present in per-task templates
- [ ] TMPL-SN-02: MUST-NOT-FORGET present in planning documents
- [ ] TMPL-ST-05: Full example in fenced code block with annotation
- [ ] TMPL-PH-01: Placeholders use `[BRACKETS]` consistently
- [ ] TMPL-PH-02: Date patterns use format directly, no brackets
- [ ] TMPL-AN-02: Conditional sections use XML comment with criteria
- [ ] TMPL-AN-06: Instruction sections wrapped in XML comments
