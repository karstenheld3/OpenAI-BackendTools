# [Filename]_REVIEW.md

**Doc ID**: [SOURCE-DOC-ID]-RV[NN]
<!-- Topic IDs: 7-14 uppercase chars. Review IDs use source doc ID + -RV suffix. -->
**Goal**: Verify factual claims against external reality and assign verdicts
**Timeline**: Created YYYY-MM-DD
**Reviewed**: [YYYY-MM-DD HH:MM]
**Context**: Fact-check of [document description]
**Input**: [document filename and path]

## Table of Contents

1. [Fact-Check Summary](#fact-check-summary)
2. [Source Verdicts](#source-verdicts)
3. [Fact Verdicts](#fact-verdicts)
4. [Conclusion Verdicts](#conclusion-verdicts)
5. [Unfalsifiable Claims](#unfalsifiable-claims)
6. [Recommendations](#recommendations)
7. [Document History](#document-history)

## Fact-Check Summary

- **Sources**: [N] total ([n] confirmed, [n] not-found, [n] changed, [n] inaccessible)
- **Facts**: [N] total ([n] confirmed, [n] refuted, [n] unverifiable, [n] unsourced, [n] weakened)
- **Conclusions**: [N] total ([n] confirmed, [n] refuted, [n] weakened, [n] unsupported)
- **Unfalsifiable**: [N] flagged (not verified)
- **Recommendation**: STOP AND FIX / PROCEED WITH CAUTION / PROCEED

<!-- Recommendation thresholds:
- Any refuted fact -> STOP AND FIX
- Multiple weakened or unsupported -> PROCEED WITH CAUTION
- All confirmed or minor unsourced -> PROCEED -->

## Source Verdicts

### Confirmed Sources

<!-- One entry per confirmed source. Include _SOURCES/ reference for materialized copies. -->

- **S01** `confirmed` - [reference or URL] -> `_SOURCES/S01_[name].md`
  - Content matches document claims

### Failed Sources

<!-- Group by verdict: not-found, changed, inaccessible. -->

- **S02** `not-found` - [reference or URL]
  - [reason: 404, file missing, document not found]

- **S03** `changed` - [reference or URL] -> `_SOURCES/S03_[name].md`
  - Document claims: [what the reviewed document says the source contains]
  - Actual content: [what the source actually says now]

- **S04** `inaccessible` - [reference or URL]
  - [reason: paywall, timeout, auth required, rate limited]

## Fact Verdicts

### Critical (Refuted)

<!-- Facts contradicted by observed reality or verified source content. -->

- **F01** `refuted` - "[fact text as it appears in document]"
  - **Type**: [factual / sourced-attribution / quantitative / existence]
  - **Cites**: S01
  - **Evidence**: [what was found that contradicts the claim]

### High (Weakened / Unsupported)

<!-- Facts whose sources failed verification (cascading invalidation) or have no identified support. -->

- **F02** `weakened` - "[fact text]"
  - **Type**: [type]
  - **Cites**: S02 (not-found)
  - **Reason**: Source not available for verification

- **F03** `unsupported` - "[fact text]"
  - **Type**: [type]
  - **Reason**: No supporting evidence identified

### Medium (Unverifiable)

<!-- Facts that cannot be checked due to access limitations or claim vagueness. -->

- **F04** `unverifiable` - "[fact text]"
  - **Type**: [type]
  - **Reason**: [why verification is not possible]

### Low (Unsourced)

<!-- Factual claims with no citation and no independent verification performed. -->

- **F05** `unsourced` - "[fact text]"
  - **Type**: [type]
  - **Reason**: No citation provided

## Conclusion Verdicts

<!-- Each conclusion lists its supporting facts and their verdicts.
Verdict logic:
- All facts confirmed + reasoning sound -> confirmed
- Any fact refuted -> refuted
- Any fact weakened or unverifiable -> weakened
- Supporting facts not identified -> unsupported -->

- **C01** `confirmed` - "[conclusion text]"
  - **Supports**: F06 (confirmed), F07 (confirmed)
  - **Reasoning**: Sound

- **C02** `weakened` - "[conclusion text]"
  - **Supports**: F02 (weakened), F04 (unverifiable)
  - **Reasoning**: Supporting facts not fully verified

- **C03** `refuted` - "[conclusion text]"
  - **Supports**: F01 (refuted)
  - **Reasoning**: Key supporting fact contradicted by evidence

## Unfalsifiable Claims

<!-- Subjective assessments, opinions, and value judgments. Flagged but not assigned truth verdicts.
These appear in a separate section to distinguish them from verified/unverified facts. -->

- **F08** `unfalsifiable` - "[claim text]"
  - **Location**: Section [X]
  - **Why unfalsifiable**: [subjective assessment / opinion / value judgment / comparative without criteria]

## Recommendations

### Must Do

<!-- Actions for refuted facts. -->
- [ ] [Fix: replace refuted claim with correct information, cite source]

### Should Do

<!-- Actions for weakened/unsourced facts. -->
- [ ] [Add source citation for unsourced claim F05]
- [ ] [Re-verify F02 when source S02 becomes available]

### Could Do

<!-- Optional improvements. -->
- [ ] [Remove or qualify unfalsifiable claims in Section X]

## Reference

**File Naming**:
- INFO review: `_INFO_CRAWLER_REVIEW.md`
- SPEC review: `_SPEC_AUTH_REVIEW.md`
- Code review: `auth_handler_REVIEW.md`

**Companion Artifacts**:
- `_SOURCES/` - Transcribed source content (checked in). Naming: `[SOURCE_ID]_[descriptive-name].md`
- `_DOWNLOADS_gitignore/` - Raw downloads (not checked in). Naming: `[SOURCE_ID]_[original-name].[ext]`

**Management**: Create fresh each fact-check. Consumed by `/reconcile` or `/implement` for remediation.

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial fact-check review created
