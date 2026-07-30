# Curated Research Strategy (MEPI Approach)

Research **[SUBJECT]** using the MEPI (Most Executable Point of Information) approach - curated best options per topic.

This strategy follows the global Phase 1-4 model defined in SKILL.md.

## Prerequisites

- Output folder created per SKILL.md "Output Folder" section
- Topic ID registered in ID-REGISTRY.md
- All file paths below are relative to the output folder

## MUST-NOT-FORGET

- Run `/verify` on STRUT plan before proceeding

**When to use MEPI instead of MCPI:**
- Reversible decisions (can change later)
- Time-constrained (user needs answer quickly)
- Action-oriented (user will do something, not archive)
- Low-to-medium stakes (not legal/financial/medical critical)

## Phase 1: Preflight

Decompose prompt, document assumptions, collect sources, verify/correct, create STRUT, run first VCRIV.

### Step 1: Create STRUT and Decompose Prompt

- Create `__STRUT_[TOPIC].md` using `/write-strut` workflow
- STRUT defines: phases, objectives, steps, deliverables, transitions
- STRUT enforces 3 VCRIV gate deliverables (Preflight, Planning, Final) + per-file VCRIV during research = 4 checkpoints total per SKILL.md
- STRUT MUST include quality pipeline steps and time log
- **Domain identification**:
  1. Determine research domain from prompt context
  2. Read corresponding `[domain]/DOMAIN_*.md` profile (if available)
  3. Incorporate domain-specific rules
  4. If no matching profile, use `default/DOMAIN_DEFAULT.md` and document in STRUT
- STRUT MUST include the active domain profile and its rules
- Answer 7 decomposition questions per SKILL.md, store PromptDecomposition in STRUT
- At Q5: Confirm MEPI. Switch to MCPI if high-stakes discovered.
- Run `/verify` on STRUT plan
- **Done when**: STRUT created, all 7 questions answered, PromptDecomposition stored, effort estimated

### Step 2: Document Assumptions

- Write down "Pre-research assumptions" about [SUBJECT]
- Parse prompt for: subject details, scope boundaries, output expectations
- Check conversation history and NOTES.md for prior context
- Document inferred details with [ASSUMED] label
- Proceed with best interpretation - do NOT ask unless genuinely ambiguous

### Step 3: Collect Sources (Curated)

- **Document version scope**: Explicitly state the [SUBJECT] version (e.g., `v2.1.0`, `API v3`). If not applicable, use date: `YYYY-MM-DD`
- Create `_INFO_[TOPIC]-02_Sources.md`
- **MANDATORY: Google search via Playwright** (ms-playwright-mcp). Navigate to google.com and run targeted queries:
  - `"[SUBJECT]" filetype:pdf` - Find whitepapers, specs, official PDFs
  - `"[SUBJECT]" site:[official-domain]` - Official content discovery
  - `"[SUBJECT]" [dimension keyword]` - Per-dimension discovery
  - Collect PDF URLs, documentation pages, and public resources from results
  - Download discovered PDFs to `_DOWNLOADS_gitignore/`
  - **Google = URL discovery only**: Skip AI Overview, Featured Snippets, Knowledge Panels. Extract URLs and titles only, then click through to source websites for content. See RESEARCH_TOOLS.md "Google Search Extraction Principle".
- **Classify discovery platforms** from Q7 as FREE/PAID/PARTIAL; use FREE and PARTIAL, note PAID for user follow-up
- Collect **5-10 sources per dimension** (focus on top-tier sources first)
- Skip exhaustive community source collection
- Use source tiers from active domain profile. Default: official documentation > vendor content > community/analyst sources.
- Assign source IDs: `[TOPIC]-SC-[SOURCE]-[DOCREF]`
- Group sources by category (domain-specific)
- Process all PDF sources through transcription pipeline
- **Done when**: 5-10 quality sources per dimension, all with IDs, PDFs transcribed

### Step 4: Verify and Correct Assumptions

- Verify assumptions against primary sources
- If >30% wrong or outdated, re-run with corrected understanding (strikethrough originals). **Max 2 re-runs**, then proceed.
- Document accuracy in `_INFO_[TOPIC]-02_Sources.md` header (e.g., "Preflight accuracy: 7/10 verified")
- **Rubric**: CORRECT = matches exactly. PARTIAL = spirit correct, details differ (counts as wrong). WRONG = contradicted.

### Step 5: Run First VCRIV

Run quality pipeline on Preflight deliverables (SOURCES, STRUT, PromptDecomposition).
- **Done when**: Phase 1 deliverables verified, critique addressed

## Phase 2: Planning

Create Summary file (skeletal), topic template, TASKS plan, run second VCRIV.

### Step 1: Summary File Creation

- Follow [RESEARCH_CREATE_SUMMARY.md](RESEARCH_CREATE_SUMMARY.md) workflow
- `Copy-Item` [RESEARCH_SUMMARY_TEMPLATE.md](RESEARCH_SUMMARY_TEMPLATE.md) to output file (literal copy)
- Create `_INFO_[TOPIC]-01_Summary.md` with skeletal structure
- Summary can be shorter than MCPI (5-10 sentences)
- **Done when**: Summary file covers major topics from sources, all topic file links resolve

