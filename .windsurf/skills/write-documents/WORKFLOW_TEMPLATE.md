# Workflow Template

Template for writing Windsurf workflows with MNF, context branching, and verification.

## Workflow Structure

```markdown
---
description: [Brief description of what the verb does]
auto_execution_mode: 1
---

# [Verb Name] Workflow

[Brief description in plain English - no AGEN verb references]

**Goal**: [What this workflow produces - the expected outcome]

**Why**: [Problem this workflow solves - why it exists]

## Required Skills

- @skill-name for [what it provides]

## MUST-NOT-FORGET

- [Critical item 1]
- [Critical item 2]
- Run `/verify` after workflow complete

## Mandatory Re-read

**SESSION-MODE**:
- NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**:
- README.md, !NOTES.md or NOTES.md, FAILS.md

## Prerequisites

- [Document X exists] → proceed
- [Document X missing] → run `/other-workflow` first

## GLOBAL-RULES

Apply to ALL contexts before any context-specific steps.

1. [Universal rule]
2. [Universal rule]

# CONTEXT-SPECIFIC

## Context A: [Condition]

1. [Step]
2. [Step]

## Context B: [Condition]

1. [Step]
2. [Step]

## No Context Match

1. [Fallback or ask user]

# EXECUTION

## Steps

1. [Step]
2. [Step]
3. [Step]

## Gate Check: [PHASE]→[NEXT_PHASE]

- [ ] [Condition 1]
- [ ] [Condition 2]

Pass: [next action] | Fail: Continue current phase

## Stuck Detection

If 3 consecutive attempts fail:
1. Document in PROBLEMS.md
2. Ask user for guidance

# FINALIZATION

## Verification

Run `/verify` to check:
1. [Check 1]
2. [Check 2]

## Output

- [Where results go]
- [What to update]
```

## Optional Sections

Include based on workflow complexity:

- **Required Skills** - Workflow uses skills
- **MUST-NOT-FORGET** - Always (even 2-3 items)
- **Mandatory Re-read** - Modifies docs/code, makes decisions
- **Prerequisites** - Has entry conditions
- **GLOBAL-RULES** - Has universal rules across contexts
- **CONTEXT-SPECIFIC** - Behavior varies by context
- **Gate Check** - Multi-phase workflow
- **Stuck Detection** - Has retry loops
- **Verification** - Always
- **Output** - Has specific output locations

## Complexity Tiers

**Tier 1: Simple** (30-50 lines)
- Header (desc, goal, why), MNF, Steps, Verification

**Tier 2: Standard** (50-100 lines)
- Header, MNF, Prerequisites, GLOBAL-RULES, Steps, Verification

**Tier 3: Complex** (100-300 lines)
- All sections as needed

## Anti-Patterns

- Duplicate content from skills (reference instead)
- AGEN verbs in descriptions
- Hardcoded paths (use placeholders like `[WORKSPACE_FOLDER]`)
- Skip MNF or Verification sections
- Omit Goal/Why in header

## Examples

- `/fail`, `/learn` - Tier 1 (simple)
- `/write-info`, `/improve` - Tier 2 (standard)
- `/verify`, `/implement`, `/transcribe` - Tier 3 (complex)
