# Exhaustive Research Strategy (MCPI Approach)

Research **[SUBJECT]** exhaustively using the MCPI (Most Complete Point of Information) approach.

This strategy follows the global Phase 1-4 model defined in SKILL.md.

## Prerequisites

- Output folder created per SKILL.md "Output Folder" section
- Topic ID registered in ID-REGISTRY.md
- All file paths below are relative to the output folder

## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding

## Phase 1: Preflight

Decompose prompt, document assumptions, collect sources, verify/correct, create STRUT, run first VCRIV.

### Step 1: Create STRUT and Decompose Prompt

- Create `__STRUT_[TOPIC].md` using `/write-strut` workflow
- STRUT defines: phases, objectives, steps, deliverables, transitions
- STRUT enforces 3 VCRIV checkpoints as deliverables
- STRUT MUST include quality pipeline steps and time log:
  ```
  ## Time Log
  Started: [YYYY-MM-DD HH:MM]
  Ended: [pending]
  Active intervals:
  - [HH:MM-HH:MM] (Phase X)
  Net research time: [pending]
  ```
- **Domain identification**:
  1. Determine research domain from prompt context
  2. Read corresponding `DOMAIN_*.md` profile (if available)
  3. Incorporate domain-specific rules (source tiers, document handling, template additions, quality criteria)
  4. If no matching profile, use DOMAIN_DEFAULT.md and document in STRUT
- STRUT MUST include the active domain profile and its rules
- Answer 7 decomposition questions per SKILL.md, store PromptDecomposition in STRUT
- Run `/verify` on STRUT plan
- **Done when**: STRUT created, all 7 questions answered, PromptDecomposition stored, effort estimated

### Step 2: Document Assumptions

- Write down "Pre-research assumptions" about [SUBJECT]
- Parse prompt for: subject details, scope boundaries, output expectations
- Check conversation history and NOTES.md for prior context
- Document inferred details with [ASSUMED] label
- Proceed with best interpretation - do NOT ask unless genuinely ambiguous

### Step 3: Test Discovery Platforms

Before collecting sources, test each discovery platform from Q7:
- Query each platform with test search matching research criteria
- Classify access: **FREE** (full results), **PAID** (paywall), **PARTIAL** (limited free tier)
- Keep platforms with FREE or PARTIAL access
- Document PAID platforms in `_INFO_[TOPIC]_02-SOURCES.md` for user follow-up
- **Done when**: All platforms tested, access levels documented, selected platforms identified

### Step 4: Collect Sources

- **Document version scope**: Explicitly state the [SUBJECT] version (e.g., `v2.1.0`, `API v3`). If not applicable, use date: `YYYY-MM-DD`
- Create `_INFO_[TOPIC]_02-SOURCES.md`
- **Query selected discovery platforms** from Step 3 first
- Collect ALL official documentation URLs from vendor/project documentation
- Collect community sources (secondary sources) for real-world insights:
  - Stack Overflow questions/answers with high votes
  - GitHub issues (open and closed) revealing bugs, limitations, workarounds
  - Blog posts from recognized experts or official developer advocates
  - Reddit/forum discussions highlighting gotchas
  - Release notes and changelogs for version-specific behavior
- **Community source rule**: Community sources supplement official docs, not replace. Use for limitations, quirks, gotchas. **Filter to match [SUBJECT] version** - discard outdated issues.
- **Source collection using domain-specific tiers**: Use tiers from the active domain profile. Default: official documentation > vendor content > community/analyst sources.
- Assign source IDs: `[SUBJECT]-SC-[SOURCE]-[DOCNAME]` (per SKILL.md format)
  - Official: `[SUBJECT]-SC-[VENDOR]-[DOCNAME]`
  - Community: `[SUBJECT]-SC-[PLATFORM]-[DOCNAME]` (e.g., `GRPH-SC-SO-RATELIMIT`)
- Group sources by category (domain-specific)
- Include "Related" section listing similar or easily confused alternatives
- **Source processing**: Process all PDF sources through transcription pipeline. Read `deep-research-config.json` for settings.
- **Done when**: (a) Official docs main navigation fully enumerated, (b) 15-30 sources collected (minimum 15), (c) All sources have IDs, (d) PDF sources transcribed

### Step 5: Verify and Correct Assumptions

- Verify assumptions against primary sources
- If >30% wrong or outdated, re-run with corrected understanding, keep originals (strikethrough). **Max 2 re-runs**, then proceed.
- Document accuracy in `_INFO_[TOPIC]_02-SOURCES.md` header (e.g., "Preflight accuracy: 7/10 assumptions verified")
- **Rubric**: CORRECT = matches source exactly. PARTIAL = spirit correct but details differ (counts as wrong). WRONG = contradicted by source.

### Step 6: Run First VCRIV

Run quality pipeline on Preflight deliverables (SOURCES, STRUT, PromptDecomposition).
- **Done when**: Phase 1 deliverables verified, critique addressed

## Phase 2: Planning

Create Summary file (skeletal), topic template, TASKS plan, run second VCRIV.

### Step 1: Summary File Creation

- Follow [RESEARCH_CREATE_SUMMARY.md](RESEARCH_CREATE_SUMMARY.md) workflow
- Use [RESEARCH_SUMMARY_TEMPLATE.md](RESEARCH_SUMMARY_TEMPLATE.md) as base
- Create `_INFO_[TOPIC]_01-SUMMARY.md` with skeletal structure (summary placeholder, topic file links, topic count)
- **Done when**: Summary file covers all major topics from sources, skeletal summary present, all topic file links resolve

### Step 2: Template Creation

