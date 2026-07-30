# Research Output Verification Rules

Enforceable rules for verifying deep-research output. Referenced by `/verify` and `/improve` workflows when context is deep-research output (multi-file research set).

**Scope**: Entire research output folder - all files checked as a set, not individually.

## Detection

Apply these rules when scope contains ANY of:
- `_INFO_[TOPIC]-01_Summary.md` (Summary file)
- `_INFO_[TOPIC]-02_Sources.md` (Sources file)
- `__STRUT_[TOPIC].md` (STRUT plan)
- Multiple `_INFO_[TOPIC]-[NN]_*.md` files (topic files)

## Rule Index

Structure (RS) - File set completeness
- RS-01: Summary file exists and is finalized
- RS-02: Sources file exists with all source IDs
- RS-03: STRUT plan fully executed (all checkboxes checked)
- RS-04: Topic files use sequential numbering from 03
- RS-05: All topic file links in Summary resolve to existing files
- RS-06: No orphan topic files (every file referenced in Summary)

Sources (SC) - Source collection quality
- SC-01: Google search via Playwright was executed (evidence in sources or STRUT)
- SC-02: All sources have IDs in format `[TOPIC]-SC-[SOURCE]-[DOCREF]`
- SC-03: All sources have `Accessed: YYYY-MM-DD` dates
- SC-04: Source hierarchy respected (tier 1-3 for critical claims)
- SC-05: PDF sources downloaded to `_DOWNLOADS_gitignore/` and transcribed to `_SOURCES/`
- SC-06: Community sources labeled `[COMMUNITY]`
- SC-07: Source count meets strategy minimum (MCPI: 15+, MEPI: 5-10 per dimension)
- SC-08: Discovery platforms tested and classified (FREE/PAID/PARTIAL)
- SC-09: No Google-rendered content used as source material (AI Overview, Featured Snippets, Knowledge Panels, People Also Ask). Google used for URL discovery only.

Summary (SM) - Summary file quality
- SM-01: Summary section is 5-15 sentences of cross-document synthesis (not a TOC restatement)
- SM-02: Topic Files section has clickable links with Doc IDs
- SM-03: Topic Count section present with per-category breakdown
- SM-04: Research stats in header block (`Xm net | Y docs | Z sources`)
- SM-05: Doc ID is `[TOPIC]-IN01`
- SM-06: Depends-on references `_INFO_[TOPIC]-02_Sources.md`
- SM-07: Document History section exists and is current
- SM-08: Goals and/or Questions section present (at least one required; per `INFO_GUIDE.md` Section 3)
- SM-09: Per-Topic Summaries section present (3-20 sentences + Key Findings per topic file)
- SM-10: Conclusions section present when research produces actionable conclusions (reference IN-numbers)
- SM-11: Emergent Hypotheses section present when patterns emerged from combined evidence (all [ASSUMED])

Topic Files (TF) - Individual topic file quality
- TF-01: Header block present (Doc ID, Goal, Dependencies, Version/Date scope)
- TF-02: Doc ID follows `[TOPIC]-IN[NN]` format (NN matches filename number)
- TF-03: Summary section present (5-15 sentences, scale with complexity)
- TF-04: Key Facts with verification labels present
- TF-05: Limitations and Known Issues section present
- TF-06: Sources section present with IDs matching `_INFO_[TOPIC]-02_Sources.md`
- TF-07: Document History section exists
- TF-08: Critical conclusions have inline citations: `[LABEL] (SOURCE_ID | URL or filename)`
- TF-09: All claims have verification labels: [VERIFIED], [ASSUMED], [TESTED], [PROVEN], [COMMUNITY]
- TF-10: Referenced `_SOURCES/` files exist on disk

STRUT Compliance (ST) - Process execution
- ST-01: STRUT plan exists with all phases defined
- ST-02: All STRUT deliverable checkboxes checked
- ST-03: Time log present with start, end, net research time
- ST-04: PromptDecomposition stored (all 7 questions answered)
- ST-05: Domain profile identified and documented
- ST-06: VCRIV checkpoints executed per granularity rules
- ST-07: Effort estimate present and actual time >= 50% of estimate

Quality (QA) - Cross-cutting quality
- QA-01: No [ASSUMED] labels where verification was possible
- QA-02: No stale sources (>12 months for fast-moving topics without justification)
- QA-03: Each dimension has 3+ sources (MCPI) or adequate coverage (MEPI)
- QA-04: Facts distinguished from opinions and assumptions
- QA-05: APAPALAN compliance (precision, brevity, structure, naming)
- QA-06: MECT compliance (voice, word choice, terminology, headings)
- QA-07: No markdown tables (use lists unless `<DevSystem MarkdownTablesAllowed=true />` present)
- QA-08: No emojis (unless `<DevSystem EmojisAllowed=true />` present)
- QA-09: Verification labels used consistently across all files (applied by writing/verification workflows, never pre-filled in templates)
- QA-10: Strategy and domain documented in Summary header with rationale
- QA-11: Native special characters used when writing in non-English languages (e.g., ae → ä, oe → ö, ue → ü, ss → ß). Never ASCII approximations.

## Verification Procedure (`/verify`)

Execute in this order:

### 1. Structure Check (RS-01 through RS-06)

```
List all files in research folder
├─> _INFO_[TOPIC]-01_Summary.md exists? (RS-01)
├─> _INFO_[TOPIC]-02_Sources.md exists? (RS-02)
├─> __STRUT_[TOPIC].md exists and complete? (RS-03)
├─> Topic files numbered 03+? (RS-04)
├─> All Summary links resolve? (RS-05)
└─> All topic files referenced in Summary? (RS-06)
```

### 2. Sources Check (SC-01 through SC-09)

