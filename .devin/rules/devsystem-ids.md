---
trigger: always_on
---

# Document ID System

All documents and items must have unique IDs for traceability.

## Number Formats (2-digit vs 4-digit)

**2-digit `[NN]` or `[NUMBER]`** - For document-scoped items (bounded, rarely exceed 99):
- Document IDs: `CRAWLENG-SP01`, `AUTHSYST-IP01`
- Review IDs: `CRAWLENG-SP01-RV01`
- Spec items (FR, DD, IG, AC): `CRAWLENG-FR-01`
- Plan items (EC, IS, VC, TC, TK): `CRAWLENG-IP01-EC-01`, `AUTHSYST-TK01-TK-05`
- Review findings (RF): `CRAWLENG-SP01-RV01-RF-01`

**4-digit `[NNNN]`** - For tracking IDs (unbounded, accumulate over time):
- Bugs: `WEBSYSTM-BG-0001`, `GLOB-BG-0001`
- Problems: `AUTHSYST-PR-0001`
- Features: `CRAWLENG-FT-0001`
- Fixes: `CRAWLENG-FX-0002`
- Failures: `GLOB-FL-0019`

## Topic Registry

**Topic:** 7-14 uppercase letters describing component (e.g., `CRAWLENG` for Crawler Engine, `AUTHSYST` for Authentication System, `EDIRDMDL` for EDIRD Phase Model)

**Migration note (forward-only):** Topics created before 2026-06-16 may have 2-6 chars. These remain valid. All NEW topics MUST be 7-14 chars.

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
- Named concepts get their own TOPIC: `EDIRDMDL-IN01`, `STRUTPLN-SP01`
- Features get their own TOPIC: `AUTHSYST-SP01`, `CRAWLENG-IP01`
- If a document has a name, it has a TOPIC

**Example: SINGLE-PROJECT-MODE**
```
## Topic Registry
- `GLOB` - Project-mode (main spec, architecture)
- `CRAWLENG` - Crawler Engine
- `CRAWLNXT` - Version 2 Crawler
- `COMNUIFN` - Common UI Functions
- `COMNSPFN` - Common SharePoint Functions
```

**Example: MONOREPO** (first 2-3 letters = repo prefix)
```
## Topic Registry
- `CRWCORE` - CR: Crawler Core (shared libraries)
- `CRWAPIS` - CR: Crawler API (REST endpoints)
- `CRWUIFR` - CR: Crawler UI (frontend)
- `IXRCORE` - IX: Indexer Core (indexing engine)
- `IXRSCHED` - IX: Indexer Scheduler (job scheduling)
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
- `CRAWLENG-SP01` - Crawler Engine Spec 1
- `CRAWLNXT-IP01` - V2 Crawler Implementation Plan 1
- `CRAWLNXT-TP01` - V2 Crawler Test Plan 1

## Nested Document IDs

Documents inside `T##_` (Topic) or `S##_` (Step) session subfolders use nested IDs to avoid collisions when the same subject is researched in multiple sessions or contexts.

**Format:** `[TOPIC]-[SUBTOPIC]-[DOC][NN]`

**Rules:**
- `TOPIC` - The session-level or parent topic (7-14 chars, registered in ID-REGISTRY.md)
- `SUBTOPIC` - The subfolder-specific topic (7-14 chars, registered in session NOTES.md only)
- SubTopicIDs do NOT require global registration in ID-REGISTRY.md
- No collision possible: parent TOPIC is globally unique, SUBTOPIC is scoped to that parent
- Nesting applies ONLY inside `T##_` or `S##_` folders. Session root documents use flat IDs.
- Max 1 level of nesting (no `[TOPIC]-[SUB1]-[SUB2]-...`)

**When to use nested IDs:**
- Session has multiple Topic Folders exploring different angles of the same subject
- Deep research creates multiple `T##_` folders under one session topic
- Step Folders produce documents that need distinct identity from the parent

**When NOT to use (flat ID):**
- Documents at session root
- Single-focus sessions without `T##_`/`S##_` subfolders
- The subfolder topic is itself globally unique and registered in ID-REGISTRY.md

