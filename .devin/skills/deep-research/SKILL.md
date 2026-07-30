---
name: deep-research
description: Apply when conducting deep research on technologies, APIs, frameworks, people, companies, organizations, networks, or other topics requiring systematic investigation
---

# Deep Research Skill

Systematic research using MCPI (Most Complete Point of Information) or MEPI (Most Executable Point of Information) approaches.

## When to Use

**Use this skill** when the user's intent requires:
- Making an informed decision between alternatives
- Understanding something deeply before acting
- Preparing for a complex undertaking
- Evaluating risks, trade-offs, or consequences
- Gathering exhaustive knowledge on a topic

## Quick Start

1. Read this SKILL.md for core principles
2. Detect Work Mode and create output folder (see "Output Folder" section below)
3. Read the appropriate strategy file (MCPI or MEPI)
4. Follow Phases 1-4 systematically
5. Output findings as INFO document

## Output Folder (Pre-Phase 1)

Deep research ALWAYS creates a dedicated subfolder for its outputs. This ensures parallel researches on the same topic cannot have filename or ID conflicts - each folder has an independent numbering namespace.

### Step 1.1: Detect Work Mode

1. Read workspace NOTES.md for `[DEFAULT_SESSIONS_FOLDER]`
2. Check from conversation: Is there an active session?
   - Active session exists -> SESSION-MODE
   - No active session -> PROJECT-MODE
3. If already working inside a `T##_` or `S##_` or other session subfolder -> create output folder here (Step 1.2)

### Step 1.2: Create Output Folder

**PROJECT-MODE:** Run `/session-new` first, then create Topic Folder inside.

**SESSION-MODE (default):** Create Topic Folder per @skills:session-management Topic Folder Creation procedure. Folder name: `T##_[TOPIC]-[PascalCaseName]_YYYY-MM-DD/`

**SESSION-MODE as Step (only if user explicitly requests):** Create Step Folder per @skills:session-management Step Folder naming. Folder name: `S##_[TOPIC]-[PascalCaseName]_YYYY-MM-DD/`

All deep-research output files go in this folder. Each folder has independent numbering namespace per @skills:session-management.

**Parallel research isolation**: Multiple deep-researches for the same TOPIC are safe because each gets its own `T##_` subfolder with independent file numbering. Topic IDs are unique per ID-REGISTRY.md, but folder-level isolation prevents file conflicts even when the same TOPIC is researched from different angles.

## Phase Model (Global)

All research (MCPI and MEPI) follows these 4 phases:

**Phase 1 - Preflight**: Decompose prompt, document assumptions, collect sources, verify/correct assumptions, create STRUT with QA pipelines, run first VCRIV

**Phase 2 - Planning**: Create Summary file (skeletal), topic template, TASKS plan, run second VCRIV

**Phase 3 - Research**: Topic-by-topic file-by-file research per TASKS/STRUT, run VCRIV per granularity rules

**Phase 4 - Final Verification and Sync**: Dimension coverage, completeness check, finalize Summary (cross-document synthesis), metadata, final VCRIV

Strategy files (MCPI/MEPI) define the details for each phase.

## Topic ID Registration (Phase 1, after Prompt Decomposition)

Before proceeding to source collection, ensure Topic ID uniqueness:
1. Read ID-REGISTRY.md in workspace root
2. Create Topic ID: 7-14 uppercase chars (mandatory for all new topics)
3. Check for collision with existing Topic IDs per Topic Registry rules in devsystem-ids.md
4. If collision: extend or narrow abbreviation
5. Register new Topic ID immediately in ID-REGISTRY.md

**Nested IDs for T##/S## subfolders:**
When deep research creates multiple `T##_` folders under one session topic, each subfolder uses a nested Doc ID: `[TOPIC]-[SUBTOPIC]-[DOC][NN]`. The SUBTOPIC (7-14 chars) is registered in session NOTES.md only, not in ID-REGISTRY.md. See devsystem-ids.md "Nested Document IDs" section.

## Prompt Decomposition (Phase 1, Step 1)

Answer these 7 questions before any source collection:

