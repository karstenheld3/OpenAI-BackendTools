---
trigger: always_on
---

# Document ID System

All documents and items must have unique IDs for traceability.

## Number Formats (2-digit vs 4-digit)

**2-digit `[NN]` or `[NUMBER]`** - For document-scoped items (bounded, rarely exceed 99):
- Document IDs: `AUTH-SP01`, `CRWL-IP01`
- Review IDs: `AUTH-SP01-RV01`
- Spec items (FR, DD, IG, AC): `CRWL-FR-01`
- Plan items (EC, IS, VC, TC, TK): `CRWL-IP01-EC-01`, `AUTH-TK01-TK-05`
- Review findings (RF): `AUTH-SP01-RV01-RF-01`

**4-digit `[NNNN]`** - For tracking IDs (unbounded, accumulate over time):
- Bugs: `SAP-BG-0001`, `GLOB-BG-0001`
- Problems: `AUTH-PR-0001`
- Features: `UI-FT-0001`
- Fixes: `CRWL-FX-0002`
- Failures: `GLOB-FL-0019`

## Topic Registry

**Topic:** 2-6 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication, `EDIRD` for EDIRD Phase Model)

**REQUIREMENT:** Workspace must have an `ID-REGISTRY.md` file as the authoritative source for all TOPICs, acronyms, and states to avoid conflicting topic ids. Topic ids must be unique.

**Before creating a new TOPIC or acronym:**
1. Read `ID-REGISTRY.md` to check for existing TOPICs
2. If new, add to `ID-REGISTRY.md` with description
3. Use consistent TOPIC across all related documents
4. Never create duplicate or conflicting TOPICs

**GLOB Usage:**

Use `GLOB` for **tracking IDs only** (workspace-level failures, problems, tasks, bugs):
- `GLOB-BG-*` - Bugs in `_BugFixes` session (PROJECT-MODE, cross-cutting)
- `GLOB-FL-*` - DevSystem failures (sync errors, gate bypasses, tool issues)
- `GLOB-PR-*` - Cross-cutting problems affecting multiple components
- `GLOB-TK-*` - Workspace-wide tasks (deployments, refactoring)

**_BugFixes Session:** Uses `GLOB` prefix for all tracking IDs because bugs there span multiple components. See `/bugfix` workflow for details.

Do NOT use `GLOB` for **document IDs** (IN, SP, IP, TP, TK):
- Named concepts get their own TOPIC: `MEPI-IN01`, `EDIRD-SP01`, `STRUT-SP01`
- Features get their own TOPIC: `AUTH-SP01`, `CRWL-IP01`
- If a document has a name, it has a TOPIC

**Example: SINGLE-PROJECT-MODE**
```
## Topic Registry
- `GLOB` - Project-mode (main spec, architecture)
- `V1CR` - Version 1 Crawler
- `V2CR` - Version 2 Crawler
- `CUIF` - Common UI Functions
- `CSPF` - Common SharePoint Functions
```

**Example: MONOREPO** (first 2 letters = repo prefix)
```
## Topic Registry
- `CRCORE` - CR: Crawler Core (shared libraries)
- `CRAPI` - CR: Crawler API (REST endpoints)
- `CRUI` - CR: Crawler UI (frontend)
- `IXCORE` - IX: Indexer Core (indexing engine)
- `IXSCHED` - IX: Indexer Scheduler (job scheduling)
```

## Document IDs

Every document MUST have an ID in its header block.

**Format:** `[TOPIC]-[DOC][NN]`

**Document Types:**
- `IN` - INFO document
- `SP` - SPEC document
- `IP` - Implementation Plan
- `TP` - Test Plan
- `TK` - TASKS document
- `RV` - REVIEW document
- `LN` - LEARNINGS document

**Examples:**
- `AUTH-IN01` - Authentication Info doc 1
- `CRWL-SP01` - Crawler Spec 1
- `V2CR-IP01` - V2 Crawler Implementation Plan 1
- `V2CR-TP01` - V2 Crawler Test Plan 1

### Why IMPL and TEST, not PLAN

We use **IMPL** (Implementation Plan) and **TEST** (Test Plan) instead of generic "PLAN" to avoid term collision. "Plan" is overloaded in software development:
- Project plan (schedule, milestones)
- Task list / backlog
- Sprint plan
- Release plan
- Migration plan

