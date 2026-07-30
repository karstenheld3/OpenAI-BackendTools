---
description: Run tests based on scope and context
auto_execution_mode: 1
---

# Test Workflow

Run tests based on scope and context.

## Required Skills

Invoke based on context:
- @ms-playwright-mcp for UI testing
- @write-documents for documenting problems and failures
- @coding-conventions for code verification

## Workflow

1. Determine which context applies (UI, Code, Build, Deploy)
2. Read the relevant Context-Specific section below
3. Execute context-specific steps
4. Document results (pass/fail with details)
5. If failures: fix or ask user for help

## MUST-NOT-FORGET

- Re-read TEST plan (or IMPL if no TEST) before testing
- Check SPEC for edge cases that need test coverage
- Make internal checklist of what to verify
- After each test: update checklist, note failures immediately
- Never skip documenting failures - they inform future work

## GLOBAL-RULES

- Always run tests before committing
- Use existing test infrastructure when available
- Clean up `.tmp_*` test files after completion
- Document flaky tests in PROBLEMS.md with reproduction steps

# CONTEXT-SPECIFIC

## UI Testing

Test UI functionality using Playwright MCP server.

1. Gather UI requirements from SPEC or TEST plan
2. Test using `mcp0_execute` for browser automation
3. Use `accessibilitySnapshot` for element discovery
4. Use `screenshotWithAccessibilityLabels` for visual verification
5. Document results in PROGRESS.md

## Code Testing

Test code against IMPL and TEST plans.

1. Gather test cases from TEST plan (or IMPL if no TEST)
2. Run tests using existing test framework or temporary scripts
3. For temporary scripts: prefix with `.tmp_` for cleanup
4. Verify all test cases pass
5. Document problems in PROBLEMS.md and failures in FAILS.md

## Build Testing

Test if build prerequisites are fulfilled.

1. Gather build requirements from README.md or NOTES.md
2. Verify dependencies installed (package.json, requirements.txt, etc.)
3. Verify environment variables configured
4. Test build command executes successfully
5. Document missing prerequisites in PROBLEMS.md

## Deploy Testing

Test if deployment succeeded.

1. Verify deployment target accessible
2. Test health endpoints respond
3. Test core functionality works in deployed environment
4. Verify no errors in deployment logs
5. Document deployment issues in PROBLEMS.md
