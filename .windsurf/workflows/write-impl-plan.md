---
description: Create implementation plan from spec
auto_execution_mode: 1
---

# Write Implementation Plan Workflow

Create implementation plans from specifications.

## Required Skills

Invoke these skills before proceeding:
- @write-documents for document structure and formatting rules

## Prerequisites

- Specification exists (`_SPEC_[COMPONENT].md`)
- Read spec completely before starting
- Read @write-documents skill

## Steps

1. **Create Implementation Plan File**
   - Create `_IMPL_[COMPONENT].md` in session folder
   - Header block with Plan ID, Goal, Target files (NEW/EXTEND/MODIFY)

2. **Define File Structure**
   - Tree diagram showing files to create/modify
   - Mark each: [NEW], [EXTEND +N lines], [MODIFY]

3. **Derive Edge Cases**
   - From domain objects and actions in spec
   - Number as XXXX-IP01-EC-01
   - Categories: input boundaries, state transitions, external failures, data anomalies

4. **Write Implementation Steps**
   - Number as XXXX-IP01-IS-01
   - Include: Location, Action, Code snippet, Notes
   - Keep steps small and verifiable

5. **Define Test Cases**
   - Group by category
   - Number as XXXX-IP01-TC-01
   - Format: Description -> expected result

6. **Create Verification Checklist**
   - Number as XXXX-IP01-VC-01
   - Checkbox format for tracking
   - Include: Prerequisites, Implementation steps, Verification

7. **Verify**
   - Run /verify workflow
   - Cross-check against spec: anything forgotten?
