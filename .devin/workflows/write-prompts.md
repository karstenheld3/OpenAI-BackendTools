---
description: Create prompt queue files (_PROMPTS_[Topic].md) for sequential headless execution
auto_execution_mode: 3
---

# Write Prompts Workflow

Create `_PROMPTS_[Topic].md` files containing an ordered list of prompts. Each prompt is a fenced code block. Prompts execute sequentially as turns of ONE session.

**Goal**: Validated `_PROMPTS_[Topic].md` file with focused, verifiable prompts

**Why**: Headless prompts must be complete on first submission - no human correction loop

## Required Skills

- @skills:write-documents `PROMPTS_TEMPLATE.md` for file skeleton (copy and fill)
- @skills:write-documents `PROMPTS_GUIDES.md` for strategic approach (read BEFORE writing)
- @skills:write-documents `PROMPTS_RULES.md` for output verification (PRMT-* rules)

## MUST-NOT-FORGET

- First non-empty line MUST be an opening fence OR Commentary (heading/notes). No YAML frontmatter.
- Fence length: 3-9 backticks per prompt. Outer fence MUST exceed deepest inner fence
- `---` separator between every pair of consecutive prompts
- Commentary (headings, notes) only between `---` and next fence - never sent to model
- Heading recommendation (PRMT-FT-07): use `## Prompt N - [title]` before each prompt. If headings are used, ALL prompts MUST have headings
- At least one prompt per file
- **NEVER modify tracking documents** (PROGRESS.md, PROBLEMS.md, NOTES.md, FAILS.md). Write-* workflows create NEW files only.
- Pre-Write Privacy Gate (`agent-behavior.md`): General-purpose documents → all content generic. ILLUSTRATIVE content → examples generic.
- **Rule precedence**: PRMT-CT-04 (objectives not steps) overrides PRMT-CT-05 (precision). See PRMT-CT-04 for details.

## Context Branching

This workflow has two modes. Determine the mode from the user's request:

- **Compose mode** (default) - Write prompts from scratch based on user description
  - Trigger: `/write-prompts [description]`
  - Steps: classify task, decompose, write, verify

- **From Template mode** - Generate a filled prompts file from a `_PROMPTS_*_TEMPLATE.md`
  - Trigger: `/write-prompts from template [path/to/template]`
  - Steps: read template, collect placeholder values, generate filled instance, verify
  - The template's top comment block contains the placeholder registry and usage instructions
  - Output: `_PROMPTS_[Topic]_[Instance].md` following the template's naming convention

## Prerequisites

### Compose mode

- User has described one or more prompts to execute sequentially
- Determine if prompts contain code blocks (affects fence length)

### From Template mode

- User has provided a path to a `_PROMPTS_*_TEMPLATE.md` file
- User has provided (or can provide) case-specific context for placeholder values

# COMPOSE MODE

## Step 1: Read PROMPTS_GUIDES.md

Read `PROMPTS_GUIDES.md` from @skills:write-documents. Classify the task, decide decomposition, plan state flow between prompts.

## Step 2: Determine File Location and Name

- Filename: `_PROMPTS_[Topic].md`
- `[Topic]` = CamelCase description of prompt purpose
- Location: session folder (default), workspace root, or user-specified path
- Examples: `_PROMPTS_SetupProject.md`, `_PROMPTS_MigrateAuth.md`, `_PROMPTS_AnalyzePerformance.md`

## Step 3: Select Fence Length Per Prompt

For each prompt, find the deepest inner fence and set the outer fence one longer.

- Prompt has no code blocks → 3 backticks
- Prompt contains ``` blocks → 4+ backtick outer fence
- Prompt contains ```` blocks (e.g. markdown examples with ``` inside) → 5+ backtick outer fence
- Maximum outer fence: 9 backticks. If deeper nesting needed, restructure the prompt.

## Step 4: Write Prompts File

**Format overview** (3-prompt example with headings, per PRMT-FT-07):

`````markdown
## Prompt 1 - Setup

```
First prompt text. Plain instruction, no code blocks inside.
```

---

## Step 2 - commentary heading (never sent to the model)

Optional notes explaining the next prompt's purpose.

````
Second prompt with a code block inside:
```python
print("hello")
```
````

---

## Prompt 3 - Finalize

```
Third prompt. Simple again.
```
`````

