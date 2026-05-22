---
name: write-documents
description: Apply when creating or editing INFO, SPEC, IMPL, TEST, FIX documents, STRUT plans, or CONVERSATION files
---

# Document Writing Guide

This skill contains document templates, formatting rules, and writing quality standards.

**Writing quality standard:** All documents MUST follow:
- `APAPALAN_RULES.md` - Precision formatting, brevity, document structure, naming conventions
- `MECT_WRITING_RULES.md` - Voice, word choice, terminology design, heading/list construction, description types

**Quality evaluation:** `SOCAS_RULES.md` - Signs of Confusion and Sloppiness (15 criteria). Used by `/verify`, `/critique`, `/improve`, `/research`.

**Translation quality:** `TRANSLATION_RULES.md` - Quality dimensions, term pairs, prompt templates, improvement cycle. Used by `/translate`, `/verify`, `/improve`.

Read APAPALAN and MECT before writing any document. Read SOCAS when evaluating quality.

## Verb Mapping

This skill implements:
- [WRITE-INFO] - Create INFO documents (use `INFO_TEMPLATE.md`)
- [WRITE-SPEC] - Create SPEC documents (use `SPEC_TEMPLATE.md`, read `SPEC_RULES.md`)
- [WRITE-IMPL-PLAN] - Create IMPL documents (use `IMPL_TEMPLATE.md`)
- [WRITE-TEST-PLAN] - Create TEST documents (use `TEST_TEMPLATE.md`)
- [WRITE-FIX] - Create FIX documents (use `FIXES_TEMPLATE.md`)
- [WRITE-FAIL] - Create/update FAILS.md (use `FAILS_TEMPLATE.md`)
- [WRITE-REVIEW] - Create _REVIEW.md documents (use `REVIEW_TEMPLATE.md`)
- [WRITE-TASKS-PLAN] - Create TASKS documents (use `TASKS_TEMPLATE.md`)
- [WRITE-STRUT] - Create/insert STRUT plans (use `STRUT_TEMPLATE.md`)
- [WRITE-SKILL] - Create/update skill folders (use `SKILL_TEMPLATE.md`, read `SKILL_RULES.md`)
- [WRITE-CONVERSATION] - Create conversation files (use `CONVERSATION_TEMPLATE.md`, read `CONVERSATION_RULES.md`)
- [UPDATE-CONVERSATION] - Update existing conversation files (read `CONVERSATION_RULES.md`)

## MUST-NOT-FORGET

- Read `APAPALAN_RULES.md` before writing - precision first, then brevity
- Read `MECT_WRITING_RULES.md` before writing - voice, word choice, terminology design
- Use lists, not Markdown tables
- No emojis - ASCII only, no `---` markers between sections
- Header block: Doc ID (required), Goal (required), Target file, Depends on (omit if N/A)
- Every document MUST have a unique ID
- Reference other docs by filename AND Doc ID: `_SPEC_CRAWLER.md [CRWL-SP01]`
- Be exhaustive: list ALL domain objects, actions, functions
- Document History section at end, reverse chronological
- Use box-drawing characters (├── └── │) for trees
- SPEC, IMPL, TEST documents MUST have MUST-NOT-FORGET section (after header block, before TOC)

## Document Types and When to Use

**Research and Knowledge:**
- **INFO** (`_INFO_[TOPIC].md`) - Research, analysis, option evaluation. Use when gathering information before making decisions. Read template: `INFO_TEMPLATE.md`
- **REVIEW** (`_REVIEW_[TOPIC].md`) - Structured review of existing documents. Use for `/critique` and `/reconcile` outputs. Read template: `REVIEW_TEMPLATE.md`

**Planning:**
- **SPEC** (`_SPEC_[COMPONENT].md`) - Technical specifications. Use to define WHAT to build before building it. Read template: `SPEC_TEMPLATE.md`, rules: `SPEC_RULES.md`
- **IMPL** (`_IMPL_[COMPONENT].md`) - Implementation plans. Use to define HOW to build what SPEC describes. Read template: `IMPL_TEMPLATE.md`
- **TEST** (`_TEST_[COMPONENT].md`) - Test plans. Use to define how to VERIFY what SPEC requires. Read template: `TEST_TEMPLATE.md`
- **TASKS** (`TASKS_[TOPIC].md`) - Partitioned task lists from IMPL/TEST plans. Use to break plans into discrete work items. Read template: `TASKS_TEMPLATE.md`

**Execution Tracking:**
- **STRUT** (embedded in any document) - Structured execution plans with checkboxes. Use for phased work with verification gates. Read template: `STRUT_TEMPLATE.md`
- **FIXES** (`_IMPL_[COMPONENT]_FIXES.md`) - Fix tracking during implementation. Read template: `FIXES_TEMPLATE.md`
- **FAILS** (`FAILS.md`) - Failure log, lessons learned. Use to record mistakes and prevent repetition. Read template: `FAILS_TEMPLATE.md`

