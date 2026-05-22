---
name: coding-conventions
description: Provides coding style rules for Python and PowerShell. Apply when writing, editing, reviewing, or debugging code.
---

# Coding Conventions

**Code quality standard:** All code MUST follow:
- `MECT_CODING_RULES.md` - Precision, brevity, consistency, naming design, documentation (MECT + APAPALAN for code)

Read before writing or reviewing any code.

## Files

MECT_CODING_RULES.md - Code quality (precision, brevity, consistency, naming, documentation)
PYTHON-RULES.md - Python (formatting, imports, naming, comments)
JSON-RULES.md - JSON (field naming, 2-space indent)
WORKFLOW-RULES.md - Workflow documents (structure, token optimization)

## Logging Files (read when writing or reviewing logging/output code)

LOGGING-RULES.md - General logging rules, philosophy, type overview (read first)
LOGGING-RULES-APP-LEVEL.md - System/debug logging for technical staff (LOG-AP rules)
LOGGING-RULES-SCRIPT-LEVEL.md - Script output for QA and automation verification (LOG-SC rules)
LOGGING-RULES-USER-FACING.md - End-user visible output via console or SSE (LOG-UF rules)

## Tools

reindent.py - Convert Python indentation to target spaces

```powershell
python reindent.py folder/ --to 2 --recursive
python reindent.py folder/ --to 2 --recursive --dry-run
python reindent.py script.py --to 2
```
