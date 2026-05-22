# Exhaustive API/Technology Research Strategy (MCPI Approach)

Research **[SUBJECT]** exhaustively using the MCPI (Most Complete Point of Information) approach.

## Prerequisites

- Output folder created per SKILL.md "Output Folder" section
- Topic ID registered in ID-REGISTRY.md
- All file paths below are relative to the output folder

**Before starting**: Create `__STRUT_[TOPIC].md` using `/write-strut` with Time Log and Credit Tracking sections:
```
## Time Log
Started: [YYYY-MM-DD HH:MM]
Ended: [pending]

Active intervals:
- [HH:MM-HH:MM] (Phase X-Y)

Net research time: [pending]

## Credit Tracking
Phase 1: [model] [Xx] - [HH:MM]

Estimated credits: [pending]
```

**At each phase start**:
1. Run `simple-screenshot.ps1` to capture Windsurf header
2. Detect current model name from screenshot
3. Lookup cost in `windsurf-model-registry.json`
4. Log to Credit Tracking section
5. **Never auto-switch models** - only observe and log

**Phases:**

**Phase 1: Preflight - Assumptions & Source Collection**
- **Assumptions Check**:
  1. Write down "Pre-research assumptions" about [SUBJECT]
  2. Verify assumptions against primary sources during preflight
  3. If >30% of assumptions are wrong or outdated, re-run preflight with corrected understanding, keep original assumptions (strikethrough). **Max 2 re-runs**, then proceed with corrected assumptions.
  4. Document assumption accuracy in `_INFO_[TOPIC]_02-SOURCES.md` header (e.g., "Preflight accuracy: 7/10 assumptions verified")
  5. **Assumption verification rubric**: CORRECT = matches source exactly. PARTIAL = spirit correct but details differ (counts as wrong for threshold). WRONG = contradicted by source.
- **Document version scope**: Explicitly state the [SUBJECT] version being documented (e.g., `v2.1.0`, `API v3`). If versioning not applicable, use documentation date: `YYYY-MM-DD`
- Create `_INFO_[TOPIC]_02-SOURCES.md`
- Collect ALL official documentation URLs from vendor/project documentation
- Collect community sources (secondary sources) for real-world insights:
  - Stack Overflow questions/answers with high votes
  - GitHub issues (open and closed) revealing bugs, limitations, workarounds
  - Blog posts from recognized experts or official developer advocates
  - Reddit/forum discussions highlighting gotchas
  - Release notes and changelogs for version-specific behavior
- **Community source rule**: Community sources supplement official docs, not replace. Use primarily for limitations, quirks, and real-world gotchas. **Filter community sources to match [SUBJECT] version** - discard outdated version-specific issues.
- Assign source IDs in format: `[TOPIC]-IN01-SC-[SOURCE]-[DOCNAME]`
  - Official sources: `[TOPIC]-IN01-SC-[VENDOR]-[DOCNAME]`
  - Community sources: `[TOPIC]-IN01-SC-[PLATFORM]-[DOCNAME]` (e.g., `GRPH-IN01-SC-SO-RATELIMIT`, `GRPH-IN01-SC-GH-ISSUE1234`)
- Group sources by category: Core Docs, SDK/Libraries, Resource Types, Licensing, Related APIs/Technologies, Community Sources
- Include "Related APIs/Technologies" section listing similar or easily confused alternatives
- **Done when**: (a) Official docs main navigation fully enumerated, (b) 10-20 community sources collected, (c) All sources have IDs assigned

**Phase 2: Summary File Creation (workflow: /verify > /critique > /reconcile /implement > /verify)**
- Follow [RESEARCH_CREATE_SUMMARY.md](RESEARCH_CREATE_SUMMARY.md) workflow
- Use [RESEARCH_SUMMARY_TEMPLATE.md](RESEARCH_SUMMARY_TEMPLATE.md) as base
- Create `_INFO_[TOPIC]_01-SUMMARY.md` with skeletal structure
- **Done when**: Summary file covers all major topics from sources, skeletal summary present, all topic file links resolve