1. **Q1 - Goal**: What is the user's intent? (1-2 sentences)
2. **Q2 - Scope**: NARROW (1 dim), FOCUSED (2-4 dim), or EXPLORATORY (5-9 dim)?
3. **Q3 - Dimensions**: Which apply? (legal, financial, administrative, practical, technical, professional, medical, psychological, personal, organizational, strategic, security, cultural, educational, historical, or custom)
4. **Q4 - Topics**: 3-5 topics per dimension
5. **Q5 - Strategy**: MCPI (exhaustive) or MEPI (curated)?
6. **Q6 - Domain**: Which profile? (SOFTWARE, MARKET_INTEL, LEGAL, PROFILES, or DEFAULT)
7. **Q7 - Discovery Platforms**: What databases/platforms index this entity type? Test each, classify access level.

Store PromptDecomposition in STRUT plan. Do NOT proceed to source collection until all 7 questions are answered.

### PromptDecomposition Schema

```json
{
  "goal": "string (1-2 sentences)",
  "scope": "NARROW | FOCUSED | EXPLORATORY",
  "dimensions": ["list of dimension names"],
  "topics_per_dimension": { "dimension": ["topics"] },
  "strategy": "MCPI | MEPI",
  "strategy_rationale": "string (WHY this strategy fits the prompt)",
  "domain": "DEFAULT | SOFTWARE | MARKET_INTEL | LEGAL | PROFILES",
  "domain_rationale": "string (WHY this domain profile applies)",
  "effort_estimate": "N hours minimum",
  "discovery_platforms": {
    "identified": ["list of platforms that index this entity type"],
    "tested": { "platform_name": "FREE | PAID | PARTIAL" },
    "selected": ["platforms to use (FREE or PARTIAL only)"]
  }
}
```

### Scope Examples

- NARROW: "What are the rate limits for the Microsoft Graph API?" -> 1 dimension (technical)
- FOCUSED: "Should we use PostgreSQL or MongoDB for our event sourcing system?" -> 3 dimensions (technical, operational, financial)
- EXPLORATORY: "How should our startup approach SOC 2 compliance?" -> 6 dimensions (legal, technical, organizational, financial, operational, educational)

## MUST-NOT-FORGET

- **NEVER ask questions** - Derive goal or best option from the previous prompt, or from conversation context. Act on best inference
- **STRUT required** for all research sessions (include pipeline steps and time log)
- **Assumptions check first** - write down what you think you know before researching
- **Google search via Playwright** - MANDATORY for all research. Use ms-playwright-mcp to search google.com with targeted queries (filetype:pdf, site:, exact phrases). Discovers PDFs, whitepapers, and public documents that `search_web` misses.
- **Google = URL discovery only** - Never extract text content from Google result pages (AI Overview, Featured Snippets, Knowledge Panels, People Also Ask). Click through to source websites. See RESEARCH_TOOLS.md "Google Search Extraction Principle".
- **Discovery platforms tested** - identify, test, classify (FREE/PAID/PARTIAL) before source collection
- **Primary sources > secondary > community** - verify tier 1-3 before accepting tier 6-8
- **Access dates required**: `Accessed: YYYY-MM-DD` on all sources
- **Track time** - log task start/end for net research time calculation
- **Quality pipeline 3x** (not optional): Summary+template, each topic, complete set
- **Source completeness**: Full PDF transcription via pipeline, no agent-selected chunks
- **Download** source files (PDFs, images) to `_DOWNLOADS_gitignore/` subfolder (not checked in)
- **Transcribe** downloaded sources to `_SOURCES/` subfolder (checked in, web content changes)
- **Inline citations** on critical conclusions: `[LABEL] (SOURCE_ID | URL or filename)`
- **Identify domain** during Preflight, read corresponding DOMAIN_*.md profile
- **Document strategy choice** - OUTPUT document must include strategy (MEPI/MCPI) + domain + rationale for both in header block
- **Distinguish** facts from opinions from assumptions
- **Autonomous after Phase 1** - no user interaction until delivery (except [CONSULT])

## Effort Validation

- Decomposition MUST estimate minimum research hours in STRUT
- If actual time < 50% of estimate, agent MUST justify or expand research
- Goal: outperform equivalent human research time for the given scope

