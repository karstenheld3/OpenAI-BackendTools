---
description: Verify factual claims in documents against external reality
auto_execution_mode: 3
---

# Fact-Check Workflow

Verify factual claims in documents by extracting sources, facts, and conclusions, then checking each against external reality.

**Goal**: Review document with all factual claims verified, verdicts assigned, and findings reported in `[filename]_REVIEW.md`

**Why**: AI agents trust all text unconditionally. No existing workflow crosses the gap from claims-about-reality to observed-reality. `/verify` checks conformance but trusts upstream documents as correct. A fabricated claim in a SPEC propagates through IMPL to code without detection.

**Scope**: Factual truth only. Use `/verify` for rule conformance, formatting, naming. Zero overlap.

## Required Skills

- @skills:write-documents for review document output (use `FACT-CHECK_REVIEW_TEMPLATE.md`)
- @skills:deep-research for source collection tools (use `RESEARCH_TOOLS.md`)
- @skills:pdf-tools for PDF processing pipeline
- @skills:llm-transcription for image and scanned document transcription
- @skills:ms-playwright-mcp for web page access and full-page capture

## MUST-NOT-FORGET

- **NEVER modify the original document, code, or any file other than the review output** - produce `[filename]_REVIEW.md` only. This workflow is a JUDGE, not a fixer. Corrections happen in `/implement` after `/reconcile` approval. If you feel the urge to fix something, write it as a finding instead.
- Consensus is not evidence - multiple sources agreeing adds zero value unless they independently observed the actual system
- Documentation is secondary, not primary - the shipped product (running API, source code, test output) is the primary source
- Trust hierarchy: observed behavior > source code > official docs > community sources > LLM output
- Source verification MUST happen before fact verification - a hallucinated source invalidates all facts citing it
- Download source files to `_DOWNLOADS_gitignore/` (not checked in)
- Transcribe sources to `_SOURCES/` (checked in - preserves evidence)
- Full-page screenshots MUST use `fullPage: true, type: "jpeg"` per @skills:ms-playwright-mcp
- Run `/verify` after workflow complete

## Mandatory Re-read

**SESSION-MODE**: NOTES.md, PROBLEMS.md, PROGRESS.md, FAILS.md

**PROJECT-MODE**: README.md, !NOTES.md or NOTES.md, FAILS.md

## Prerequisites

- Target document exists and is readable
- Network access available if document references external URLs

## GLOBAL-RULES

Apply to ALL input types before context-specific steps.

1. Trust hierarchy governs ALL verification: observed behavior > source code > official docs > community sources > LLM output. Every verification must push toward the left of this chain
2. Non-destructive: never modify the original. All output goes to `[filename]_REVIEW.md` and source folders
3. Source-first order: verify sources BEFORE facts, facts BEFORE conclusions. One source failure cascades to all citing facts
4. Autonomous execution: no confirmation gates. Extract, materialize, verify, and report without pausing
5. Graceful degradation: if a source is inaccessible, assign `inaccessible` verdict and continue. Never abort because one source failed
6. Unfalsifiable claims (opinions, subjective assessments) are flagged but never verified
7. Privacy gate: review document is general-purpose. All examples and evidence descriptions must use generic references
8. Triage-informed priority: scan for hallucination triage signals before deep verification. Seven signals: generic phrasing (SOCAS-08), stale info (SOCAS-12), empty structure (SOCAS-13), vague claims (AP-PR-07), wrong terms (MW-WC-01), assumptions stated as facts (SOCAS-10), unsupported conclusions (SOCAS-06). Facts matching triage signals get priority, but ALL facts get verdicts

# CONTEXT-SPECIFIC

## INFO / Research Documents

High claim density. Most claims should have source citations.

1. Verify every sourced claim and existence claim
2. Flag unsourced factual claims as priority findings
3. Check `[VERIFIED]` and `[ASSUMED]` labels against actual verification status
4. Cross-check version numbers, dates, and URLs for staleness
5. Verify cited sources still exist and still say what the document claims