IMPL and TEST provide specificity: IMPL = "how to build it", TEST = "how to verify it". This enables unambiguous references like `[WRITE-IMPL-PLAN]` vs `[WRITE-TEST-PLAN]` and distinct Doc IDs (`IP` vs `TP`).

## Review Document IDs

Reviews reference their source document with `-RV` suffix.

**Format:** `[SOURCE-DOC-ID]-RV[NN]`

**Examples:**
- `AUTH-SP01-RV01` - First review of AUTH-SP01
- `CRWL-IP01-RV02` - Second review of CRWL-IP01
- `V2CR-IN01-RV01` - First review of V2CR-IN01

## Spec-Level Item IDs (FR, IG, DD)

Defined in SPECs, referenced across IMPL and TEST plans.

**Format:** `[TOPIC]-[TYPE]-[NUMBER]`

**Types:**
- `FR` - Functional Requirement
- `IG` - Implementation Guarantee
- `DD` - Design Decision
- `AC` - Acceptance Criteria

**Examples:**
- `CRWL-FR-01` - Crawler Functional Requirement 1
- `CRWL-DD-03` - Crawler Design Decision 3
- `AUTH-IG-02` - Authentication Implementation Guarantee 2

## Plan-Level Item IDs (EC, IS, VC, TC, TK)

Local to IMPL, TEST, and TASKS plans. Do NOT use in SPECs.

**Format:** `[TOPIC]-[DOC][NN]-[TYPE]-[NUMBER]`

**Types:**
- `EC` - Edge Case
- `IS` - Implementation Step
- `VC` - Verification Checklist item
- `TC` - Test Case
- `TK` - Task (work item in TASKS document)

**Examples:**
- `CRWL-IP01-EC-01` - Crawler Plan 01, Edge Case 1
- `CRWL-IP01-IS-05` - Crawler Plan 01, Implementation Step 5
- `AUTH-TP01-TC-03` - Authentication Test Plan 01, Test Case 3
- `AUTH-TK01-TK-05` - Authentication Tasks 01, Task 5

## INFO Document Source IDs

All sources in INFO documents MUST have unique IDs.

**Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

**Components:**
- `SC` - Source type marker
- `SOURCE_ID` - Website/source mnemonic (2-6 chars)
- `SOURCE_REF` - Page/section identifier (2-12 chars, omit vowels)

**Examples:**
- `AGSK-IN01-SC-ASIO-HOME` - agentskills.io/home
- `AGSK-IN01-SC-CLAUD-SKLBP` - platform.claude.com/.../best-practices

## Session Document IDs

Session tracking documents use date-based IDs instead of TOPIC-based IDs.

**Format:** `YYYY-MM-DD_[SessionTopicCamelCase]-[TYPE]`

**Types:**
- `NOTES` - Session notes
- `PROBLEMS` - Session problems tracking
- `PROGRESS` - Session progress tracking

**Examples:**
- `2026-01-15_FixAuthenticationBug-NOTES`
- `2026-01-15_FixAuthenticationBug-PROBLEMS`
- `2026-01-15_FixAuthenticationBug-PROGRESS`

## Tracking IDs (BG, FT, PR, FX, FL)

For session and project tracking in PROBLEMS.md, FAILS.md, _REVIEW.md, and backlog documents.

**Format:** `[TOPIC]-[TYPE]-[NNNN]` (4-digit number)

**Types:**
- `BG` - Bug (defect in existing code)
- `FT` - Feature (new functionality request)
- `PR` - Problem (issue discovered during session)
- `FX` - Fix (documented fix for a problem)
- `FL` - Failure log entry (actual failure in FAILS.md)

**Examples:**
- `SAP-BG-0001` - SAP-related bug 1 (SESSION-MODE)
- `AUTH-FT-0001` - Authentication feature request 1
- `GLOB-PR-0003` - Project-wide problem 3 (PROJECT-MODE)
- `GLOB-BG-0002` - Project-wide bug 2 (PROJECT-MODE)
- `CRWL-FX-0002` - Crawler fix 2
- `CRWL-FL-0001` - Crawler failure log entry 1

**Note:** The `[TOPIC]` links together related SPEC, IMPL, TEST, INFO, FAILS, and REVIEW documents.
