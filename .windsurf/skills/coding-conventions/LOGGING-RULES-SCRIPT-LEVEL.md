# Script-Level Logging Rules

Rules for script output used by Quality Assurance (QA) to verify correctness.

## Rule Index

- [LOG-SC-01](#log-sc-01-no-timestamps): No timestamps
- [LOG-SC-02](#log-sc-02-section-structure): Section structure
- [LOG-SC-03](#log-sc-03-test-case-ids): Test case IDs
- [LOG-SC-04](#log-sc-04-status-markers): Status markers
- [LOG-SC-05](#log-sc-05-status-patterns): Status patterns
- [LOG-SC-06](#log-sc-06-output-details): Output details
- [LOG-SC-07](#log-sc-07-summary-and-result): Summary and result

## Philosophy

**Goal: All failure information must be in the logs.**

A QA engineer should understand what failed and why without analyzing additional files, databases, or external data sources. The log output alone must be sufficient to diagnose the problem.

**This goal drives all rules in this document:**
- No timestamps for deterministic output ([LOG-SC-01](#log-sc-01-no-timestamps))
- Clear section structure ([LOG-SC-02](#log-sc-02-section-structure))
- Test case IDs for traceability ([LOG-SC-03](#log-sc-03-test-case-ids))
- Explicit status markers ([LOG-SC-04](#log-sc-04-status-markers))
- Consistent status patterns ([LOG-SC-05](#log-sc-05-status-patterns))
- Detailed output for debugging ([LOG-SC-06](#log-sc-06-output-details))
- Summary with pass/fail counts ([LOG-SC-07](#log-sc-07-summary-and-result))

## Related Documents

- `LOGGING-RULES.md` - General rules (LOG-GN-01 to LOG-GN-11)
- `LOGGING-RULES-USER-FACING.md` - User-facing rules (LOG-UF-01 to LOG-UF-06)
- `LOGGING-RULES-APP-LEVEL.md` - App-level rules (LOG-AP-01 to LOG-AP-05)

## Rules

### LOG-SC-01: No Timestamps

Test output must be deterministic for diff comparison. Timestamps add noise and break comparisons.

**Rationale:** Test output should be identical across runs if the code hasn't changed. Timestamps make every run different.

*BAD*:
```
[10:15:23] Running test_user_creation...
[10:15:24] PASSED
2026-03-04 10:15:25.456 Test completed
```

*GOOD*:
```
Running test_user_creation...
  OK.
Test 'test_user_creation' completed.
```

**Exception:** Selftest endpoints that stream to users may include timestamps for progress indication, but the test logic itself should not depend on them.

### LOG-SC-02: Section Structure

Use visual separators to group tests. **All test output MUST use 100-char START/END headers/footers.**

**Two formats:**

- **Test header/footer** (REQUIRED) - 100 chars total - Wraps entire test run
- **Phase header** - `===== Phase N: Name =====` (5 `=` each side) - Sub-phases within test run

**Header width:** 100 characters (same as User-Facing LOG-UF-06).

**Rationale:** Consistent boundaries make test output easy to locate in logs. 100-char width matches User-Facing conventions (LOG-UF-06).

*BAD*:
```
--- Tests ---
Test 1
Test 2
=== More Tests ===
Test 3
```

*GOOD*:
```
===================================== START: USER AUTHENTICATION TESTS =====================================
Verifying login, logout, and session management.

[ 1 / 3 ] TC-01: Login with valid credentials...
  OK.
[ 2 / 3 ] TC-02: Login with invalid password...
  OK. Correctly rejected.
[ 3 / 3 ] TC-03: Session timeout after inactivity...
  OK.

======================================= END: USER AUTHENTICATION TESTS ======================================
3 tests passed, 0 failed.
```

**With phases:**
```
======================================== START: SHAREPOINT SELFTEST ========================================

===== Phase 1: Configuration =====

[ 1 / 25 ] M1: Config validation - site URL...
  OK. site_url='https://contoso.sharepoint.com/sites/SelftestSite'
[ 2 / 25 ] M2: Config validation - certificate path...
  OK. cert_path='E:\certs\app.pfx'

===== Phase 2: Connection =====

[ 3 / 25 ] M3: Connect to SharePoint site...
  OK. Connected as 'app@contoso.onmicrosoft.com'

========================================= END: SHAREPOINT SELFTEST =========================================
25 tests passed, 0 failed.
```

### LOG-SC-03: Test Case IDs

Use prefix format for traceability: `TC-01:`, `M1:`, etc.

**Rationale:** IDs enable referencing specific tests in bug reports, documentation, and discussions.

*BAD*:
```
Testing login...
Testing logout...
Testing session...
```

*GOOD*:
```
[ 1 / 9 ] TC-01: Creating test site 'selftest_a1b2c3d4'...
[ 2 / 9 ] TC-02: Getting test site...
[ 3 / 9 ] TC-03: Updating test site...
```

**Alternative formats:**
```
[ 1 / 25 ] M1: Config validation...
[ 5 / 11 ] TC-05: Process library items...
[ 7 / 25 ] M7: Full crawl...
```

### LOG-SC-04: Status Markers

Use explicit markers for comparison and assertion results.

**Comparison:** `[equal]`, `[different]`

```
  [equal] Row count  Expected=14  Actual=14
  [different] Column count  Expected=5  Actual=4
  [equal] File size  Expected=1024  Actual=1024
```

**Assertion:** `[ok]`, `[fail]`

```
  [ok] All required fields present
  [fail] Missing 'created_date' column
  [ok] Data types match expected schema
```

**Rationale:** Explicit markers enable grep/search for failures and make status immediately visible.

### LOG-SC-05: Status Patterns

Use consistent status keyword patterns.

**Success:**
```
  OK.
  OK. 12 members resolved.
  OK. site_url='https://contoso.sharepoint.com/sites/SelftestSite'
```

**Failure:**
```
  FAIL: Delete failed: {'ok': False, 'error': 'Site not found'}
  FAIL: Validation failed -> Expected 5, got 4
  PARTIAL FAIL: 2 of 3 items processed, 1 failed.
```

**Warning:**
```
  WARNING: 2 items skipped due to missing data.
  WARNING: Using fallback configuration.
```

**Expected failure:**
```
  EXPECTED FAIL: (401) Unauthorized
  EXPECTED FAIL: (404) Site not found
```

**Skip:**
```
  SKIP: Test requires database connection.
  SKIP: Feature not enabled in test environment.
```

**Rationale:** Consistent patterns enable automated parsing and reporting.

### LOG-SC-06: Output Details

Provide enough detail to understand failures without additional investigation.

**Item lists with references:**
```
  3 items missing from output:
    Line 8: 'user_alpha@example.com'
    Line 15: 'user_beta@example.com'
    Line 22: 'user_gamma@example.com'
```

**Comparison details:**
```
  [different] Column 'date_created' format
    Expected: 'YYYY-MM-DD'
    Actual: 'MM/DD/YYYY'
    Line 1: '03/04/2026' should be '2026-03-04'
```

**Row/column counts:**
```
  Comparing CSV files...
    [equal] Row count: 523
    [different] Column count: Expected=8, Actual=7
    Missing column: 'last_modified'
```

**Rationale:** Self-contained details eliminate need to examine source files or databases.

### LOG-SC-07: Summary and Result

Always end with a summary showing counts and final result.

**Summary format:**
```
OK: X, FAIL: Y
OK: X, SKIP: Y, FAIL: Z
OK: X, EXPECTED FAIL: Y, FAIL: Z
OK: X, EXPECTED FAIL: Y, SKIP: Z, FAIL: W
```

**Final result:**
```
RESULT: PASSED
RESULT: PASSED WITH WARNINGS
RESULT: FAILED
```

**Complete summary block:**
```
===== SELFTEST COMPLETE =====
OK: 10, EXPECTED FAIL: 1, FAIL: 0
Test execution completed.
END: sites_security_scan_selftest() (12.0 secs).
```

**Extended summary:** Summary line before END footer. RESULT on final line before footer.
```
15 tests: 12 passed, 2 skipped, 1 failed. Duration: 4.2s

RESULT: FAILED
=========================================== END: SELFTEST ===========================================
```

## Complete Examples

### Example 1: Sites CRUD Selftest

```
START: sites_selftest()...

[ 1 / 9 ] TC-01: Creating test site 'selftest_a1b2c3d4'...
  OK.
[ 2 / 9 ] TC-02: Getting test site...
  OK.
[ 3 / 9 ] TC-03: Updating test site...
  OK.
[ 4 / 9 ] TC-04: Renaming test site 'selftest_a1b2c3d4' -> 'selftest_a1b2c3d4_renamed'...
  OK.
[ 5 / 9 ] TC-05: Deleting test site 'selftest_a1b2c3d4_renamed'...
  OK.
[ 6 / 9 ] TC-06: Verifying deletion...
  OK.
[ 7 / 9 ] TC-07: Creating site with underscore prefix (should fail)...
  OK.
[ 8 / 9 ] TC-08: Verifying underscore folders ignored in list...
  OK.
[ 9 / 9 ] TC-09: Cleaning up underscore folder...
  OK.

===== SELFTEST COMPLETE =====
OK: 9, FAIL: 0
END: sites_selftest() (5.0 secs).
```

### Example 2: Security Scan Selftest (with expected fail)

```
START: sites_security_scan_selftest()...

[ 1 / 11 ] TC-01: Connect to selftest site...
  OK. site_url='https://contoso.sharepoint.com/sites/SelftestSite'
[ 2 / 11 ] TC-02: Enumerate site groups...
  OK. 5 groups found.
[ 3 / 11 ] TC-03: Resolve group members...
  OK. 12 members resolved.
[ 4 / 11 ] TC-04: Query lists with HasUniqueRoleAssignments...
  OK. 3 lists with unique permissions.
[ 5 / 11 ] TC-05: Process library items...
  OK. 156 items scanned.
[ 6 / 11 ] TC-06: Detect broken inheritance...
  OK. 8 items with broken inheritance.
[ 7 / 11 ] TC-07: Generate CSV output...
  OK. 4 CSV files generated.
[ 8 / 11 ] TC-08: Access restricted site (expected fail)...
  EXPECTED FAIL: (401) Unauthorized
[ 9 / 11 ] TC-09: Verify scan statistics...
  OK. Statistics match expected values.
[ 10 / 11 ] TC-10: Cleanup test artifacts...
  OK. 4 files deleted.
[ 11 / 11 ] TC-11: Verify cleanup complete...
  OK.

===== SELFTEST COMPLETE =====
OK: 10, EXPECTED FAIL: 1, FAIL: 0
END: sites_security_scan_selftest() (12.0 secs).
```

### Example 3: Multi-Phase Crawler Selftest

```
START: crawler_selftest()...

===== Phase 1: Configuration =====
[ 1 / 25 ] M1: Config validation - CRAWLER_SELFTEST_SHAREPOINT_SITE...
  OK. site_url='https://contoso.sharepoint.com/sites/SelftestSite'
[ 2 / 25 ] M2: Config validation - Certificate path...
  OK. cert_path='E:\certs\app.pfx'

===== Phase 2: SharePoint Connection =====
[ 3 / 25 ] M3: Connect to SharePoint site...
  OK. Connected as 'app@contoso.onmicrosoft.com'
[ 4 / 25 ] M4: Enumerate document libraries...
  OK. 3 libraries found.

===== Phase 3: Create Test Data =====
[ 5 / 25 ] M5: Create test library 'SelftestLibrary'...
  OK. Library created.
[ 6 / 25 ] M6: Upload test files...
  OK. 5 files uploaded.

===== Phase 4: Crawl Operations =====
[ 7 / 25 ] M7: Full crawl...
  OK. 5 files crawled in 4.2 secs.
[ 8 / 25 ] M8: Incremental crawl (no changes)...
  OK. 0 changes detected.
[ 9 / 25 ] M9: Modify test file...
  OK. File modified.
[ 10 / 25 ] M10: Incremental crawl (1 change)...
  OK. 1 change detected.

===== Phase 5: Error Handling =====
[ 11 / 25 ] M11: Access non-existent file (expected fail)...
  EXPECTED FAIL: (404) File not found
[ 12 / 25 ] M12: Handle rate limiting...
  OK. Retry succeeded after 2 attempts.

===== Phase 6: Cleanup =====
[ 24 / 25 ] M24: Delete test library...
  OK. Library deleted.
[ 25 / 25 ] M25: Delete local artifacts...
  OK. 12 files deleted.

===== SELFTEST COMPLETE =====
OK: 24, EXPECTED FAIL: 1, FAIL: 0
Test execution completed.
END: crawler_selftest() (2 mins 3 secs).
```

### Example 4: Data Comparison Test

```
======================================= START: DATA EXPORT VALIDATION =======================================
Comparing exported CSV against expected output to verify field mapping and data integrity.

  Loading expected file 'expected_output.csv'...
    OK. 523 rows, 8 columns.
  Loading actual file 'actual_output.csv'...
    OK. 523 rows, 8 columns.

Comparing 'actual_output.csv' against 'expected_output.csv'...

  [equal] Row count  expected=523  actual=523
  [equal] Column count  expected=8  actual=8
  [equal] Column names match
  [different] Column 'date_created' format  expected='YYYY-MM-DD'  actual='MM/DD/YYYY'

1 format mismatch in 'actual_output.csv':
  Line 1: Column 'date_created' uses 'MM/DD/YYYY' instead of 'YYYY-MM-DD'

WARNING: Data matches but format differs.

3 validations run. OK: 2, WARNING: 1. Duration: 0.3s
RESULT: PASSED WITH WARNINGS
======================================== END: DATA EXPORT VALIDATION ========================================
```

### Example 5: Standalone Test Script

```
======================================= START: SHAREPOINT INTEGRATION TESTS =======================================

===== Phase 1: Connection Tests =====
Testing connection to SharePoint sites with various credentials.

[ 1 / 4 ] TC-01: Connect with valid app registration...
  OK.
[ 2 / 4 ] TC-02: Connect with expired certificate...
  OK. Correctly rejected with (401) Certificate expired.
[ 3 / 4 ] TC-03: Connect with invalid tenant...
  OK. Correctly rejected with (400) Invalid tenant ID.
[ 4 / 4 ] TC-04: Disconnect and verify cleanup...
  OK.

===== Phase 2: File Operations Tests =====
Testing upload, download, and delete operations.

[ 1 / 5 ] TC-05: Upload small file (<1MB)...
  OK.
[ 2 / 5 ] TC-06: Upload large file (50MB)...
  OK.
[ 3 / 5 ] TC-07: Download uploaded file...
  OK.
  [equal] File size  Expected=52428800  Actual=52428800
  [equal] Checksum  Expected=a1b2c3...  Actual=a1b2c3...
[ 4 / 5 ] TC-08: Delete uploaded files...
  OK.
[ 5 / 5 ] TC-09: Verify deletion...
  OK.

9 tests executed. OK: 9, FAIL: 0. Duration: 45.2s
RESULT: PASSED
======================================== END: SHAREPOINT INTEGRATION TESTS ========================================
```

### Example 6: Test with Actual Failure

```
START: data_integrity_selftest()...

[ 1 / 5 ] TC-01: Load source data...
  OK. 1000 records loaded.
[ 2 / 5 ] TC-02: Transform data...
  OK. 1000 records transformed.
[ 3 / 5 ] TC-03: Validate schema...
  FAIL: Schema validation failed
    Missing required field: 'customer_id'
    Field 'order_date' has wrong type: expected 'date', got 'string'
    2 validation errors found.
[ 4 / 5 ] TC-04: Compare with expected output...
  SKIP: Skipping due to previous failure.
[ 5 / 5 ] TC-05: Cleanup test data...
  OK.

===== SELFTEST COMPLETE =====
OK: 3, SKIP: 1, FAIL: 1

Failure details:
  TC-03: Schema validation failed
    - Missing required field: 'customer_id'
    - Field 'order_date' has wrong type: expected 'date', got 'string'

END: data_integrity_selftest() (2.3 secs).
RESULT: FAILED
```

### Example 7: Comparison with Item Lists

```
====================================== START: PERMISSION AUDIT COMPARISON ======================================
Comparing current permissions against baseline snapshot.

Loading baseline 'permissions_baseline.json'...
  156 permission entries.
Loading current 'permissions_current.json'...
  159 permission entries.

Comparing 'permissions_current.json' against 'permissions_baseline.json'...

[different] Entry count  baseline=156  current=159

3 entries added in 'permissions_current.json':
  Line 157: user='new_user@company.com' site='ProjectA' level='Contribute'
  Line 158: user='contractor@external.com' site='ProjectB' level='Read'
  Line 159: group='External Partners' site='ProjectC' level='Read'

0 entries removed from 'permissions_baseline.json'.

2 entries modified (baseline -> current):
  Line 45: user='admin@company.com' level='Contribute' -> 'Full Control'
  Line 89: group='Site Members' members added 'new_member@company.com'

Comparison complete: 3 added, 0 removed, 2 modified.
RESULT: DIFFERENCES FOUND
======================================= END: PERMISSION AUDIT COMPARISON =======================================
```