## SPEC Documents

Functional requirements may rest on factual assumptions about external systems.

1. Verify Functional Requirement (FR) and Design Decision (DD) factual basis against actual systems
2. Check existence claims (methods, parameters, endpoints referenced in FRs)
3. Verify quantitative claims (timeouts, limits, thresholds) against actual system behavior
4. Flag design decisions based on unverified assumptions about external behavior

## IMPL / TEST Documents

Lower claim density. Focus on concrete technical claims.

1. Verify dependency claims (packages, versions, APIs exist as described)
2. Verify code path assumptions (referenced functions, methods, signatures exist)
3. Check configuration claims against actual configuration files
4. Verify test expectations against actual system behavior

## Code Files

Code is both a claim and a testable artifact.

1. Verify claims IN code: comments and docstrings vs actual behavior
2. Verify claims ABOUT code: does referenced functionality exist?
3. Verify dependency claims: imports, method signatures, parameter names
4. Verify configuration claims: referenced config values, environment variables

## Workflow / Skill Documents

Operational claims about tools, file locations, and system behavior.

1. Verify tool availability claims (binaries, scripts, APIs)
2. Verify file path and location claims
3. Verify behavioral claims about referenced workflows or skills
4. Check if referenced rule IDs exist in their source files

## External / Unknown Document Type

1. Extract all URL and file references as sources
2. Extract all factual statements
3. Apply standard pipeline (materialize, verify, report)

## No Context Match

Treat as External document type and apply standard pipeline.

# EXECUTION

## Phase 1: Extract

Scan the document for checkable items. Three extraction passes.

1. **Extract sources**: Scan for URLs, file paths, document references (`_INFO_*.md`, `_SPEC_*.md`), source ID citations (`[TOPIC-SC-*]`), inline citations ("According to...", "The documentation states..."), verification labels (`[VERIFIED]`, `[ASSUMED]`)
2. **Extract facts**: Scan for falsifiable factual statements. Classify each:
   - `factual` - direct assertion about system behavior
   - `sourced-attribution` - claim attributed to a specific source
   - `quantitative` - numerical claim (versions, thresholds, measurements)
   - `existence` - claim about presence/absence of a feature, method, file
   - `unfalsifiable` - subjective assessment (flag, do not verify)
3. **Extract conclusions**: Scan for derived statements (recommendations, assessments). Identify supporting facts for each. Indicators: "Therefore...", "This means...", "As a result...", recommendation language, claims in Summary or Conclusions sections
4. **Link**: Associate each fact with its cited sources. Flag unsourced facts

Output: numbered source list [S01, S02, ...], fact list [F01, F02, ...], conclusion list [C01, C02, ...]

## Phase 2: Materialize

Download and transcribe URL sources to local storage for reliable verification.

1. Create `_DOWNLOADS_gitignore/` and `_SOURCES/` subfolders adjacent to review output location
2. For each URL source:
   - Web pages: `read_url_content` (preferred) or ms-playwright-mcp `browser_navigate` + `browser_snapshot` (fallback). Save text to `_SOURCES/[SOURCE_ID]_[name].md`. Visual archive: `browser_take_screenshot(fullPage: true, type: "jpeg")` to `_DOWNLOADS_gitignore/`
   - PDFs: download to `_DOWNLOADS_gitignore/[SOURCE_ID]_[name].pdf`, process via @skills:pdf-tools (`pdftotext` for text-native, `convert-pdf-to-jpg` + @skills:llm-transcription for scanned). Save transcription to `_SOURCES/`
   - Images: download to `_DOWNLOADS_gitignore/`, transcribe via @skills:llm-transcription to `_SOURCES/`
3. For file/document sources: read directly (no download needed)
4. If access fails after 2 retries: search archive.org or cached version. If none found: mark as `inaccessible`, proceed
5. Max 3 inaccessible sources before logging a warning in the review

