---
description: Create specification from requirements
auto_execution_mode: 1
---

# Write Specification Workflow

Create technical specifications from requirements.

## Required Skills

Invoke these skills before proceeding:
- @write-documents for document structure and formatting rules

## Prerequisites

- User has described the problem or feature
- Clarify scope and naming before starting
- Read @write-documents skill

## Steps

1. **Gather Requirements**
   - Ask clarifying questions if scope is unclear
   - Identify domain objects, actions, and constraints
   - Document "What we don't want" (anti-patterns, rejected approaches)

2. **Propose Alternatives** (for complex tasks)
   - Present 2-3 implementation approaches
   - Compare pros/cons
   - Let user choose before proceeding

3. **Create Specification File**
   - Create `_SPEC_[COMPONENT].md` in session folder
   - Follow @write-documents skill structure:
     - Header block (Goal, Target file, Dependencies)
     - Table of Contents
     - Scenario (Problem, Solution, What we don't want)
     - Domain Objects
     - Functional Requirements (numbered: XXXX-FR-01)
     - Design Decisions (numbered: XXXX-DD-01)
     - Key Mechanisms

4. **For UI Specs** (`_SPEC_[COMPONENT]_UI.md`)
   - Add User Actions section
   - Add UX Design with ASCII diagrams
   - Show ALL buttons and interactive elements

5. **Verify**
   - Run /verify workflow
   - Check exhaustiveness: all domain objects, buttons, functions listed?
