# Logging Rules

Language-agnostic output rules for Python, PowerShell, and future languages.

## Rule Index

- [LOG-GN-01](#log-gn-01-indentation): Indentation
- [LOG-GN-02](#log-gn-02-quote-paths-names-and-ids): Quote paths, names, IDs
- [LOG-GN-03](#log-gn-03-numbers-and-counters-first): Numbers and counters first
- [LOG-GN-04](#log-gn-04-duration-format): Duration format
- [LOG-GN-05](#log-gn-05-singularplural): Singular/plural
- [LOG-GN-06](#log-gn-06-property-format): Property format
- [LOG-GN-07](#log-gn-07-unknown-constant): UNKNOWN constant
- [LOG-GN-08](#log-gn-08-error-formatting): Error formatting
- [LOG-GN-09](#log-gn-09-log-before-execution): Log before execution
- [LOG-GN-10](#log-gn-10-ellipsis-usage): Ellipsis usage
- [LOG-GN-11](#log-gn-11-sentence-endings): Sentence endings
- [LOG-GN-12](#log-gn-12-no-acronyms): No acronyms

## Table of Contents

1. [Overview](#overview)
2. [Logging Philosophy](#logging-philosophy)
3. [Philosophy-to-Rules Mapping](#philosophy-to-rules-mapping)
4. [Related Documents](#related-documents)
5. [General Rules (LOG-GN)](#general-rules-log-gn)

## Overview

Four logging types serve distinct audiences with specific patterns.

**Logging Types:**
- **General (GN)** - Rules applying to all output types
- **User-Facing (UF)** - End users monitoring progress via console or Server-Sent Events (SSE) stream
- **App-Level (AP)** - Technical staff debugging and auditing via server logs
- **Script-Level (SC)** - Quality Assurance (QA) verifying correctness via selftest output

## Logging Philosophy

Each logging type has a specific goal that drives its rules.

### APAPALAN Principle

**As precise as possible, as little as necessary.**

Every log line should convey maximum information with minimum words. Avoid verbosity, filler words, and redundant phrases. Be concise but never ambiguous.

**Anti-pattern:** Cryptic abbreviations sacrifice precision for brevity.
- BAD: `P=1`, `F1=1` - unclear type, unclear meaning
- GOOD: `Precision=1.00`, `F1-Score=1.00` - full name, 2 decimals indicate float

### Principle of Least Surprise

**Logging should be predictable across all solutions.**

A developer familiar with one codebase should immediately understand logs from another. Same patterns, same formats, same structure. No variations "just because" - consistency enables faster debugging and onboarding.

### Principle of Full Disclosure

**Each log line should be understandable without context.**

Every descriptive line should read like a complete sentence. Include the subject (what), the action (verb), and the target (where/which). A reader scanning logs should not need to look at previous lines to understand the current one.

**Required context per line:**
- **What** is being processed (file name, item ID, record)
- **What action** is happening (extracting, validating, converting)
- **Enough detail** for the reader to assess complexity and estimate completion

**BAD:**
- `[ 1 / 2 ] LLM extraction run 1...`
- Missing: which file? what content? how complex?

**GOOD:**
- `[ 1 / 2 ] Calling gpt-5-mini to extract 5 records from 20 rows...`
- `[ 1 / 2 ] Extracting metadata from 'invoice_2024.pdf' (3 pages)...`
- Reader knows: file name, model, operation, complexity indicator

### Principle of Visible Structure

**Logs reveal the workflow, not just progress.**

Logs should be self-explanatory and explorative. By reading the logs, any reader can understand the inner workings and workflow mechanics without documentation.

Break operations into numbered steps `[ x / n ]` so readers can:
- Assess progress and estimate completion
- Understand the logical structure of the operation
- Learn how the system works by observation

Logging makes the developer's structured thinking visible. A non-technical user reading `[ 1 / 4 ] Connecting...`, `[ 2 / 4 ] Loading data...`, `[ 3 / 4 ] Processing...`, `[ 4 / 4 ] Saving results...` understands the entire workflow.

### Principle of Announce > Track > Report

**Every activity follows the same three-phase logging pattern:**

1. **Announce** - State what will happen in plain English with full disclosure before starting
2. **Track** - Log progress with intermediate results as nested lines
3. **Report** - State final status and results with full disclosure on separate lines

**Item-level status** (for individual operations within an activity):
Each separately logged item level action finishes with either 
- `OK.` (standalone success) or `OK: <what, details>` (success with details)
or
- `SKIP: <why>`
or
- `ERROR: <what> -> <system error>` (use ERROR for items, not FAIL)
and can log additional
- `WARNING: <non-breaking problem>`

**Activity-level status** (for the whole activity):
Each separately logged activity finishes with either
- `OK.` (standalone success) or `OK: <results>` (success with details)
or
- `SKIP: <why>`
or
- `FAIL: <fail summary>` (use FAIL for activities, not ERROR)
or 
- `PARTIAL FAIL: <fail summary>` (can continue, but some items failed)
and can log additional
- `WARNING: <non-breaking problem>` (can continue, but noticed something worth noting)
- `HINT: <actionable advice>` (user-facing and script-level, suggests what user or admin can do to fix the issue)

**Final line rule:** The last line of any activity or script must contain a status keyword (`OK.`, `FAIL:`, `PARTIAL FAIL:`, `SKIP:`) so scripts can determine success without reading the entire log.

**Parallel execution rule:** When items run in parallel, Report lines MUST carry the same identifier as their Announce line (results arrive in arbitrary order).
- BAD: `OK. Extracted 5 correct...` - which run?
- GOOD: `[ 1 / 2 ] OK. Extracted 5 correct...` - run 1 result

**Worker/process prefix rule:** Scripts with multiple workers or apps with multiple processes MUST prefix all log lines with their identity.
- Workers: `[ worker 1 ] [ 1 / 5 ] Processing 'file.pdf'...`
- Processes: `[timestamp,process 12345,request 1] START: function_name...`
- This enables log filtering and correlation when output is interleaved

**Not used for status:** `DONE`, `FINISHED`, `INFO`, `DEBUG`, etc.

```
Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
Processing 3 libraries...
  [ 1 / 3 ] Processing library 'Documents'...
    342 files retrieved.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    ERROR: Access denied -> (403) Forbidden
  [ 3 / 3 ] Processing library 'Archive'...
    SKIP: Library empty.
  FAIL: 2 libraries processed, 1 failed.
```

### Principle of Two-Level Errors (User-Facing)

**Format:** `<what failed> -> <system error>`

- **What failed** - Neutral description of the operation that did not complete. No blame, no assumptions about cause. Example: `Could not save user`
- **System error** - Exact message from the system, unchanged. Enables technical follow-up. Example: `A user with this email already exists`

*BAD:*
```
Error: A user with this email already exists.
Could not save user because email is duplicate.
```

*GOOD:*
```
Could not save user -> A user with this email already exists.
Could not connect to site -> (401) Unauthorized
File upload failed -> Connection reset by peer
```

**Why "what failed" must be neutral:** The system error reveals the cause. "Could not save user" is factual. "Could not save user because email is duplicate" assumes the cause before showing the evidence.

### Arrow Convention

**Use ` -> ` as the universal separator for:**
- Error chains: `context -> nested error -> root cause`
- Two-level errors: `summary -> exact error`
- Transformations: `'old_value' -> 'new_value'`

Context determines meaning. `Renaming 'X' -> 'Y'` is clearly a transform, `Failed -> Connection refused` is clearly an error.

Never use `-`, `:`, or other separators for these patterns.

### Script-Level Goal

**All failure information must be in the logs.**

A QA engineer should understand what failed and why without analyzing additional files, databases, or external data sources. The log output alone must be sufficient to diagnose the problem.

**This goal drives:**
- No timestamps (deterministic output for diff comparison)
- Comparison markers: `[equal]`, `[different]`
- Results on separate lines: `OK.`, `OK: <what>`, `FAIL: <what>`, `SKIP: <why>`
- Complete error context with test case IDs
- Summary with pass/fail counts

### App-Level Goal

**Logs must be human-readable AND machine-parseable.**

A developer unfamiliar with the codebase should understand what happened by reading the logs. Scripts should be able to parse logs with reasonable effort. When multiple processed are logged together, the process id must be included in a log line prefix.

**This goal drives:**
- Extended timestamps with process ID and request correlation
- START/END markers showing execution flow
- Nested indentation matching call depth
- Consistent `key='value'` property format
- Error chains preserving full context

### User-Facing Goal

**Users must always know what is happening.**

Progress indication via iteration counters, running totals, and feedback every ~10 seconds for long operations. Users should never wonder if the system is stuck.

**This goal drives:**
- Simple timestamps without technical noise
- Iteration progress `[ x / n ]` at line start
- Running counts during long operations
- 100-char START/END headers/footers for scripts
- Plain language, no jargon

## Philosophy-to-Rules Mapping

Shows how each philosophy goal maps to specific rules.

### Script-Level: "All failure info in logs"

- **Deterministic output** - LOG-SC-01: No timestamps
- **Clear pass/fail** - LOG-SC-04: Status markers
- **Traceable failures** - LOG-SC-03: Test case IDs (`TC-01:`, `M1:`)
- **Self-contained results** - LOG-SC-07: Summary with counts

### App-Level: "Human-readable AND machine-parseable"

- **Trace requests** - LOG-AP-01: Extended timestamp with PID, request N
- **Understand flow** - LOG-AP-04: START/END execution boundaries
- **Parse programmatically** - LOG-GN-02: `key='value'` property format
- **Debug failures** - LOG-AP-05: Error chains with full context

### User-Facing: "Users always know what is happening"

- **Show progress** - LOG-UF-02: Iteration `[ x / n ]`, running counts
- **Feedback timing** - LOG-UF-04: Emit every ~10 seconds
- **Plain language** - LOG-UF-03: No jargon, actionable errors
- **Activity boundaries** - LOG-UF-06: 100-char headers/footers

## Related Documents

- `LOGGING-RULES-USER-FACING.md` - LOG-UF-01 to LOG-UF-06 (6 rules)
- `LOGGING-RULES-APP-LEVEL.md` - LOG-AP-01 to LOG-AP-05 (5 rules)
- `LOGGING-RULES-SCRIPT-LEVEL.md` - LOG-SC-01 to LOG-SC-07 (7 rules)

## General Rules (LOG-GN)

12 rules that apply to ALL logging types. These ensure consistency across user-facing, app-level, and script-level output.

**Rule Index:**
- [LOG-GN-01](#log-gn-01-indentation): Indentation (2-space per level)
- [LOG-GN-02](#log-gn-02-quote-paths-names-and-ids): Quote paths, names, IDs with single quotes
- [LOG-GN-03](#log-gn-03-numbers-and-counters-first): Numbers and counters first in result messages
- [LOG-GN-04](#log-gn-04-duration-format): Duration format (ms, secs, mins, hours)
- [LOG-GN-05](#log-gn-05-singularplural): Singular/plural correctness
- [LOG-GN-06](#log-gn-06-property-format): Property format `key='value'`
- [LOG-GN-07](#log-gn-07-unknown-constant): UNKNOWN constant for missing values
- [LOG-GN-08](#log-gn-08-error-formatting): Error formatting (chains, rename, parentheses)
- [LOG-GN-09](#log-gn-09-log-before-execution): Log before execution
- [LOG-GN-10](#log-gn-10-ellipsis-usage): Ellipsis usage
- [LOG-GN-11](#log-gn-11-sentence-endings): Sentence endings
- [LOG-GN-12](#log-gn-12-no-acronyms): No acronyms in logs

### LOG-GN-01: Indentation

Use 2 spaces per indent level. Define as a global constant for consistency.

```
INDENT = "  "
```

*Example*:
```
Processing batch...
  Loading configuration...
    OK.
  Validating inputs...
    3 inputs valid.
    OK.
  Starting work...
```

### LOG-GN-02: Quote Paths, Names, and IDs

Surround file paths, resource names, and identifiers with single quotes.

*BAD*:
```
Processing file report.csv
User admin@company.com not found
Deleting folder C:\temp\data
```

*GOOD*:
```
Processing file 'report.csv'...
User 'admin@company.com' not found.
Deleting folder 'C:\temp\data'...
```

### LOG-GN-03: Numbers and Counters First

**Place numbers and iteration counters at line start.**

**Application 1: Result messages** - Start with the count, not the action verb.

*BAD*:
```
Retrieved 5 records
Successfully processed 12 items
Found 3 errors in the file
```

*GOOD*:
```
5 records retrieved.
12 items processed.
3 errors found.
```

**Application 2: Iteration counters** - Place counters at line start.

- **Top-level iterations:** `[ x / n ]` at line start
- **Nested subitems:** `( x / n )` at line start (indented)

*BAD*:
```
Processing item [ 1 / 5 ]...
Processing broken items ( 50 / 127 )...
```

*GOOD*:
```
[ 1 / 5 ] Processing item...
( 50 / 127 ) Processing broken items...
```

**Exception:** Activity announcements describe the action first.

```
Processing 5 items...
Scanning folder '/documents'...
Uploading 12 files to 'https://contoso.sharepoint.com'...
```

**Rationale:** Numbers at line start enable quick visual scanning of counts and progress.

### LOG-GN-04: Duration Format

Use consistent duration formatting. Measure and report duration for any process >30 seconds.

**Formats:**
- Milliseconds: `245 ms`
- Seconds: `1.5 secs`
- Minutes: `2 mins 30 secs`
- Hours: `1 hour 15 mins`

*BAD*:
```
Completed in 90000ms
Duration: 1.5 minutes
Time: 90 seconds
```

*GOOD*:
```
Completed in 1 min 30 secs.
END: process_batch() (1 min 30 secs).
Duration: 2 hours 15 mins.
```

### LOG-GN-05: Singular/Plural

Handle singular and plural correctly. Never use `(s)` shortcuts.

*BAD*:
```
3 file(s) found
1 item(s) processed
0 error(s) detected
```

*GOOD*:
```
3 files found.
1 item processed.
0 errors detected.
```

### LOG-GN-06: Property Format

Use `key='value'` format for key-value pairs. This makes logs parseable and values unambiguous.

**Inline properties:** Use `key='value'` within statements.

*BAD*:
```
Loading domain AiSearch from: E:\domains\config.json
Site URL: https://example.com/sites/Test
Source: SharedDocuments
```

*GOOD*:
```
Loading domain='AiSearch' from 'E:\domains\config.json'...
  Site: url='https://example.com/sites/Test'
  Library: title='Shared Documents' (id='045229b3-57de')
  OK.
```

**Additional properties in parentheses:** Add IDs, sizes, and metadata after the primary identifier.

```
Processing library 'Documents' (id='045229b3-57de')...
Downloading file 'report.pdf' (size=2.4MB, modified=2026-01-15)...
Site: url='https://contoso.sharepoint.com' (template='TeamSite')
Uploading file='data.xlsx' (size=1.2MB)...
ERROR: Failed to process 'Documents' (site='ProjectA', id='045229b3') -> Access denied
```

**Rationale:** Parenthesized properties provide context without cluttering the main message. IDs enable tracing specific items in logs.

### LOG-GN-07: UNKNOWN Constant

Use a constant for missing or unavailable values. Never use arbitrary defaults or leave None/null visible in logs.

```
UNKNOWN = '[UNKNOWN]'
```

*BAD*:
```
User: None
Library: ''
File ID: ?
Title: Unknown
```

*GOOD*:
```
  User: '[UNKNOWN]'
  Library: '[UNKNOWN]'
  File ID: '[UNKNOWN]'
  Title: '[UNKNOWN]'
```

### LOG-GN-08: Error Formatting

Concatenate nested errors with ` -> `. Include context (paths, IDs) to trace the failure. Also use ` -> ` for rename/transform operations.

**Error chains:**

*BAD*:
```
Error occurred
Connection refused
Failed
```

*GOOD*:
```
Failed to upload file 'report.pdf' -> Connection refused -> Server timeout after 30s
Processing 'config.json' failed -> JSON parse error -> Unexpected token at line 15
```

**Rename/transform operations:**
```
Renaming 'site_001' -> 'site_001_archived'...
Moving 'old_folder' -> 'archive/old_folder'...
```

**Additional info in parentheses:**
```
Processing library 'Documents' (id='045229b3-57de')...
Downloading file 'report.pdf' (size=2.4MB, modified=2026-01-15)...
```

### LOG-GN-09: Log Before Execution

Always log what will happen BEFORE starting code that could hang or take long. If it hangs, the last log line shows where.

*BAD*:
```
[nothing logged, then hangs]
Connection established.
```

*GOOD*:
```
Connecting to 'https://sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
Downloading file 'report.pdf' (size=2.4MB)...
  OK.
```

### LOG-GN-10: Ellipsis Usage

Use ellipsis (`...`) for ongoing actions. Never use ellipsis on result lines.

*BAD*:
```
5 files found...
Processing complete...
```

*GOOD*:
```
Processing files...
5 files found.
Processing complete.
```

### LOG-GN-11: Sentence Endings

**Write proper English sentences.** Every log line ends with punctuation:
- **Activity announcements** (something is starting/in progress) end with `...`
- **Results/statements** (something completed/found/failed) end with `.`

*BAD:*
```
Connecting to server
5 files retrieved...
Processing
User not found
```

*GOOD:*
```
Connecting to server...
5 files retrieved.
Processing complete.
User 'admin@company.com' not found.
```

### LOG-GN-12: No Acronyms

**NEVER use acronyms alone in logs.** Always spell out the full term first, with the acronym in parentheses.

This is especially critical for user-facing logs where readers may not know technical abbreviations.

**Format:** `Full Term (ACRONYM)`

**This also applies to naming:** Environment variables, configuration settings, and other identifiers should use full names, not acronyms.
- BAD: `OBO_ENABLED`, `SPO_TENANT_ID`
- GOOD: `ON_BEHALF_OF_ENABLED`, `SHAREPOINT_ONLINE_TENANT_ID`

*BAD:*
```
Authenticating via OBO...
Connecting to SPO...
Using MI for authentication...
Calling AOI Service...
```

*GOOD:*
```
Authenticating via On Behalf Of (OBO)...
Connecting to SharePoint Online (SPO)...
Using Managed Identity (MI) for authentication...
Calling Azure OpenAI (AOI) Service...
```

**Rationale:** Acronyms are insider knowledge. Users, support staff, and future developers may not recognize them. Spelling out the term first ensures everyone understands the log, while the parenthesized acronym allows correlation with documentation that uses the short form.

## Complete Example

Showing Announce > Track > Report with proper status patterns:

```
Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  OK. Connected in 1.2 secs.
Loading libraries...
  3 libraries found.
  OK.
Processing 3 libraries...
  [ 1 / 3 ] Processing library 'Documents'...
    Scanning files...
    ( 100 / 342 ) items retrieved...
    ( 200 / 342 ) items retrieved...
    342 files retrieved.
    12 added, 3 changed, 0 removed.
    OK.
  [ 2 / 3 ] Processing library 'Reports'...
    Scanning files...
    45 files retrieved.
    ERROR: Failed to process file 'budget.xlsx' -> Access denied -> User lacks read permission
  [ 3 / 3 ] Processing library 'Archive'...
    SKIP: Library empty.
  PARTIAL FAIL: 2 libraries processed, 1 failed.
Renaming 'site_backup' -> 'site_backup_2026-03-04'...
  OK.
```