**Phase 3: Template Creation (verify > critique > reconcile > verify)**
- Create `__TEMPLATE_[TOPIC]_TOPIC.md` (working template, deleted after research)
- Template structure:
  - Header block (Doc ID, Goal, Dependencies, **Version/Date scope**)
  - Summary: **5-15 sentences** (scale with topic complexity)
  - Key Facts with [VERIFIED] labels
  - Use Cases
  - Quick Reference (one-screen lookup)
  - Main Sections (follow TOC structure)
  - **Limitations and Known Issues** (from community sources)
  - **Gotchas and Quirks** (undocumented behavior, edge cases)
  - SDK Examples (adapt to relevant languages: C#, Python, TypeScript, PowerShell, JavaScript, Go, etc.)
  - Error Responses with codes
  - Rate Limiting / Throttling Considerations
  - Sources section with **same IDs as `_INFO_[TOPIC]_02-SOURCES.md`**
  - Document History
- Include "Template Instructions" section (to be deleted when using)
- Run `/verify` then `/critique` then `/reconcile /implement` findings then `/verify` again
- **Done when**: Template has all required sections, instructions are clear
- **USER APPROVAL GATE**: Present Summary file + Template to user before proceeding to Phase 4

**Phase 4: TASKS Plan**
- Create `__TASKS_[TOPIC]_RESEARCH.md`
- Partition topics from Summary file into discrete tasks
- Each task: Status, Estimated effort, Sources (official + community), Items to document, Done-when criteria
- **Task timing format**: `- [ ] TK-01: [Description] [HH:MM-HH:MM] Xm`
  - Log start time when beginning task, end time when completing
  - Mark parallel tasks with `(parallel)` suffix
  - Example: `- [x] TK-02: Rate limits [10:15-11:00] 45m (parallel)`
- Include Progress Summary section
- **Done when**: All topics have corresponding tasks, effort estimates assigned

**Phase 5: File-by-File Research**
- For each topic file from TASKS:
  1. Research using official source URLs first
  2. Cross-reference with community sources for limitations, bugs, quirks
  3. Create `_INFO_[TOPIC]_[NN]-[NAME].md` using template
     - NN = sequential number starting at 03 (01=Summary, 02=Sources)
     - Files sort alphabetically
     - Example: `_INFO_OASDKP_03-INTRODUCTION.md`
  4. Include "Limitations and Known Issues" section with community source citations
  5. Run `/verify` then `/critique` then `/reconcile /implement` findings then `/verify` again
  6. Update TASKS progress
  7. Update Summary file status
- All claims must have verification labels: [VERIFIED], [ASSUMED], [TESTED], [PROVEN], [COMMUNITY]
- **Done when**: All tasks in TASKS plan completed and checked off

**Phase 6: Final Verification and Sync**
- **Verify against this document** (`RESEARCH_STRATEGY_TECH_MCPI.md`) - check all phase requirements met
- Cross-verify all topic files against Summary file checklist
- Finalize Summary section with cross-document synthesis from completed topic files
- Verify all links work
- Ensure community-sourced limitations are included in relevant sections
- **Add Research stats to Summary file header block** (copy from STRUT):
  ```
  **Research stats**: 35m net | ~35 credits | 62 docs | 79 sources | Opus 4.5 Thinking
  ```
- Run final `/verify` with context: RESEARCH_STRATEGY_TECH_MCPI
- **Done when**: All strategy requirements met, links work, summaries synced, metadata added

**Phase 6.5: Completeness Verification**
- Re-read official documentation structure (main navigation/sidebar)
- Compare against Summary file - identify any missed topics
- For each gap:
  1. Assess priority (High: core feature, Medium: useful, Low: niche)
  2. Create INFO files for High/Medium priority gaps
  3. Update Summary file with new topics
- Document coverage percentage in Summary file header
- **Done when**: All High/Medium priority topics documented, gaps acknowledged

**Rollback**: If any phase reveals fundamental error in earlier phase, document in PROBLEMS.md and consult user before rollback.

**File Naming** (numbered scheme):
- `_INFO_[TOPIC]_01-SUMMARY.md` - Summary file with cross-document synthesis + Topic Files section (Doc ID: `[TOPIC]-IN01`)
- `_INFO_[TOPIC]_02-SOURCES.md` - Collected sources with IDs and verification labels (Doc ID: `[TOPIC]-IN02`)
- `_INFO_[TOPIC]_03-[NAME].md` through `_INFO_[TOPIC]_[NN]-[NAME].md` - Individual topic files (Doc ID: `[TOPIC]-IN03+`)
- No prefix: Tracking files (TASKS, NOTES, PROBLEMS, PROGRESS)

**Verification Labels:**
- `[VERIFIED]` - Confirmed from official documentation
- `[ASSUMED]` - Inferred but not explicitly stated
- `[TESTED]` - Manually tested by running code
- `[PROVEN]` - Confirmed from multiple independent sources
- `[COMMUNITY]` - Reported by community sources (cite source ID)

**Source Types:**
- **Primary (Official)**: Vendor documentation, official SDKs, API references, release notes
- **Secondary (Community)**: Stack Overflow, GitHub issues, expert blogs, forums, conference talks

**Anti-patterns to Avoid:**
- Checkboxes in Summary file topic lists (use links instead)
- Short summaries (2-3 sentences) for complex topics
- Missing Related APIs/Technologies section
- Source IDs not matching between SOURCES and topic files
- Non-clickable references in Summary file
- Ignoring community sources for known issues
- Treating community reports as verified without citation
- Non-sequential file numbering (files should sort in topic order)
- Plain text file references in Summary file (use markdown links)
- Skipping completeness verification against source docs

**Quality Gates:**
- Every topic file verified against source URLs
- All SDK examples syntactically correct
- No Markdown tables (use lists)
- No emojis
- All sources cited with IDs
- Summary copy/paste ready for executive use
- Limitations section populated from community research
- Known issues cross-referenced with official bug trackers where available
