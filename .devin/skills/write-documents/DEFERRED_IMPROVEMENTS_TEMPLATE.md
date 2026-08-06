<!--
DEFERRED IMPROVEMENTS TEMPLATE
Created automatically by `/improve` when Phase 3 defers candidates.

Naming: `__<target_filename_without_ext>_DEFERRED_IMPROVEMENTS.md` in same directory as target file.
Examples:
  _SPEC_CRAWLER.md          -> __SPEC_CRAWLER_DEFERRED_IMPROVEMENTS.md
  MARKET_ANALYSIS.md        -> __MARKET_ANALYSIS_DEFERRED_IMPROVEMENTS.md
  Folder scope src/         -> __src_DEFERRED_IMPROVEMENTS.md in that folder

Remove this comment block after creating the document.
-->

# Deferred Improvements: [TARGET_FILENAME]

**Doc ID**: [TOPIC]-DF[NN]
<!-- Topic IDs: 7-14 uppercase chars. Inside T##/S## folders use nested: [TOPIC]-[SUBTOPIC]-DF[NN] -->
**Goal**: Track improvement candidates deferred from `/improve` runs
**Target file(s)**:
- `[path/to/target_file.md]`
**Timeline**: Created YYYY-MM-DD, Updated N times (YYYY-MM-DD - YYYY-MM-DD)

**Depends on:**
- `[TARGET_FILE] [TARGET-DOC-ID]` for improvement context

## Candidates

<!-- D-[NN] numbering is sequential across all runs, never reused. -->

### D-01: [Issue title] ([rule or technique reference])
- **Issue**: [What is wrong or missing]
- **Fix**: [Proposed change]
- **Effort**: [Minimal | Low | Medium | High]
- **Value**: [LOW | MEDIUM | HIGH] ([justification])

<!-- Optional fields per candidate:
- **Status**: PARTIALLY ADDRESSED | SUPERSEDED | BLOCKED BY [ref]
- **Remaining**: [What is left to do if partially addressed]
- **Technique**: [SD-ES-XX or other technique reference]
-->

## Log

<!-- One entry per `/improve` run that applied an improvement. -->

- **Run 1** (YYYY-MM-DD): [One-line summary of improvement applied]

## Document History

**[YYYY-MM-DD HH:MM]**
- Initial deferred improvements file created from `/improve` run 1

<!-- EXAMPLE: Reference only. Do not copy into new documents. Shows a completed document with real values. -->

## Full Example

```markdown
# Deferred Improvements: MARKET_ANALYSIS_WHY_STARTUPS_WIN_HERE

**Doc ID**: DLPHS-BSNPLNV3-DF01
**Goal**: Track improvement candidates deferred from `/improve` runs
**Target file(s)**:
- `S03_BusinessPlanV3/MARKET_ANALYSIS_WHY_STARTUPS_WIN_HERE.md`
**Timeline**: Created 2026-08-05, Updated 2 times (2026-08-05 - 2026-08-05)

**Depends on:**
- `MARKET_ANALYSIS_WHY_STARTUPS_WIN_HERE.md [DLPHS-BSNPLNV3-MA01]` for improvement context

## Candidates

### D-01: Section 7 intro lacks decision framing (AP-ST-01)
- **Issue**: Intro states content but not WHY or what decision it enables
- **Fix**: Add one sentence linking to comparison matrix decision criteria
- **Effort**: Minimal
- **Value**: MEDIUM (reader orientation)

### D-02: Key Source Quotes missing (SD-CD-06)
- **Issue**: Zero direct quotes in document
- **Technique**: Read topic files for quotable insights per SD-CD-06
- **Effort**: Medium
- **Value**: HIGH (directly usable in pitch speaker notes)

## Log

- **Run 1** (2026-08-05): Added margin conditions mapping to Section 7 comparison matrix
- **Run 2** (2026-08-05): Added 3 text diagrams (Argument Arc, Bimodal Distribution, Positioning Framework)
- **Run 3** (2026-08-05): Added Contradictions and Tensions section (SD-ES-03)

## Document History

**[2026-08-05 21:00]**
- Initial deferred improvements file created from `/improve` run 1
- Added D-01, D-02 candidates

**[2026-08-05 21:30]**
- Added D-03, D-04 candidates from run 3
```