## Strategy Selection

**MEPI** (Default) - curated options, deeply researched, compare and recommend
- Use for: User intent is specific, danger of analysis-paralysis and introducing irrelevant options
- Strategy file: [RESEARCH_STRATEGY_MEPI.md](RESEARCH_STRATEGY_MEPI.md)

**MCPI** (Exception) - exhaustive coverage, document everything
- Use for: User intent is broad, wants to see the whole picture
- Strategy file: [RESEARCH_STRATEGY_MCPI.md](RESEARCH_STRATEGY_MCPI.md)

## Source Hierarchy

1. Official PDFs/papers (legislation, specs, whitepapers)
2. Official documentation
3. Official blog/changelog
4. GitHub repo
5. Conference talks by maintainers
6. Reputable tech blogs
7. Stack Overflow
8. Community forums/Discord

**Enforcement** (legal/financial/medical): MUST cite tier 1-3 for critical claims. Label tier 6-8 as `[COMMUNITY]`. Violation triggers `[CONSULT]` to user.

## Verification Labels

- `[VERIFIED]` - Confirmed from official docs
- `[ASSUMED]` - Inferred, not explicit
- `[TESTED]` - Manually tested
- `[PROVEN]` - Multiple independent sources
- `[COMMUNITY]` - Community sources (cite ID)

## Quality Pipeline (VCRIV)

```
verify → critique → reconcile → implement → verify
```

- **V** - Verify: Formal correctness check (`/verify` workflow)
- **C** - Critique: Find gaps, reasoning flaws; produces `*_REVIEW.md` (`/critique` workflow)
- **R** - Reconcile: Prioritize findings (`/reconcile` workflow)
- **I** - Implement: Apply findings, delete `*_REVIEW.md` (`/implement` workflow)
- **V** - Verify (final): Confirm corrections complete

**Four mandatory checkpoints:**
1. Preflight deliverables (STRUT, SOURCES, PromptDecomposition)
2. Planning deliverables (Summary file, template, TASKS)
3. Each research output (per VCRIV granularity rules)
4. Complete research set ex-post (after all topics complete)

**Execution modes:**
- **Full VCRIV** (5 steps): verify → critique → reconcile → implement → verify. Use for planning deliverables and final ex-post review.
- **Consolidated VCRIV** (1 step): All 5 steps executed in a single pass without separate review files. Use for individual topic files and single-profile research.

**Granularity** (scope-based):
- NARROW: VCRIV per topic file (consolidated)
- FOCUSED/EXPLORATORY: VCRIV per dimension (consolidated)
- Final VCRIV on Summary file (full)
- Profile research: VCRIV per standalone profile document (consolidated for single, full for network sets)

**Termination**: Max 2 cycles per checkpoint, then [CONSULT].

## Inline Citations

Critical conclusions MUST have: `[VERIFICATION_LABEL] (SOURCE_ID | URL or filename)`

Examples:
- `[VERIFIED] (GRPH-SC-MSFT-RATELMT | https://learn.microsoft.com/graph/throttling)`
- `[VERIFIED] (ANTH-SC-ANTH-MDLCRD | _SOURCES/anthropic-model-card-2025.md)`

Referenced files MUST exist in `_SOURCES/` subfolder (transcribed markdown).

## Domain Profiles

Read one profile per session based on Q6:
- [DOMAIN_SOFTWARE.md](software/DOMAIN_SOFTWARE.md) - APIs, frameworks, libraries
- [DOMAIN_MARKET_INTEL.md](market-intel/DOMAIN_MARKET_INTEL.md) - Companies, financials
- [DOMAIN_LEGAL.md](legal/DOMAIN_LEGAL.md) - Legislation, case law
- [DOMAIN_PROFILES.md](profiles/DOMAIN_PROFILES.md) - People, companies, organizations, networks
- [DOMAIN_DEFAULT.md](default/DOMAIN_DEFAULT.md) - Generic (use when none match)

## Output Format