- Create `__TEMPLATE_[TOPIC]_TOPIC.md` (working template, deleted after research)
- Template structure (base + domain-specific additions from active profile):
  - Header block (Doc ID, Goal, Dependencies, **Version/Date scope**)
  - Summary: **5-15 sentences** (scale with complexity)
  - Key Facts with [VERIFIED] labels
  - Use Cases
  - Quick Reference (one-screen lookup)
  - Main Sections (follow TOC structure)
  - **Limitations and Known Issues** (from community sources)
  - **Gotchas and Quirks** (undocumented behavior, edge cases)
  - Sources section with **same IDs as `_INFO_[TOPIC]_02-SOURCES.md`**
  - Document History
- Include "Template Instructions" section (to be deleted when using)
- **Done when**: Template has all required sections, instructions clear

### Step 3: TASKS Plan

- Create `__TASKS_[TOPIC]_RESEARCH.md` using `/write-tasks-plan` workflow
- Partition topics from Summary file into discrete tasks
- Each task: Status, Estimated effort, Sources (official + community), Items to document, Done-when criteria
- **Task timing format**: `- [ ] TK-01: [Description] [HH:MM-HH:MM] Xm`
  - Mark parallel tasks with `(parallel)` suffix
- **Done when**: All topics have corresponding tasks, effort estimates assigned

### Step 4: Run Second VCRIV

Run quality pipeline on Planning deliverables (Summary file, template, TASKS).
- **Done when**: Phase 2 deliverables verified, critique addressed

## Phase 3: Topic-by-Topic, File-by-File Research

Adhere to TASKS plan and STRUT. Run VCRIV per granularity rules.

### Execution

- For each topic file from TASKS:
  1. Research using official source URLs first
  2. Cross-reference with community sources for limitations, bugs, quirks
  3. Process sources per domain profile document handling rules
  4. Create `_INFO_[TOPIC]_[NN]-[NAME].md` using template
     - NN = sequential number starting at 03 (01=Summary, 02=Sources)
     - Files sort alphabetically
  5. Include "Limitations and Known Issues" with community source citations
  6. **Mandatory inline citations**: Critical conclusions MUST include `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`. Referenced files MUST exist in `_SOURCES/`.
  7. Update TASKS progress and Summary file status
- All claims must have verification labels: [VERIFIED], [ASSUMED], [TESTED], [PROVEN], [COMMUNITY]

### VCRIV per Granularity Rules

Run quality pipeline as defined in STRUT (scope-based from SKILL.md):
- NARROW: VCRIV per topic file
- FOCUSED/EXPLORATORY: VCRIV per dimension
- **Done when**: All tasks in TASKS plan completed and checked off

## Phase 4: Final Verification and Sync

### Dimension Coverage Check

- Each dimension MUST have: 3+ sources, 1+ topic file, verification labels
- Missing dimensions MUST have documented rationale in STRUT
- Calculate coverage percentage per dimension
- If any dimension has 0 sources, escalate to [CONSULT]

### Completeness Verification

- Re-read official documentation structure (main navigation/sidebar)
- Compare against Summary file - identify missed topics
- For each gap: assess priority (High/Medium/Low), create INFO files for High/Medium
- Document coverage percentage in Summary file header

### Sync and Metadata

- Cross-verify all topic files against Summary file checklist
- Finalize Summary section with cross-document synthesis from completed topic files
- Verify all links work
- Ensure community-sourced limitations included in relevant sections
- **Add Research stats to Summary file header block**: `**Research stats**: 35m net | 62 docs | 79 sources`

### Ex-Post Review Questions

1. Does output meet research goal with maximum quality, clarity, correctness?
2. Does it contain self-critical perspective?
3. Did it invest substantial effort on primary sources?
4. Did it invest substantial effort on secondary sources?
5. Were PDFs downloaded and read (not just web research)?
6. Are all initial research questions answered?
7. Are findings properly linked in Summary file?

### Run Final VCRIV

Run quality pipeline on complete research set.
- **Done when**: All strategy requirements met, links work, summaries synced, metadata added

## Global Rules

**Termination criteria**: Max 2 cycles per quality checkpoint. If issues persist after 2 cycles, escalate to [ACTOR] via [CONSULT].

**Autonomous operation**: After Phase 1, NO user interaction until delivery of final verified research set. [CONSULT] (from termination criteria) is the only exception.

**Rollback**: If any phase reveals fundamental error in earlier phase, document in PROBLEMS.md and consult user before rollback.

## Scoring Model (When Ranking Requested)

If user intent includes ranking (e.g., "best", "top", "recommend", "which should I"):
1. **Define scoring dimensions** - 3-5 criteria relevant to user's goal (document in output)
2. **Score each option** - 0-3 per dimension, calculate total
3. **Present results in ranked order** - most useful on top
4. **Include scoring rationale** - brief explanation per option

Example scoring table:
```
| Option | Dim1 | Dim2 | Dim3 | Total | Notes |
|--------|------|------|------|-------|-------|
| A      | 3    | 2    | 3    | 8     | Best overall fit |
| B      | 2    | 3    | 2    | 7     | Strong in Dim2 |
```

## Output Format

MCPI outputs an INFO document with:
1. **Research Question** - What we investigated
2. **Strategy & Domain** - MCPI + domain profile + rationale for each choice
3. **Scoring Model** (if ranking requested) - Dimensions and weights
4. **Key Findings** - Exhaustive coverage, ranked by score if applicable
5. **Detailed Analysis** - Per-topic breakdowns
6. **Limitations** - What we didn't cover, caveats
7. **Sources** - All sources with IDs and verification labels

See SKILL.md for file naming, verification labels, source hierarchy, and quality rules.