### Step 2: Template Creation

- Create `__TEMPLATE_[TOPIC]_TOPIC.md` (working template, deleted after research)
- Template structure (base + domain-specific additions from active profile):
  - Header block (Doc ID, Goal, Dependencies, **Version/Date scope**)
  - Summary (5-10 sentences)
  - Key Facts with [VERIFIED] labels
  - Use Cases, Quick Reference
  - Main Sections (follow TOC structure)
  - **Limitations and Known Issues**, **Gotchas and Quirks**
  - Sources section, Document History
- **Done when**: Template has all required sections

### Step 3: TASKS Plan

- Create `__TASKS_[TOPIC]_RESEARCH.md`
- Partition topics from Summary file into discrete tasks
- Each task: Status, Estimated effort, Sources, Done-when criteria
- Effort estimates typically 2-4 hours total
- **Done when**: All topics have corresponding tasks

### Step 4: Run Second VCRIV

Run quality pipeline on Planning deliverables (Summary file, template, TASKS).
- **Done when**: Phase 2 deliverables verified, critique addressed

## Phase 3: Topic-by-Topic, File-by-File Research

Adhere to TASKS plan and STRUT. Run VCRIV per granularity rules.

### Execution

- For each topic file from TASKS:
  1. Research using official source URLs first
  2. Cross-reference with community sources for limitations, quirks
  3. Create `_INFO_[TOPIC]-[NN]_[Name].md` using template (NN starts at 03)
  4. **Focus on curated best options** - recommend, don't just list
  5. Include **clear recommendation with rationale** for each topic
  6. **Mandatory inline citations**: `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`
  7. Update TASKS progress and Summary file status
- All claims must have verification labels

### VCRIV per Granularity Rules

Run quality pipeline as defined in STRUT (scope-based from SKILL.md):
- NARROW: VCRIV per topic file
- FOCUSED/EXPLORATORY: VCRIV per dimension
- **Done when**: All tasks completed with curated recommendations each

## Phase 4: Final Verification and Sync

### Dimension Coverage Check

- Each dimension MUST have: sources, topic file(s), verification labels
- Missing dimensions MUST have documented rationale in STRUT
- If any dimension has 0 sources, escalate to [CONSULT]

### Sync and Metadata

- Cross-verify topic files against Summary file checklist
- Finalize Summary section with cross-document synthesis from completed topic files
- Verify all links work
- **Add Research stats to Summary file header block**: `**Research stats**: Xm net | Y docs | Z sources`

### Run Final VCRIV

Run quality pipeline on complete research set.
- **Done when**: All requirements met, recommendations actionable

## Global Rules

**Termination criteria**: Max 2 cycles per quality checkpoint. Escalate via [CONSULT] if issues persist.

**Autonomous operation**: After Phase 1, NO user interaction until delivery. [CONSULT] is the only exception.

**Rollback**: If any phase reveals fundamental error in earlier phase, document in PROBLEMS.md and consult user.

## Scoring Model (When Ranking Requested)

If user intent includes ranking (e.g., "best", "top", "recommend", "which should I"):
1. **Define scoring dimensions** - 3-5 criteria relevant to user's goal
2. **Score ALL discovered options** - 0-3 per dimension, calculate total
3. **Use scores to select curated options** - top N options become recommendations
4. **Document selection rationale**:
   - **Included options** - why they scored high, what makes them fit
   - **Excluded options** - why they didn't make the cut (low score, poor fit, missing criteria)

Example:
```
## Option Selection

**Scoring Dimensions**: Thematic Fit (0-3), Reach (0-3), Accessibility (0-3)

**Included** (score >= 7):
- Option A (9/9): Perfect thematic fit, high reach, easy to contact
- Option B (8/9): Strong fit, medium reach, responsive

**Excluded** (score < 7):
- Option X (4/9): High reach but no thematic fit - wrong audience
- Option Y (5/9): Good fit but inactive account - no recent posts
```

## Output Format

MEPI outputs an INFO document with:
1. **Research Question** - What we investigated
2. **Strategy & Domain** - MEPI + domain profile + rationale for each choice
3. **Scoring Model** (if ranking requested) - Dimensions, included/excluded rationale
4. **Key Findings** - Curated recommendations with rationale
5. **Comparison** - Brief comparison of options (pros/cons)
6. **Recommendation** - Clear "do this" guidance
7. **Limitations** - What we didn't cover, caveats
8. **Sources** - Quality sources with IDs

## Anti-patterns to Avoid

- Treating MEPI as "skip quality" - VCRIV still runs
- Missing decomposition - Phase 1 is still mandatory
- No recommendation - MEPI must recommend, not just list
- Shallow research - curated != minimal effort
- Monolithic single-file research - MEPI also decomposes into individual topic files
- Summary without synthesis - Summary file must contain cross-document synthesis, not just topic links