**Format rules:**
1. First non-empty line = opening fence OR Commentary (heading/notes). No YAML frontmatter
2. Each prompt = opening fence + prompt text + closing fence
3. Closing fence = line with >= N backticks (where N = opening fence length)
4. `---` on its own line between consecutive prompts
5. Commentary (headings, paragraphs, lists) allowed before the first prompt and between `---` and next opening fence
6. Heading recommendation (PRMT-FT-07): use `## Prompt N - [title]` before each prompt. If headings are used, ALL prompts MUST have headings
7. Info string after opening fence (e.g. `` ```text ``) is optional and ignored by executor
8. Prompts execute in file order

## Step 5: Verify

Check output against all PRMT-* rules in `PROMPTS_RULES.md`:

- [ ] Format (FT): PRMT-FT-01 through PRMT-FT-07
- [ ] Structure (ST): PRMT-ST-01 through PRMT-ST-05
- [ ] Sequence (SQ): PRMT-SQ-01 through PRMT-SQ-03
- [ ] Content (CT): PRMT-CT-01 through PRMT-CT-07

# FROM TEMPLATE MODE

## Step T1: Read Template

Read the `_PROMPTS_*_TEMPLATE.md` file specified by the user. Extract:

1. **Placeholder registry** from the top comment block - list of all `[PLACEHOLDER]` values with descriptions
2. **Instance naming convention** - how the filled file should be named
3. **Usage instructions** - any special filling rules
4. **Conditional sections** - prompts or sections marked `<!-- Conditional: ... -->` that may be included or removed based on context

## Step T2: Collect Placeholder Values

For each placeholder in the registry:

1. Check if the user provided the value in their request or conversation history
2. If not provided: derive from context (session files, PROBLEMS.md, SPEC, IMPL) by reading the referenced files
3. If not derivable: list the missing placeholders and their descriptions - the user must provide them
4. Do not guess placeholder values. Every value must be sourced from user input or workspace files.

## Step T3: Generate Filled Instance

1. Copy the template content
2. Remove ALL XML comments (template annotations are not part of the output)
3. Replace ALL `[PLACEHOLDER]` values with the collected case-specific data
4. Resolve conditional sections: remove the branch that does not apply based on the collected values (e.g., remove BUG pipeline when category = CHANGE)
5. Verify fence depths are still correct after modifications (PRMT-FT-02)
6. Save as `_PROMPTS_[Topic]_[Instance].md` following the template's naming convention

## Step T4: Verify Filled Instance

The filled file must pass all PRMT-* rules as a standalone prompts file:

- [ ] PRMT-FT-01: First non-empty line is an opening fence OR Commentary
- [ ] PRMT-FT-02: Fence lengths correct (outer > deepest inner)
- [ ] PRMT-FT-03: `---` separator between every pair of consecutive prompts
- [ ] PRMT-FT-04: Commentary only between separator and next fence (or before first fence)
- [ ] PRMT-FT-07: If headings are used, all prompts have headings (MUST)
- [ ] PRMT-ST-01..05: Each prompt has objective, constraints (if implementation), verification, single reasoning mode, density limit
- [ ] PRMT-SQ-01..03: No contradictions, explicit dependencies, commentary documents state
- [ ] PRMT-CT-01..07: Specific objectives, negative constraints, observable verification
- [ ] No unresolved `[PLACEHOLDER]` values remain in the output
- [ ] No XML comments remain in the output
- [ ] Privacy gate: no real user data leaked into the filled instance

# OUTPUT

## Compose mode

Validated `_PROMPTS_[Topic].md` file in target location.

## From Template mode

Validated `_PROMPTS_[Topic]_[Instance].md` file with all placeholders resolved, ready for sequential execution.

## Quality Gate

- [ ] All PRMT-* rules pass
- [ ] Privacy gate applied (no real project data in examples)
- [ ] Fence depths verified (outer > deepest inner per prompt)
- [ ] **From Template mode**: Zero unresolved placeholders
- [ ] **From Template mode**: Zero remaining XML comments
- [ ] **From Template mode**: All conditional sections resolved
