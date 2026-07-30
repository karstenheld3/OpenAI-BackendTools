---
description: Fix any problem by reading relevant DevSystem knowledge and applying it
---

# Fix Workflow

Fix any problem by reading relevant DevSystem knowledge and applying it.

## Required Reading (Always)

- `rules/devsystem-core.md` - Core definitions, document types, workflow reference
- `rules/agent-behavior.md` - Attitude, communication, work patterns

## MUST-NOT-FORGET

- Read context-specific files BEFORE acting
- Apply knowledge from read files, don't just route to other workflows
- Document findings before implementing
- Verify fix against the principles read

## Step 1: Classify Problem

Determine what's broken:
- CODE - Implementation defect
- DOCUMENT - Incorrect/incomplete documentation
- DESIGN - Architecture or approach flaw
- UNDERSTANDING - Knowledge gap
- PROCESS - Workflow or procedure issue
- CONFIGURATION - Settings or environment

## Step 2: Read Context-Specific Knowledge

Based on classification, READ these files from `[AGENT_FOLDER]`:

CODE:
- `workflows/bugfix.md` - Bug investigation patterns
- `workflows/implement.md` - Impact assessment, execution sequence
- `skills/coding-conventions/SKILL.md` - Code rules

DOCUMENT:
- `workflows/improve.md` - Issue categories (contradictions, ambiguities...)
- `workflows/verify.md` - Verification techniques
- `skills/write-documents/SKILL.md` - Document rules

DESIGN:
- `workflows/critique.md` - Finding flaws (mindset, questions)
- `workflows/reconcile.md` - Pragmatic evaluation
- `rules/edird-phase-planning.md` - Phase gates

UNDERSTANDING:
- `workflows/research.md` - Research principles (MEPI/MCPI)
- `workflows/deep-research.md` - Deep investigation
- `skills/deep-research/SKILL.md` - Strategies

PROCESS:
- `workflows/write-spec.md` - Specification patterns
- `workflows/write-impl-plan.md` - Planning patterns

## Step 3: Apply Knowledge

Using principles from read files:

1. Understand the problem (root cause)
2. Assess impact (what's affected)
3. Plan the fix (minimal change)
4. Execute the fix
5. Verify against read principles