INFO document with:
1. Research Question
2. **Strategy & Domain** (MEPI/MCPI + domain profile + rationale for each choice)
3. Key Findings (curated for MEPI, exhaustive for MCPI)
4. Detailed Analysis
5. Limitations and Known Issues
6. Sources (with verification labels)
7. Recommendations

MEPI uses its own output format (see RESEARCH_STRATEGY_MEPI.md) with Comparison and Recommendation sections.

## Planning Structure

**STRUT** (high-level, REQUIRED): Phases, objectives, deliverables, transitions, time log. File: `__STRUT_[TOPIC].md`

**TASKS** (low-level, Phase 2): Flat task list with durations and done-when criteria. File: `__TASKS_[TOPIC]_RESEARCH.md`

## Reference Files

- [RESEARCH_RULES.md](RESEARCH_RULES.md) - Verification and improvement rules for research output (used by `/verify` and `/improve`)
- [RESEARCH_TOOLS.md](RESEARCH_TOOLS.md) - Tools, source processing, configuration
- [RESEARCH_TOC_TEMPLATE.md](RESEARCH_TOC_TEMPLATE.md) - TOC template (MUST use when >1 topic files)
- [RESEARCH_CREATE_TOC.md](RESEARCH_CREATE_TOC.md) - TOC creation workflow
- [RESEARCH_SUMMARY_TEMPLATE.md](RESEARCH_SUMMARY_TEMPLATE.md) - Summary file template
- [RESEARCH_CREATE_SUMMARY.md](RESEARCH_CREATE_SUMMARY.md) - Summary creation workflow

**Profile Templates and Rules** (in `profiles/` subfolder, see [DOMAIN_PROFILES.md](profiles/DOMAIN_PROFILES.md) for full instructions):
- [PERSONAL_PROFILE_TEMPLATE.md](profiles/PERSONAL_PROFILE_TEMPLATE.md) + [PERSONAL_PROFILE_RULES.md](profiles/PERSONAL_PROFILE_RULES.md)
- [COMPANY_PROFILE_TEMPLATE.md](profiles/COMPANY_PROFILE_TEMPLATE.md) + [COMPANY_PROFILE_RULES.md](profiles/COMPANY_PROFILE_RULES.md)
- [ORGA_PROFILE_TEMPLATE.md](profiles/ORGA_PROFILE_TEMPLATE.md) + [ORGA_PROFILE_RULES.md](profiles/ORGA_PROFILE_RULES.md)
- [NETWORK_PROFILE_TEMPLATE.md](profiles/NETWORK_PROFILE_TEMPLATE.md) + [NETWORK_PROFILE_RULES.md](profiles/NETWORK_PROFILE_RULES.md)

**Output Rules** (global invariant):

- **Always create subfolder** per "Output Folder" section above. No exceptions.
- **Single-file output** (e.g., single profile): Apply naming convention from context (session, conversation, step, topic). File name does NOT use numbered scheme. Example: `_INFO_[TOPIC]_[SubjectName].md`
- **Multi-file output** (multiple sub-topics): Use numbered scheme with reserved slots:
  - `_INFO_[TOPIC]-01_Summary.md` - **RESERVED**. Mandatory. Stub created in Phase 2, finalized in Phase 4 with cross-document synthesis.
  - `_INFO_[TOPIC]-02_Sources.md` - **RESERVED**. Mandatory. Created in Phase 1, populated during Phases 1, 2, and 3.
  - `_INFO_[TOPIC]-03_[Name].md` through `_INFO_[TOPIC]-[NN]_[Name].md` - Individual topic files (PascalCase)

**Decomposition rule**: Both MCPI and MEPI decompose topics into individually researched files. No monolithic single-file research.

**Source ID format**: `[TOPIC]-SC-[SOURCE]-[DOCREF]`
- `[SOURCE]` = site mnemonic 2-6 chars (e.g., `MSFT`, `SO`, `GH`)
- `[DOCREF]` = page/section 2-12 chars, omit vowels (e.g., `RATELMT`, `ISSUE1234`)
- Note: Simplified from devsystem-ids.md `[TOPIC]-[DOC]-SC-...` format. The `[DOC]` segment is omitted because all sources are defined in `_INFO_[TOPIC]-02_Sources.md` (always IN02).