Output: materialized source content in `_SOURCES/` and `_DOWNLOADS_gitignore/`

## Phase 3: Verify

Verify in source-first order. Cascading invalidation applies.

### 3.1 Verify Sources

For each source, verify it exists and contains what the document claims:
- URL sources: verify against materialized local copy in `_SOURCES/`
- File sources: check file exists at referenced path, read and compare
- Document sources: check DevSystem document exists, read and compare
- Implicit sources: flag as `unsourced`

Assign verdict: `confirmed`, `not-found`, `changed`, `inaccessible`

### 3.2 Verify Facts

Partition facts by source for efficient verification (one source read serves all citing facts). Apply triage signals (GLOBAL-RULE 8) for priority ordering.

- Facts citing confirmed sources: verify each against source content
- Facts citing failed sources: assign `weakened` (cascading invalidation)
- Unsourced facts: attempt independent verification (web search, file reading, code inspection, API testing)
- A fact citing multiple sources is `weakened` only if ALL its sources are non-confirmed. One confirmed source can rescue a fact

Assign verdict: `confirmed`, `refuted`, `unverifiable`, `unsourced`, `weakened`

### 3.3 Review Conclusions

For each conclusion, evaluate based on supporting fact verdicts:
- All facts confirmed + reasoning sound → `confirmed`
- Any fact refuted → `refuted` (chain breaks)
- Any fact weakened or unverifiable → `weakened`
- Supporting facts not identified → `unsupported`

## Phase 4: Report

Generate `[filename]_REVIEW.md` following @skills:write-documents `FACT-CHECK_REVIEW_TEMPLATE.md`.

1. Header: Doc ID (`[SOURCE-DOC-ID]-RV[NN]`), review date, context summary (document type, source/fact/conclusion counts)
2. Fact-Check Summary: verdict counts per category, overall recommendation
3. Source Verdicts: confirmed and failed sources with `_SOURCES/` references for materialized copies
4. Fact Verdicts: grouped by severity
   - Critical = refuted
   - High = weakened or unsupported
   - Medium = unverifiable
   - Low = unsourced
5. Conclusion Verdicts: with supporting fact references
6. Unfalsifiable Claims: flagged items (separate section, not verified)
7. Recommendations: Must Do, Should Do, Could Do

Recommendation thresholds:
- Any `refuted` fact → STOP AND FIX
- Multiple `weakened` or `unsupported` → PROCEED WITH CAUTION
- All confirmed or minor unsourced → PROCEED

## Gate Check: FACT-CHECK→COMPLETE

- [ ] Every source received exactly one verdict
- [ ] Every falsifiable fact received exactly one verdict
- [ ] Every conclusion received exactly one verdict
- [ ] Cascading invalidation applied: failed sources → weakened facts → weakened/refuted conclusions
- [ ] Unfalsifiable claims flagged separately, not given truth verdicts
- [ ] Review file created, no original files modified
- [ ] `_SOURCES/` contains materialized evidence for URL sources

Pass: Complete | Fail: Review missed items

## Stuck Detection

If 3 consecutive verification attempts fail for the same source or fact:
1. Document in PROBLEMS.md
2. Assign `unverifiable` verdict with reason
3. Continue with remaining items

# FINALIZATION

## Verification

Run `/verify` on generated `[filename]_REVIEW.md` to check:
1. Review follows `FACT-CHECK_REVIEW_TEMPLATE.md` structure
2. All verdict categories used correctly
3. No original files modified
4. MUST-NOT-FORGET (MNF) items addressed

## Output

- `[filename]_REVIEW.md` - fact-check review with all verdicts and recommendations
- `_SOURCES/` - transcribed source content (checked in, naming: `[SOURCE_ID]_[descriptive-name].md`)
- `_DOWNLOADS_gitignore/` - raw downloads (not checked in, naming: `[SOURCE_ID]_[original-name].[ext]`)