**Examples:**
```
Session topic: AIDETECT (registered in ID-REGISTRY.md)

T01_STYLMTRY_Stylometry_2026-06-16/
  _INFO_AIDETECT-STYLMTRY-01.md   → Doc ID: AIDETECT-STYLMTRY-IN01

T02_WTRMARK_Watermarking_2026-06-16/
  _INFO_AIDETECT-WTRMARK-01.md    → Doc ID: AIDETECT-WTRMARK-IN01
  _SPEC_AIDETECT-WTRMARK-01.md    → Doc ID: AIDETECT-WTRMARK-SP01

S01_SRCPROC_SourceProcessing_2026-06-16/
  _INFO_AIDETECT-SRCPROC-01.md    → Doc ID: AIDETECT-SRCPROC-IN01
```

**Tracking IDs in nested context:**
Problems, failures, and bugs inside nested folders also use the nested format:
- `AIDETECT-STYLMTRY-PR-0001` - Problem in stylometry subfolder
- `AIDETECT-WTRMARK-FL-0001` - Failure in watermarking subfolder

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
- `CRAWLENG-IP01-RV02` - Second review of CRAWLENG-IP01
- `CRAWLNXT-IN01-RV01` - First review of CRAWLNXT-IN01
- `AIDETECT-STYLMTRY-IN01-RV01` - First review of nested doc AIDETECT-STYLMTRY-IN01

## Spec-Level Item IDs (FR, IG, DD)

Defined in SPECs, referenced across IMPL and TEST plans.

**Format:** `[TOPIC]-[TYPE]-[NUMBER]`

**Types:**
- `FR` - Functional Requirement
- `IG` - Implementation Guarantee
- `DD` - Design Decision
- `AC` - Acceptance Criteria

**Examples:**
- `CRAWLENG-FR-01` - Crawler Engine Functional Requirement 1
- `CRAWLENG-DD-03` - Crawler Engine Design Decision 3
- `AUTHSYST-IG-02` - Authentication Implementation Guarantee 2

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
- `CRAWLENG-IP01-EC-01` - Crawler Engine Plan 01, Edge Case 1
- `CRAWLENG-IP01-IS-05` - Crawler Engine Plan 01, Implementation Step 5
- `AUTHSYST-TP01-TC-03` - Authentication Test Plan 01, Test Case 3
- `AIDETECT-WTRMARK-IP01-IS-03` - Nested: Watermarking subfolder, Plan 01, Step 3

## INFO Document Source IDs

All sources in INFO documents MUST have unique IDs.

**Format:** `[TOPIC]-[DOC]-SC-[SOURCE_ID]-[SOURCE_REF]`

**Components:**
- `SC` - Source type marker
- `SOURCE_ID` - Website/source mnemonic (2-6 chars)
- `SOURCE_REF` - Page/section identifier (2-12 chars, omit vowels)

**Examples:**
- `AGNTSKIL-IN01-SC-ASIO-HOME` - agentskills.io/home
- `AGNTSKIL-IN01-SC-CLAUD-SKLBP` - platform.claude.com/.../best-practices

## Session Document IDs

Session tracking documents use the session TOPIC ID. This decouples them from the session folder name, allowing folder renames without modifying contained files.

**Format:** `[TOPIC]-[TYPE]`

**Types:**
- `NOTES` - Session notes
- `PROBLEMS` - Session problems tracking
- `PROGRESS` - Session progress tracking

**Examples:**
- `AUTHSYST-NOTES`
- `AUTHSYST-PROBLEMS`
- `AUTHSYST-PROGRESS`

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
- `AUTHSYST-FT-0001` - Authentication feature request 1
- `GLOB-PR-0003` - Project-wide problem 3
- `CRAWLENG-FX-0002` - Crawler Engine fix 2
- `CRAWLENG-FL-0001` - Crawler Engine failure log entry 1
- `AIDETECT-STYLMTRY-PR-0001` - Nested: problem in stylometry subfolder

**Note:** The `[TOPIC]` links together related SPEC, IMPL, TEST, INFO, FAILS, and REVIEW documents.
