---
description: Create test plan from spec
auto_execution_mode: 1
---

# Write Test Plan Workflow

Create test plans from specifications.

## Required Skills

Invoke these skills before proceeding:
- @write-documents for document structure and formatting rules

## Prerequisites

- Specification exists (`_SPEC_[COMPONENT].md`)
- Implementation plan exists (`_IMPL_[COMPONENT].md`) - optional
- Read @write-documents skill

## Steps

1. **Create Test Plan File**
   - Create `_TEST_[COMPONENT].md` in session folder
   - Header block with Goal, Target file, Dependencies

2. **Define Test Strategy**
   - Approach: unit, integration, snapshot-based, manual
   - What to test vs what to skip (with reasons)

3. **Create Test Priority Matrix**
   - MUST TEST: Critical business logic
   - SHOULD TEST: Important workflows
   - DROP: Not worth testing (external deps, UI-only)
   - Include testability and effort estimates

4. **Define Test Data**
   - Required test fixtures
   - Setup and teardown procedures
   - Sample inputs and expected outputs

5. **Write Test Cases**
   - Group by category
   - Number as XXXX-TC-01
   - Format: Description -> ok=true/false, expected result

6. **Define Test Phases**
   - Ordered execution sequence
   - Dependencies between phases

7. **Create Verification Checklist**
   - All test cases listed with checkboxes
   - Manual verification steps if needed

8. **Verify**
   - Run /verify workflow
   - Check coverage against spec requirements
