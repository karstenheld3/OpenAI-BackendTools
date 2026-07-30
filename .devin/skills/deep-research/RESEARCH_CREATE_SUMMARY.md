# Create Summary Workflow

Global workflow for creating the Summary file in deep research. Used by all research strategies.

The Summary file (`_INFO_[TOPIC]-01_Summary.md`) is the master index and cross-document synthesis for a research topic. It contains a proper summary section AND a Topic Files section (the TOC). It is NOT just a table of contents.

## Prerequisites

- `_INFO_[TOPIC]-02_Sources.md` exists with all sources collected and IDs assigned
- [TOPIC] identifier defined (7-14 uppercase chars, e.g., `MSGRAPH`, `OAIAPIS`)
- Full subject name defined (e.g., "Microsoft Graph API")

## Workflow

1. **Copy template file**: `Copy-Item` from `RESEARCH_SUMMARY_TEMPLATE.md` to `_INFO_[TOPIC]-01_Summary.md`. Literal file copy, not regeneration from memory.
2. **Replace placeholders**:
   - `[TOPIC]` → actual topic ID (e.g., `OAIAPIS`)
   - `[SUBJECT]` → full name (e.g., `OpenAI API`)
   - `[VERSION]` → version or documentation date
3. **Write Goals and/or Questions** (at least one required):
   - Derive from prompt decomposition (Q1: Goal)
   - Goals: bulleted list of research objectives
   - Questions: `Q1:`/`A1:` pairs (question on one line, answer on next, blank line between pairs)
   - During Phase 2: leave answer lines as placeholders (`A1: [placeholder]`)
   - During Phase 4: fill in answers (1-3 sentences) with verification labels, mark goal outcomes
4. **Create categories**: Group topics logically from sources
5. **List topic files**: One entry per topic with clickable link, Doc ID, and brief description
   - Format: `[\`_INFO_[TOPIC]-[NN]_[Name].md\`](./_INFO_[TOPIC]-[NN]_[Name].md) [[TOPIC]-IN[NN]]`
   - NN = sequential number starting at 03 (01=Summary, 02=Sources)
6. **Add Topic Count section**: Summary of total and per-category counts
7. **Write Summary**: 5-15 sentences of cross-document synthesis (not a compressed TOC)
   - During Phase 2 (Planning): skeletal summary based on sources
   - During Phase 4 (Final): full cross-document synthesis from completed topic files
8. **Write Per-Topic Summaries** (Phase 4 only):
   - For each topic file: summary (3-20 sentences, scale with complexity) + Key Findings
   - Cover scope, main findings, and significance to overall research
   - Include verification labels on Key Findings
   - Goal: reader understands each topic without opening the file
9. **Write Conclusions** (Phase 4, when applicable):
   - Derive actionable conclusions from cross-topic analysis
   - Reference supporting topics by IN-number
   - Skip if Summary section already captures all takeaways
10. **Write Emergent Hypotheses** (Phase 4, when applicable):
    - Identify patterns from combined evidence not stated by any single source
    - All items marked [ASSUMED], each states evidence basis
    - Skip if no hypotheses emerged
11. **Write Limitations**: Data quality caveats, scope boundaries, source freshness
12. **Delete template instructions**: Remove the HTML comment block
13. **Run quality pipeline**: verify → critique → reconcile → implement → verify

## File Naming

Output: `_INFO_[TOPIC]-01_Summary.md`
Doc ID: `[TOPIC]-IN01`

Related files in the same research:
- `_INFO_[TOPIC]-02_Sources.md` (Doc ID: `[TOPIC]-IN02`)
- `_INFO_[TOPIC]-03_[Name].md` through `_INFO_[TOPIC]-[NN]_[Name].md` (topic files)

## Structure Rules

- **Goals/Questions**: At least one required. Derive from prompt decomposition. Questions use `Q1:`/`A1:` format. Answers filled in Phase 4
- **Summary section**: Cross-document synthesis with confidence labels, not a list of topic titles
- **Topic Files section**: Clickable links with brief descriptions, no checkboxes
- **Per-Topic Summaries**: 3-20 sentences + Key Findings per topic. Phase 4 only
- **Conclusions**: Numbered section. Actionable conclusions with IN-number references. Phase 4, when applicable
- **Emergent Hypotheses**: Numbered section. Combined-evidence patterns marked [ASSUMED]. Phase 4, when applicable
- **Limitations**: Data quality, scope boundaries, source freshness
- **NO Progress Tracking**: Progress goes in STRUT or TASKS, not Summary
- **Research stats**: Added in final phase, not during initial Summary creation

## Quality Gates

**Done when**:
- All sources from `_INFO_[TOPIC]-02_Sources.md` covered by topic files
- Doc ID is `[TOPIC]-IN01`
- Goals and/or Questions section present with answers/outcomes (SM-08)
- Summary is 5-15 sentences of cross-document synthesis (SM-01)
- Per-Topic Summaries present for all topic files (SM-09)
- Conclusions present when applicable (SM-10)
- Emergent Hypotheses present when applicable (SM-11)
- All topic links follow format: `[\`_INFO_[TOPIC]-[NN]_[Name].md\`](./_INFO_[TOPIC]-[NN]_[Name].md) [[TOPIC]-IN[NN]]`
- Topic numbering starts at 03 (01=Summary, 02=Sources)
- Topic Count section present with per-category breakdown
- Limitations section present
- `/verify` passes

## Example

Input: `_INFO_OAIAPI-02_Sources.md` with 79 sources
Output: `_INFO_OAIAPI-01_Summary.md` with 62 topics in 16 categories
