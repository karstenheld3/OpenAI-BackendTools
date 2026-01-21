---
trigger: always_on
---

# Document ID System

All documents and items must have unique IDs for traceability.

## Topic Registry

**Topic:** 2-6 uppercase letters describing component (e.g., `CRWL` for Crawler, `AUTH` for Authentication, `EDIRD` for EDIRD Phase Model)

**REQUIREMENT:** Workspace must have an `ID-REGISTRY.md` file as the authoritative source for all TOPICs, acronyms, and states to avoid conflicting topic ids. Topic ids must be unique.

**Before creating a new TOPIC or acronym:**
1. Read `ID-REGISTRY.md` to check for existing TOPICs
2. If new, add to `ID-REGISTRY.md` with description
3. Use consistent TOPIC across all related documents
4. Never create duplicate or conflicting TOPICs

**Example: SINGLE-PROJECT**
```
## Topic Registry
- `GLOB` - Project-wide (main spec, architecture)
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

## Plan-Level Item IDs (EC, IS, VC, TC)

Local to IMPL and TEST plans. Do NOT use in SPECs.

**Format:** `[TOPIC]-[DOC][NN]-[TYPE]-[NUMBER]`

**Types:**
- `EC` - Edge Case
- `IS` - Implementation Step
- `VC` - Verification Checklist item
- `TC` - Test Case

**Examples:**
- `CRWL-IP01-EC-01` - Crawler Plan 01, Edge Case 1
- `CRWL-IP01-IS-05` - Crawler Plan 01, Implementation Step 5
- `AUTH-TP01-TC-03` - Authentication Test Plan 01, Test Case 3

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

## Tracking IDs (BG, FT, PR, FX, TK, RV, FL)

For session and project tracking in PROBLEMS.md, FAILS.md, _REVIEW.md, and backlog documents.

**Format:** `[TOPIC]-[TYPE]-[NNN]` (3-digit number)

**Types:**
- `BG` - Bug (defect in existing code)
- `FT` - Feature (new functionality request)
- `PR` - Problem (issue discovered during session)
- `FX` - Fix (documented fix for a problem)
- `TK` - Task (general work item)
- `RV` - Review finding (potential issue in _REVIEW.md)
- `FL` - Failure log entry (actual failure in FAILS.md)

**Examples:**
- `SAP-BG-001` - SAP-related bug 1
- `AUTH-FT-001` - Authentication feature request 1
- `GLOB-PR-003` - Project-wide problem 3
- `CRWL-FX-002` - Crawler fix 2
- `UI-TK-015` - UI task 15
- `AUTH-RV-001` - Authentication review finding 1
- `CRWL-FL-001` - Crawler failure log entry 1

**Note:** The `[TOPIC]` links together related SPEC, IMPL, TEST, INFO, FAILS, and REVIEW documents.