**Session Tracking** (templates from @skills:session-management):
- **NOTES** (`NOTES.md`) - Session notes and context
- **PROBLEMS** (`PROBLEMS.md`) - Problem tracking
- **PROGRESS** (`PROGRESS.md`) - Progress tracking

**Conversation Tracking:**
- **CONVERSATION** (`CONVERSATION_[COUNTERPARTY].md`) - Email/WhatsApp conversation tracking. Read template: `CONVERSATION_TEMPLATE.md`, rules: `CONVERSATION_RULES.md`

**Workflow Documents:**
- **WORKFLOW** (`.md` in workflows/) - Agent workflow definitions. Read template: `WORKFLOW_TEMPLATE.md`, rules: `WORKFLOW_RULES.md`

**Skill Documents:**
- **SKILL** (`SKILL.md` in skills/[name]/) - Agent skill definitions. Read template: `SKILL_TEMPLATE.md`, rules: `SKILL_RULES.md`

## Document Dependency Chain

```
INFO (research) → SPEC (what) → IMPL (how) → TASKS (work items)
                      │                             │
                      └──> TEST (verify) ───────────┘
```

Each document type builds on the previous. INFO informs SPEC decisions. SPEC defines what IMPL must build. TEST verifies what SPEC requires. TASKS partitions IMPL and TEST into discrete work items.

## Usage

1. Read this SKILL.md for core rules
2. Read `APAPALAN_RULES.md` for precision, brevity, structure, naming
3. Read `MECT_WRITING_RULES.md` for voice, word choice, terminology, headings, lists
4. Read the template for your document type (required)
5. For SPEC documents: also read `SPEC_RULES.md` (required)
6. For WORKFLOW documents: also read `WORKFLOW_RULES.md` (required)
7. For SKILL documents: also read `SKILL_RULES.md` (required)
8. For CONVERSATION documents: also read `CONVERSATION_RULES.md` (required)
9. Follow the template structure exactly, except when user requests exceptions

## Document Writing Rules

- Enumerations: use comma-separated format (`.pdf, .docx, .ppt`), NOT slash-separated (`.pdf/.docx/.ppt`)
- Ambiguous modifiers: when a clause can attach to multiple nouns, split into separate sentences
  - BAD: "Files starting with '!' signify high relevance that must be treated with extra attention."
  - GOOD: "Files starting with '!' indicate high relevance. This information must be treated with extra attention."

## File Naming

- `_INFO_[TOPIC].md` - Research, analysis, preparation documents
- `_SPEC_[COMPONENT].md` - Technical specifications
- `_SPEC_[COMPONENT]_UI.md` - UI specifications
- `_IMPL_[COMPONENT].md` - Implementation plans
- `_IMPL_[COMPONENT]_FIXES.md` - Fix tracking during implementation
- `SPEC_[COMPONENT]_TEST.md` - Test plan for specification
- `IMPL_[COMPONENT]_TEST.md` - Test plan for implementation
- `TASKS_[TOPIC].md` - Task plans (partitioned work items)
- `CONVERSATION_[COUNTERPARTY].md` - Conversation tracking (never plain `CONVERSATION.md`)
- `!` prefix for priority docs that must be read first

## Agent Behavior

- Follow APAPALAN + MECT: precision first, then cut every unnecessary word
- NEVER ask for continuations when following plans
- Before assumptions, propose 2-3 implementation alternatives
- List assumptions at spec start for user verification
- Optimize for simplicity
- Re-use existing code by default (DRY principle)
- Research APIs before suggesting; rely on primary sources only
- Document user decisions in "Key Mechanisms" and "What we don't want" sections

## ID System

See `[AGENT_FOLDER]/rules/devsystem-ids.md` rule (always-on) for complete ID system.

**Quick Reference:**
- Document: `[TOPIC]-[DOC][NN]` (IN = Info, SP = Spec, IP = Impl Plan, TP = Test Plan)
  - Example: `CRWL-SP01`, `AUTH-IP01`
- Spec-Level: `[TOPIC]-[TYPE]-[NN]` (FR = Functional Requirement, IG = Implementation Guarantee, DD = Design Decision)
  - Example: `CRWL-FR-01`, `AUTH-DD-03`
- Plan-Level: `[TOPIC]-[DOC][NN]-[TYPE]-[NN]` (EC = Edge Case, IS = Implementation Step, VC = Verification Checklist, TC = Test Case)
  - Example: `CRWL-IP01-EC-01`, `AUTH-TP01-TC-05`