```
Read _INFO_[TOPIC]-02_Sources.md
├─> Google search evidence present? (SC-01)
├─> All entries have [TOPIC]-SC-[SOURCE]-[DOCREF] IDs? (SC-02)
├─> All entries have Accessed dates? (SC-03)
├─> Tier 1-3 cited for critical claims? (SC-04)
├─> _DOWNLOADS_gitignore/ and _SOURCES/ present? (SC-05)
├─> Community sources labeled? (SC-06)
├─> Source count sufficient? (SC-07)
├─> Platforms tested? (SC-08)
└─> Google used for URL discovery only, no AI-generated content extracted? (SC-09)
```

### 3. Summary Check (SM-01 through SM-11)

```
Read _INFO_[TOPIC]-01_Summary.md
├─> Summary is synthesis, not TOC restatement? (SM-01)
├─> Topic links clickable with Doc IDs? (SM-02)
├─> Topic Count section present? (SM-03)
├─> Research stats in header? (SM-04)
├─> Doc ID correct? (SM-05)
├─> Depends-on correct? (SM-06)
├─> Document History present? (SM-07)
├─> Goals and/or Questions present? (SM-08)
├─> Per-Topic Summaries present (3-20 sentences + Key Findings)? (SM-09)
├─> Conclusions present (when applicable)? (SM-10)
└─> Emergent Hypotheses present (when applicable)? (SM-11)
```

### 4. Topic Files Check (TF-01 through TF-10)

For each `_INFO_[TOPIC]-[NN]_*.md` (NN >= 03):

```
├─> Header block complete? (TF-01, TF-02)
├─> Summary present? (TF-03)
├─> Key Facts with labels? (TF-04)
├─> Limitations section? (TF-05)
├─> Sources section with matching IDs? (TF-06)
├─> Document History? (TF-07)
├─> Inline citations on critical claims? (TF-08)
├─> All claims labeled? (TF-09)
└─> Referenced _SOURCES/ files exist? (TF-10)
```

### 5. STRUT Check (ST-01 through ST-07)

```
Read __STRUT_[TOPIC].md
├─> All phases defined? (ST-01)
├─> All deliverables checked? (ST-02)
├─> Time log complete? (ST-03)
├─> PromptDecomposition present? (ST-04)
├─> Domain identified? (ST-05)
├─> VCRIV checkpoints documented? (ST-06)
└─> Effort validation passed? (ST-07)
```

### 6. Quality Check (QA-01 through QA-10)

Cross-cutting pass over all files:

```
├─> Testable [ASSUMED] labels remaining? (QA-01)
├─> Stale sources without justification? (QA-02)
├─> Dimension coverage adequate? (QA-03)
├─> Facts/opinions/assumptions distinguished? (QA-04)
├─> APAPALAN compliance? (QA-05)
├─> MECT compliance? (QA-06)
├─> No tables? (QA-07)
├─> No emojis? (QA-08)
├─> Labels consistent? (QA-09)
├─> Strategy + domain documented? (QA-10)
└─> Native characters used (no ASCII substitutes)? (QA-11)
```

## Improvement Procedure (`/improve`)

When `/improve` targets a deep-research output folder, apply these specialized techniques IN ADDITION to the standard Research Output context in `improve.md`:

### Depth Indicators (signs research needs more depth)

- Topic file shorter than 500 words for a complex subject
- Only 1-2 sources cited per topic file (should be 3+)
- All sources from same platform (source diversity lacking)
- No `[VERIFIED]` labels (only `[ASSUMED]` or `[COMMUNITY]`)
- Limitations section empty or says "None identified"
- Missing inline citations on key claims
- Gotchas section absent or generic
- Summary synthesis is shallow (just lists topics without connecting findings)
- Sources file has no PDF sources (missed downloadable content)
- No `_SOURCES/` folder (sources not transcribed for permanence)

### Enrichment Techniques (research-specific)

1. **Source Gap Analysis** - Compare source file against domain-specific tier list. Identify missing tiers (e.g., no official PDFs, no community sources, no changelogs). Run Google search via Playwright for each gap (URL discovery only, click through to sources).
2. **Google AI Content Audit** - Search all topic files for claims that lack a source URL or source ID. Cross-check against Google AI Overview patterns (generic summaries without attribution). Flag and replace with content from actual source websites.
3. **Dimension Depth Check** - For each dimension in PromptDecomposition, count topic files and sources. Flag dimensions with fewer than 3 sources or 1 topic file.
4. **Claim Verification Upgrade** - Find all `[ASSUMED]` labels. For each, attempt verification via primary sources. Upgrade to `[VERIFIED]` or document why verification failed.
5. **PDF Discovery Pass** - Re-run `"[SUBJECT]" filetype:pdf` searches with additional dimension keywords. Download and transcribe newly found PDFs.
6. **Temporal Freshness** - Check source dates. For fast-moving topics (software, legal, financial), sources >12 months need refresh or explicit "still current as of" note.
7. **Cross-Reference Synthesis** - Read all topic files. Identify connections, patterns, and contradictions not captured in Summary. Update Summary synthesis section.
8. **Competing Perspective Search** - For each key finding, search for contradicting evidence. Document as "Alternative View" or upgrade finding to `[PROVEN]` if no contradiction found.
9. **Practical Validation** - For actionable recommendations, verify they work in practice (code examples, configuration tests, API calls). Upgrade labels from `[VERIFIED]` to `[TESTED]`.

### Priority Order for Improvement

1. Missing mandatory files (RS-01, RS-02) - structural
2. Source gaps (SC-01, SC-05, SC-07) - foundation
3. Unverified claims (QA-01, TF-09) - credibility
4. Shallow topics (depth indicators) - value
5. Summary quality (SM-01) - synthesis
6. Expression quality (QA-05, QA-06) - polish
