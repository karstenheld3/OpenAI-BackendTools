# User-Facing Logging Rules

Rules for end-user visible output via console or Server-Sent Events (SSE) stream.

## Rule Index

- [LOG-UF-01](#log-uf-01-timestamp-format): Timestamp format
- [LOG-UF-02](#log-uf-02-progress-indicators): Progress indicators
- [LOG-UF-03](#log-uf-03-messages-and-results): Messages and results
- [LOG-UF-04](#log-uf-04-feedback-timing): Feedback timing
- [LOG-UF-05](#log-uf-05-context-display): Context display
- [LOG-UF-06](#log-uf-06-activity-boundaries): Activity boundaries

## Philosophy

**Goal: Users must always know what is happening.**

User-facing logs are self-explanatory and explorative. By reading the logs, users understand the inner workings and workflow mechanics without documentation. Users should never wonder if the system is stuck or what it's doing.

**Core requirements:**
- Numbered steps `[ x / n ]` reveal the workflow structure
- Progress indication via iteration counters and running totals
- Feedback every ~10 seconds for long operations
- Plain language that non-technical users can follow
- **Full Disclosure:** Every log section must be self-contained. Include filenames, URLs, and identifiers so readers don't need to scroll up for context.

**MUST NOT use log levels:** Never use `INFO`, `DEBUG`, `WARN` prefixes. These are for App-Level logging only. User-facing logs use plain language with status keywords: `OK`, `FAIL`, `PARTIAL FAIL`, `SKIP` or `SKIPPED`, `ERROR:`, `WARNING:`, `HINT:`.

**This goal drives all rules in this document:**
- Simple timestamps without technical noise ([LOG-UF-01](#log-uf-01-timestamp-format))
- Iteration progress at line start ([LOG-UF-02](#log-uf-02-progress-indicators))
- Plain language, no jargon ([LOG-UF-03](#log-uf-03-messages-and-results))
- Feedback timing requirements ([LOG-UF-04](#log-uf-04-feedback-timing))
- Context hierarchy display ([LOG-UF-05](#log-uf-05-context-display))

## Related Documents

- `LOGGING-RULES.md` - General rules (LOG-GN-01 to LOG-GN-11)
- `LOGGING-RULES-APP-LEVEL.md` - App-level rules (LOG-AP-01 to LOG-AP-05)
- `LOGGING-RULES-SCRIPT-LEVEL.md` - Script-level rules (LOG-SC-01 to LOG-SC-07)

## Rules

### LOG-UF-01: Timestamp Format

Use `[YYYY-MM-DD HH:MM:SS]` format. Always include date AND time. No process ID, no milliseconds.

**Rationale:** Date is essential for log files that span multiple days or are reviewed later. Consistency with app-level logging.

*BAD*:
```
[10:15:23] Starting scan...
2026-03-04 10:15:23.456 [PID:1234] [INFO] Starting scan
[2026-03-04T10:15:23.456Z] Connecting...
10:15:23.456 - Processing files
```

*GOOD*:
```
[2026-03-04 10:15:23] Starting scan...
[2026-03-04 10:15:24] Connecting to site...
[2026-03-04 10:15:25]   3 libraries found.
```

**SSE Stream Format:**
```
[2026-03-04 10:15:23] Crawling site 'https://contoso.sharepoint.com/sites/ProjectA'...
[2026-03-04 10:15:24]   3 libraries found.
[2026-03-04 10:15:30]   OK. Crawl complete in 7.2 secs.
```

### LOG-UF-02: Progress Indicators

**Iteration format:** `[ x / n ]` with spaces, at line start.

```
[ 1 / 5 ] Processing 'Document A'...
[ 2 / 5 ] Processing 'Document B'...
[ 3 / 5 ] Processing 'Document C'...
```

**Retry format:** `( x / n )` inline or as indented subitem.

*Inline:*
```
( 1 / 3 ) Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
( 2 / 3 ) Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  OK. Connected to 'https://contoso.sharepoint.com/sites/ProjectA'.
```

*Subitem:*
```
Uploading file 'report.pdf'...
  ( 1 / 3 ) Connection timeout, retrying...
  ( 2 / 3 ) Connection timeout, retrying...
  ( 3 / 3 ) Upload successful.
```

**Running count:** For long operations, show progress during retrieval using parentheses `( x / n )`.

```
( 100 / 342 ) items retrieved...
( 200 / 342 ) items retrieved...
( 300 / 342 ) items retrieved...
342 files retrieved.
```

*Or with ratio:*
```
( 100 / 342 ) Retrieving items...
( 200 / 342 ) Retrieving items...
342 files retrieved.
```

**Waiting:** Show delay reason and attempt count.

```
( 1 / 3 ) Waiting 30 seconds for rate limit...
( 2 / 3 ) Waiting 30 seconds for rate limit...
Resuming upload...
```

### LOG-UF-03: Messages and Results

**Plain language:** No technical jargon. Users should understand without developer knowledge.

*BAD*:
```
HTTP 200 OK response received
SQLException: constraint violation on PK_Users
Thread pool exhausted, queuing request
NullReferenceException at line 245
```

*GOOD:*
```
Scan complete: 156 users found.
Could not save user -> A user with this email already exists.
Request queued -> Server busy, retrying in 30 seconds.
An error occurred while processing request -> Internal server error (500).
```

**Actionable errors:** Two-level format - defensive summary + exact error.

*BAD:*
```
Error: Connection refused
Error: ENOENT
Error: 403
```

*GOOD:*
```
Could not connect to server -> Connection refused
File not found -> ENOENT - No such file or directory
Access denied to resource -> (403) Forbidden
```

**Skipping:** Always explain why items are skipped.

```
SKIP: 12 files not embeddable.
SKIP: 1 file exceeds size limit (>100MB).
SKIP: Already up to date.
```

**File operations:** Show what is being written.

```
Writing 152 lines to '01_SiteContents.csv'...
  OK: File '01_SiteContents.csv' written.
Writing 'Summary.csv'...
  OK.
```

**Summary:** Always end with counts. Use activity-level status keywords.

```
OK. 3 libraries processed. 56 added, 3 changed.
PARTIAL FAIL: 2 libraries processed, 1 failed.
FAIL: Could not complete export -> Connection lost.
```

**Multi-line warning:** For destructive operations, show details.

```
IMPORTANT: This script will permanently DELETE all versions
- except for the newest version
- except if the time to the next version is more than 15 minutes
Press any key to continue...
```

### LOG-UF-04: Feedback Timing

**Requirement:** Emit progress at least every ~10 seconds for long operations.

Users should never wonder if the system is stuck. For operations that might take more than 10 seconds, emit intermediate progress.

*BAD (no feedback for 2 minutes):*
```
[2026-03-04 10:15:23] Starting large file download...
[2026-03-04 10:17:45] Download complete.
```

*GOOD (regular feedback):*
```
[2026-03-04 10:15:23] Starting large file download...
[2026-03-04 10:15:33]   10% downloaded (12MB / 120MB)...
[2026-03-04 10:15:43]   20% downloaded (24MB / 120MB)...
[2026-03-04 10:15:53]   30% downloaded (36MB / 120MB)...
...
[2026-03-04 10:17:45] Download complete. 120MB in 2 mins 22 secs.
```

### LOG-UF-05: Context Display

Show hierarchy to help users understand where they are in the operation.

**Format:** Site > Library > Folder

```
Site: 'https://contoso.sharepoint.com/sites/ProjectA'
  Library: 'Shared Documents'
    Folder: 'Reports/2026'
      Processing 42 files...
```

**With iteration:**
```
Job [ 1 / 5 ] 'https://contoso.sharepoint.com/sites/ProjectA'
  Connecting to site...
  Loading subsites...
  3 subsites found.
    ( 1 / 3 ) Subsite 'https://contoso.sharepoint.com/sites/ProjectA/TeamB'
      4 lists found.
```

### LOG-UF-06: Activity Boundaries

**Every activity must clearly indicate start and end.**

**User-Facing and Scripts: 100-char headers/footers (REQUIRED)**

All user-facing output and standalone scripts MUST use 100-character START/END headers and footers.

**Header width:** 100 characters.

```
============================== START: SHAREPOINT PERMISSION SCANNER ==============================
2026-03-04 14:30:00

[... script output ...]

================================ END: SHAREPOINT PERMISSION SCANNER ================================
2026-03-04 14:35:23 (5 mins 23 secs)
```

**Simple operations within scripts:** Use indentation and status keywords, no additional markers needed.

```
============================== START: SHAREPOINT CRAWLER ==============================
2026-03-04 14:30:00

Crawling site 'https://contoso.sharepoint.com/sites/ProjectA'...
  3 libraries found.
  OK. 342 files processed in 7.0 secs.

RESULT: OK
================================ END: SHAREPOINT CRAWLER ================================
2026-03-04 14:30:07 (7.0 secs)
```

**Rationale:** Users must always know when something begins and when it finishes. 100-char headers/footers make script boundaries visible in long log files.

**Note:** App-Level logging uses simple `START:` / `END:` markers per LOG-AP-04.

## Complete Examples

### Example 1: SharePoint Scan

```
[2026-03-04 14:30:00] Crawling site 'https://contoso.sharepoint.com/sites/ProjectA'...
[2026-03-04 14:30:01]   3 libraries found.
[2026-03-04 14:30:01] [ 1 / 3 ] Processing 'Documents'...
[2026-03-04 14:30:02]   ( 100 / 342 ) items retrieved...
[2026-03-04 14:30:03]   ( 200 / 342 ) items retrieved...
[2026-03-04 14:30:04]   342 files retrieved.
[2026-03-04 14:30:04]   12 added, 3 changed, 0 removed.
[2026-03-04 14:30:04]   OK.
[2026-03-04 14:30:05] [ 2 / 3 ] Processing 'Reports'...
[2026-03-04 14:30:06]   45 files retrieved.
[2026-03-04 14:30:06]   OK.
[2026-03-04 14:30:07] [ 3 / 3 ] Processing 'Archive'...
[2026-03-04 14:30:07]   SKIP: Library empty.
[2026-03-04 14:30:08] OK. 2 libraries processed. 57 added, 3 changed.
[2026-03-04 14:30:08] Crawl complete in 8.0 secs.
```

### Example 2: File Upload with Retry

```
[2026-03-04 10:00:00] Uploading 5 files to 'Documents'...
[2026-03-04 10:00:01] [ 1 / 5 ] Uploading 'report.pdf'...
[2026-03-04 10:00:02]   ( 1 / 3 ) Connection timeout, retrying...
[2026-03-04 10:00:05]   ( 2 / 3 ) Connection timeout, retrying...
[2026-03-04 10:00:08]   ( 3 / 3 ) Upload successful.
[2026-03-04 10:00:08] [ 2 / 5 ] Uploading 'data.xlsx'...
[2026-03-04 10:00:09]   OK.
[2026-03-04 10:00:10] [ 3 / 5 ] Uploading 'image.png'...
[2026-03-04 10:00:11]   OK.
[2026-03-04 10:00:12] [ 4 / 5 ] Uploading 'archive.zip'...
[2026-03-04 10:00:13]   SKIP: File too large (>100MB).
[2026-03-04 10:00:14] [ 5 / 5 ] Uploading 'notes.txt'...
[2026-03-04 10:00:15]   OK.
[2026-03-04 10:00:15] 4 files uploaded, 1 skipped.
```

### Example 3: Permission Scanner

```
Job [ 1 / 5 ] 'https://contoso.sharepoint.com/sites/ProjectA'
  Connecting to 'https://contoso.sharepoint.com/sites/ProjectA'...
  Loading subsites...
  3 subsites found.
  Loading site groups...
  8 groups found in site collection.
    4 lists found.
    5420 items found, 127 with broken permissions.
      ( 50 / 127 ) Processing broken items...
      ( 100 / 127 ) Processing broken items...
    152 lines written to: '01_SiteContents.csv'
  OK: File '02_SiteGroups.csv' written.
Job [ 2 / 5 ] 'https://contoso.sharepoint.com/sites/ProjectB'
  Connecting to 'https://contoso.sharepoint.com/sites/ProjectB'...
  FAIL: (401) Unauthorized
```

### Example 4: Data Export Summary

```
[2026-03-04 10:15:23] Starting data export...
[2026-03-04 10:15:24] [ 1 / 3 ] Exporting 'Sales Data'...
[2026-03-04 10:15:26]   523 records exported.
[2026-03-04 10:15:26] [ 2 / 3 ] Exporting 'Customer List'...
[2026-03-04 10:15:27]   724 records exported.
[2026-03-04 10:15:28] [ 3 / 3 ] Exporting 'Inventory'...
[2026-03-04 10:15:28]   Skipping 3 items because they have no data.
[2026-03-04 10:15:29]   247 records exported.
[2026-03-04 10:15:29] Export complete: 3 files created, 1,494 records total.
```

### Example 5: Destructive Operation Warning

```
=================================== START: DELETE FILE VERSIONS ===================================
PowerShell: 7.4.1 | PnP.PowerShell: 2.4.0

IMPORTANT: This script will permanently DELETE all versions
- except for the newest version
- except if the time to the next version is more than 15 minutes
Press any key to continue...

Job [ 1 / 3 ] 'https://contoso.sharepoint.com/sites/Archive'
  Connecting to site...
  Loading document libraries...
  2 libraries found.
  ( 1 / 2 ) Scanning 'Documents'...
    1250 files retrieved.
    Scanning versions...
    SUMMARY: 1250 files with 3420 versions, 892 can be deleted.
    Size: 4.2 GB total (38.5% in versions), 1.1 GB (26.2%) can be deleted.
```
