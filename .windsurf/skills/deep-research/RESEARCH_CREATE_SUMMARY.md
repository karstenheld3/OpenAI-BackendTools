# Create Summary Workflow

Global workflow for creating the Summary file in deep research. Used by all research strategies.

The Summary file (`_INFO_[TOPIC]_01-SUMMARY.md`) is the master index and cross-document synthesis for a research topic. It contains a proper summary section AND a Topic Files section (the TOC). It is NOT just a table of contents.

## Prerequisites

- `_INFO_[TOPIC]_02-SOURCES.md` exists with all sources collected and IDs assigned
- [TOPIC] identifier defined (2-6 uppercase chars, e.g., `MSGRAPH`, `OAIAPI`)
- Full subject name defined (e.g., "Microsoft Graph API")

## Workflow

1. **Copy template**: Use `RESEARCH_SUMMARY_TEMPLATE.md` as base
2. **Replace placeholders**:
   - `[TOPIC]` → actual topic ID (e.g., `OAIAPI`)
   - `[SUBJECT]` → full name (e.g., `OpenAI API`)
   - `[VERSION]` → version or documentation date
3. **Create categories**: Group topics logically from sources
4. **List topic files**: One entry per topic with clickable link, Doc ID, and brief description
   - Format: `[\`_INFO_[TOPIC]_[NN]-[NAME].md\`](./_INFO_[TOPIC]_[NN]-[NAME].md) [[TOPIC]-IN[NN]]`
   - NN = sequential number starting at 03 (01=Summary, 02=Sources)
5. **Add Topic Count section**: Summary of total and per-category counts
6. **Write Topic Details**: For each topic add Scope, Contents, Sources
7. **Write Summary**: 5-15 sentences of cross-document synthesis (not a compressed TOC)
   - During Phase 2 (Planning): skeletal summary based on sources
   - During Phase 4 (Final): full cross-document synthesis from completed topic files
8. **Delete template instructions**: Remove the HTML comment block
9. **Run quality pipeline**: verify → critique → reconcile → implement → verify

## File Naming

Output: `_INFO_[TOPIC]_01-SUMMARY.md`
Doc ID: `[TOPIC]-IN01`

Related files in the same research:
- `_INFO_[TOPIC]_02-SOURCES.md` (Doc ID: `[TOPIC]-IN02`)
- `_INFO_[TOPIC]_03-[NAME].md` through `_INFO_[TOPIC]_[NN]-[NAME].md` (topic files)

## Structure Rules

- **Summary section**: Cross-document synthesis with confidence labels, not a list of topic titles
- **Topic Files section**: Clickable links with brief descriptions, no checkboxes
- **Topic Details section**: Scope + Contents + Sources for each topic
- **NO Progress Tracking**: Progress goes in STRUT or TASKS, not Summary
- **Research stats**: Added in final phase, not during initial Summary creation

## Quality Gates

**Done when**:
- All sources from `_INFO_[TOPIC]_02-SOURCES.md` covered by topic files
- Doc ID is `[TOPIC]-IN01`
- Summary is 5-15 sentences of cross-document synthesis (not just topic titles)
- All topic links follow format: `[\`_INFO_[TOPIC]_[NN]-[NAME].md\`](./_INFO_[TOPIC]_[NN]-[NAME].md) [[TOPIC]-IN[NN]]`
- Topic numbering starts at 03 (01=Summary, 02=Sources)
- Topic Count section present with per-category breakdown
- `/verify` passes

## Example

Input: `_INFO_OAIAPI_02-SOURCES.md` with 79 sources
Output: `_INFO_OAIAPI_01-SUMMARY.md` with 62 topics in 16 categories
