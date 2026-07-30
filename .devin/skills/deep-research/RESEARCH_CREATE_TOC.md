# Create TOC Workflow

Global workflow for creating Table of Contents in deep research. Used by all research strategies.

**MUST use when**: Research produces more than 1 topic file. The TOC is a working document (`__` prefix) used during Phase 2 planning to structure topics before research begins. It is consumed by RESEARCH_CREATE_SUMMARY.md to build the final Summary file.

## Prerequisites

- `_INFO_[TOPIC]-02_Sources.md` exists with all sources collected and IDs assigned
- [TOPIC] identifier defined (7-14 uppercase chars, e.g., `MSGRAPH`, `OAIAPIS`)
- Full subject name defined (e.g., "Microsoft Graph API")

## Workflow

1. **Copy template file**: `Copy-Item` from `RESEARCH_TOC_TEMPLATE.md` to `__[TOPIC]_TOC.md`. Literal file copy, not regeneration from memory.
2. **Replace placeholders**:
   - `[TOPIC]` → actual topic ID (e.g., `OAIAPI`)
   - `[SUBJECT]` → full name (e.g., `OpenAI API`)
   - `[VERSION]` → version or documentation date
3. **Create categories**: Group topics logically from sources
4. **List topic files**: One entry per topic with clickable link, Doc ID, and brief description
   - Format: `[\`_INFO_[TOPIC]-[NN]_[Name].md\`](./_INFO_[TOPIC]-[NN]_[Name].md) [TOPIC-IN[NN]]`
   - NN = sequential number starting at 03 (01=Summary, 02=Sources), PascalCase for [Name]
5. **Add Topic Count section**: Summary of total and per-category counts
6. **Write Topic Details**: For each topic add Scope, Contents, Sources
7. **Add Related**: List related/competing technologies with URLs
8. **Write Summary**: 5-15 sentences covering all key facts
9. **Delete template instructions**: Remove the HTML comment block
10. **Run quality pipeline**: verify → critique → reconcile → implement → verify

## File Naming

Output: `__[TOPIC]_TOC.md` (double underscore = scaffolding document, deleted after Summary creation)
Doc ID: `[TOPIC]-TOC` (not numbered)

## Structure Rules

- **Topic Files section**: Links only, no checkboxes
- **Topic Details section**: Scope + Contents + Sources for each topic
- **NO Progress Tracking**: Progress goes in STRUT or TASKS, not TOC
- **Research stats**: Added in final phase, not during TOC creation

## Quality Gates

**Done when**:
- All sources from `_INFO_[TOPIC]-02_Sources.md` covered
- Doc ID is `[TOPIC]-TOC` (not numbered)
- Summary is 5-15 sentences
- All topic links follow format: `[\`_INFO_[TOPIC]-[NN]_[Name].md\`](./_INFO_[TOPIC]-[NN]_[Name].md) [TOPIC-IN[NN]]`
- Topic Count section present with per-category breakdown
- Related technologies section complete
- `/verify` passes

## Example

Input: `_INFO_OAIAPI-02_Sources.md` with 79 sources
Output: `__OAIAPI_TOC.md` with 62 topics in 16 categories
